"""One-shot Developmental AI D2 synthetic simulator peer (opt-in fixture).

This is deliberately NOT a general worker/service: no shell tools, model
promotion, owner profile ingestion, network sockets or automation. It requires
the separately installed AthenZ Python package for authenticated D2 binary
pipes and never uses public/test HMAC secrets in runtime code.
"""
from __future__ import annotations

from pathlib import Path
import sys
from typing import BinaryIO

from .athenz_sim_adapter import verified_synthetic_replies
from .curriculum import CurriculumBrain
from .event_ledger import export_trace

BOOTSTRAP_BYTES = 96
SOURCE = "synthetic:interop"
TASK = "collect"
SEED = 11
EPISODE = 1
POLICY = "oracle"


def _read_bootstrap(stream: BinaryIO) -> tuple[bytes, dict[str, bytes]]:
    """Read fresh one-time root/event secrets from an already-open binary pipe."""
    material = bytearray()
    while len(material) < BOOTSTRAP_BYTES:
        part = stream.read(BOOTSTRAP_BYTES - len(material))
        if type(part) is not bytes or not part:
            raise ValueError("Incomplete one-shot D2 bootstrap")
        material.extend(part)
    return (
        bytes(material[:32]),
        {"athenz": bytes(material[32:64]),
         "learner": bytes(material[64:96])},
    )


def verified_fixture_trace(home: Path) -> tuple[dict, dict]:
    """Recreate one independently verifiable, simulator-only trace and ledger.

    The private profile is outside every Git tree; no raw trace crosses
    the AthenZ wire. The benchmark policy here is an oracle fixture,
    NOT a learned or deployed agent.
    """
    with CurriculumBrain(home / "d2_curriculum_fixture.sqlite3", SEED) as brain:
        trace = brain.trace(TASK, EPISODE, policy=POLICY)
    ledger = export_trace(trace)
    return trace, ledger


def serve_one(reader: BinaryIO, writer: BinaryIO, *, home: Path,
              enabled: bool = False) -> dict:
    """Authenticate one synthetic request, replay trace, stage replies, wait for ACK.

    Imports AthenZ only after explicit enablement. AthenZ and Developmental
    AI remain independently installable when this experimental entry point
    is not used.
    """
    if enabled is not True:
        raise ValueError("D2 simulation peer is disabled")
    from athenz.developmental_ack import SyntheticDeliveryAck
    from athenz.developmental_consent import SyntheticSourceRegistry
    from athenz.developmental_exchange import SyntheticExchange
    from athenz.developmental_pipe import learner_handshake

    root, keys = _read_bootstrap(reader)
    with SyntheticSourceRegistry(home) as grants:
        # Approval is synthetic-only; this grants no real owner data or tools.
        with SyntheticExchange.from_registry(
            home / "d2_developmental_peer_outbox.sqlite3",
            keys=keys, registry=grants, enabled=True) as outbox:
            session = learner_handshake(
                reader, writer, root_secret=root, producer_keys=keys,
                revision_check=grants.is_current, enabled=True)
            inbound = session.receive(reader, expected_producer="athenz")
            if (inbound["source_ref"] != SOURCE
                    or inbound["kind"] != "observation"
                    or inbound["payload"].get("signal") != "trace_sha256"):
                raise ValueError("Only the frozen synthetic simulator trace is supported")
            trace, ledger = verified_fixture_trace(home)
            first, second = verified_synthetic_replies(
                inbound, ledger, trace,
                athenz_secret=keys["athenz"],
                learner_secret=keys["learner"],
                source_revision_check=grants.is_current,
                learner_seq=1)
            staged = outbox.stage_pair(inbound, first, second)
            if staged["status"] not in ("staged", "duplicate"):
                raise ValueError("Synthetic D2 pair was not staged")
            pending = outbox.pending()
            if len(pending) != 2 or [m["event_id"] for m in pending] != [
                    first["event_id"], second["event_id"]]:
                raise ValueError("Expected exactly two pending synthetic replies")
            for event in pending:
                session.send(writer, event)
            ack = SyntheticDeliveryAck(session, enabled=True)
            for _ in range(2):
                receipt = ack.receive(reader, outbox)
                if receipt["status"] not in ("acked", "duplicate"):
                    raise ValueError("Synthetic receipt was not accepted")
            if outbox.pending():
                raise ValueError("Synthetic delivery is still pending")
            return {
                "status": "synthetic_pair_acknowledged",
                "events": 2, "actions_executed": False,
            }


def main() -> int:
    # The home path is not a secret; keys are NEVER accepted via CLI or env.
    if len(sys.argv) != 3 or sys.argv[1] != "--synthetic-d2-test":
        return 2
    try:
        serve_one(sys.stdin.buffer, sys.stdout.buffer,
                  home=Path(sys.argv[2]), enabled=True)
    except Exception as exc:
        print("Synthetic D2 peer rejected session: " + type(exc).__name__,
              file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
