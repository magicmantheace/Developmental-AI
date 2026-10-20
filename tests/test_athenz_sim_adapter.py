"""Synthetic Developmental AI → AthenZ trace-bound proposal interoperability."""
import copy
from datetime import datetime, timezone
import tempfile
from pathlib import Path
import unittest

from developmental_ai.athenz_bridge import (
    BridgeError, SyntheticBridgeJournal, _validate, synthetic_event,
)
from developmental_ai.athenz_sim_adapter import verified_synthetic_replies
from developmental_ai.curriculum import CurriculumBrain
from developmental_ai.event_ledger import export_trace


class AthenZSimulatorAdapterTests(unittest.TestCase):
    def setUp(self):
        root = tempfile.TemporaryDirectory()
        self.addCleanup(root.cleanup)
        self.root = Path(root.name)
        self.keys = {"athenz": b"a" * 32, "learner": b"l" * 32}
        self.revision = 1
        with CurriculumBrain(self.root / "brain.sqlite3", 11) as brain:
            self.trace = brain.trace("collect", 1, policy="oracle")
        self.ledger = export_trace(self.trace)
        self.inbound = synthetic_event(
            producer="athenz", task_id="interop", seq=1, kind="observation",
            source_ref="synthetic:interop", source_revision=1,
            payload={"signal": "trace_sha256",
                     "value": self.ledger["trace_sha256"]},
            secret=self.keys["athenz"])

    def replies(self, event=None, ledger=None, trace=None, **changes):
        return verified_synthetic_replies(
            event if event is not None else self.inbound,
            ledger if ledger is not None else self.ledger,
            trace if trace is not None else self.trace,
            athenz_secret=self.keys["athenz"],
            learner_secret=self.keys["learner"],
            source_revision_check=lambda src, ver:
                src == "synthetic:interop" and self.revision == ver,
            **changes)

    def test_independently_replayed_trace_produces_two_bounded_proposals(self):
        proposal, receipt = self.replies()
        self.assertEqual(proposal["producer"], "learner")
        self.assertEqual(proposal["origin"], "simulation_episode")
        self.assertEqual(proposal["kind"], "action_proposed")
        self.assertEqual(receipt["kind"], "evaluation_receipt")
        self.assertEqual(receipt["seq"], 2)
        self.assertEqual(proposal["scope"], "proposal_only")
        self.assertNotIn("command", proposal["payload"])
        self.assertNotIn("environment", receipt["payload"])
        _validate(proposal, self.keys)
        _validate(receipt, self.keys)

        # Verify a consumer with the same AthenZ wire implementation can
        # persist each producer's own sequence without granting any actions.
        journal = SyntheticBridgeJournal(
            self.root / "private-journal.sqlite3", keys=self.keys,
            consent_check=lambda src, ver: src == "synthetic:interop" and ver == 1,
            enabled=True)
        try:
            for item in (self.inbound, proposal, receipt):
                self.assertEqual(journal.receive(item)["status"], "accepted")
                self.assertFalse(journal.receive(item)["actions_executed"])
            self.assertEqual(journal.db.execute(
                "SELECT COUNT(*) FROM bridge_events").fetchone()[0], 3)
        finally:
            journal.close()

    def test_modified_trace_digest_is_not_accepted(self):
        altered = copy.deepcopy(self.inbound)
        altered["payload"]["value"] = "0" * 64
        # Re-sign to show source mismatch still fails AFTER successful
        # authenticated transport validation.
        from developmental_ai.athenz_bridge import _canonical
        import hashlib
        import hmac
        unsigned = {k: v for k, v in altered.items() if k != "signature"}
        altered["signature"] = hmac.new(
            self.keys["athenz"], _canonical(unsigned), hashlib.sha256).hexdigest()
        with self.assertRaisesRegex(BridgeError, "fingerprint"):
            self.replies(event=altered)

    def test_rehashed_ledger_cannot_override_independent_trace(self):
        altered = copy.deepcopy(self.ledger)
        altered["events"][0]["payload"]["state"] = "tampered"
        with self.assertRaisesRegex(BridgeError, "Unverified"):
            self.replies(ledger=altered)

    def test_nonobservation_and_nonathenz_input_rejected(self):
        event = synthetic_event(
            producer="athenz", task_id="interop", seq=1,
            kind="outcome", source_ref="synthetic:interop", source_revision=1,
            payload={"accepted": True, "result": "simulated"},
            secret=self.keys["athenz"])
        with self.assertRaisesRegex(BridgeError, "Only synthetic"):
            self.replies(event=event)
        event = synthetic_event(
            producer="learner", task_id="interop", seq=1,
            kind="action_proposed", source_ref="synthetic:interop", source_revision=1,
            payload={"summary": "try"},
            secret=self.keys["learner"])
        with self.assertRaisesRegex(BridgeError, "Only synthetic"):
            self.replies(event=event)

    def test_source_revoked_at_first_review(self):
        self.revision = 2
        with self.assertRaisesRegex(BridgeError, "revoked"):
            self.replies()

    def test_source_revoked_during_trace_replay(self):
        calls = [0]
        def current(src, ver):
            calls[0] += 1
            return calls[0] == 1
        with self.assertRaisesRegex(BridgeError, "revoked"):
            verified_synthetic_replies(
                self.inbound, self.ledger, self.trace,
                athenz_secret=self.keys["athenz"],
                learner_secret=self.keys["learner"],
                source_revision_check=current)
        self.assertGreaterEqual(calls[0], 2)

    def test_missing_checker_or_bad_sequence_rejected(self):
        with self.assertRaisesRegex(BridgeError, "checker"):
            verified_synthetic_replies(
                self.inbound, self.ledger, self.trace,
                athenz_secret=self.keys["athenz"],
                learner_secret=self.keys["learner"],
                source_revision_check=None)
        for sequence in (0, True, 10000):
            with self.subTest(sequence=sequence):
                with self.assertRaisesRegex(BridgeError, "sequence"):
                    self.replies(learner_seq=sequence)

    def test_unrelated_digest_and_no_real_caller_rejected(self):
        another = copy.deepcopy(self.ledger)
        another["trace_sha256"] = "b" * 64
        with self.assertRaises(BridgeError):
            self.replies(ledger=another)
        tampered = copy.deepcopy(self.inbound)
        tampered["namespace"] = "human"
        with self.assertRaises(BridgeError):
            self.replies(event=tampered)

    def test_no_private_contents_persisted_by_transformation(self):
        proposal, receipt = self.replies()
        self.assertNotIn(self.inbound["payload"]["value"], str(proposal))
        self.assertNotIn(self.inbound["payload"]["value"], str(receipt))
        self.assertTrue(all(item["source_ref"] == "synthetic:interop"
                            for item in (proposal, receipt)))


if __name__ == "__main__":
    unittest.main()
