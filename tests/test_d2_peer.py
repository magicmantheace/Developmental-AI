"""Private Developmental AI D2 peer bootstrap and verified-simulator tests.

The optional end-to-end test requires a separately installed AthenZ package;
these tests do not import AthenZ at module-import time.
"""
from __future__ import annotations

import importlib.util
from io import BytesIO
import os
from pathlib import Path
import secrets
import subprocess
import sys
import tempfile
import threading
import unittest

from developmental_ai.d2_peer import (
    BOOTSTRAP_BYTES, _read_bootstrap, serve_one, verified_fixture_trace,
)
from developmental_ai.event_ledger import verify_ledger

SOURCE = "synthetic:interop"


class D2PeerUnitTests(unittest.TestCase):
    def test_binary_secret_bootstrap_partial_reads(self):
        class Slow(BytesIO):
            def read(self, n=-1):
                return super().read(min(3, n))
        raw = secrets.token_bytes(BOOTSTRAP_BYTES)
        root, keys = _read_bootstrap(Slow(raw))
        self.assertEqual(root, raw[:32])
        self.assertEqual(keys["athenz"], raw[32:64])
        self.assertEqual(keys["learner"], raw[64:96])
        self.assertNotEqual(root, keys["athenz"])
        self.assertNotEqual(keys["athenz"], keys["learner"])

    def test_truncated_bootstrap_is_denied(self):
        for data in (b"", b"a" * 95, b"b" * 63):
            with self.subTest(length=len(data)):
                with self.assertRaisesRegex(ValueError, "Incomplete"):
                    _read_bootstrap(BytesIO(data))

    def test_nonbinary_bootstrap_is_denied(self):
        with self.assertRaises(ValueError):
            _read_bootstrap(BytesIO(b"a" * 2).read(0) if False else __import__("io").StringIO("x" * 96))

    def test_peer_is_off_by_default_without_importing_athenz(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "disabled"):
                serve_one(BytesIO(), BytesIO(), home=Path(tmp))
        self.assertEqual(len([item for item in sys.modules
                              if item.startswith("athenz.developmental_")]), 0)

    def test_frozen_fixture_trace_replays_independently(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            first, ledger = verified_fixture_trace(home)
            self.assertTrue(verify_ledger(ledger, first)["trace_bound"])
            trace2, ledger2 = verified_fixture_trace(home)
            self.assertEqual(first["sha256"], trace2["sha256"])
            self.assertEqual(ledger["trace_sha256"], ledger2["trace_sha256"])
            self.assertEqual(ledger, ledger2)
            self.assertEqual(ledger["scope"], "simulation-only")

    def test_entry_point_rejects_implicit_launch(self):
        from developmental_ai.d2_peer import main
        old = sys.argv
        try:
            sys.argv = ["d2_peer", "--help"]
            self.assertEqual(main(), 2)
        finally:
            sys.argv = old


@unittest.skipUnless(importlib.util.find_spec("athenz") is not None,
                     "AthenZ Python package must be installed to test D2 cross-process protocol")
class OptionalInstalledAthenZInteropTests(unittest.TestCase):
    def test_separate_process_real_simulator_trace_durable_ack(self):
        from athenz.developmental_bridge import synthetic_event
        from athenz.developmental_consent import SyntheticSourceRegistry
        from athenz.developmental_exchange import SyntheticExchange
        from athenz.developmental_receiver import SyntheticDurableReceiver
        from athenz.developmental_roundtrip import synthetic_trace_roundtrip

        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "private"
            with SyntheticSourceRegistry(home) as grants:
                preview = grants.preview(SOURCE, "approve")
                grants.review(SOURCE, "approve",
                              review_sha256=preview["review_sha256"], confirmed=True)
                trace, ledger = verified_fixture_trace(home)
                assert verify_ledger(ledger, trace)["trace_bound"]
                bundle = secrets.token_bytes(96)
                keys = {"athenz": bundle[32:64], "learner": bundle[64:]}
                with SyntheticDurableReceiver(
                    home / "athenz_received.sqlite3", keys=keys,
                    revision_check=grants.is_current, enabled=True
                ) as journal, SyntheticExchange.from_registry(
                    home / "athenz_outbox.sqlite3", keys=keys,
                    registry=grants, enabled=True,
                ) as outbox:
                    request = synthetic_event(
                        producer="athenz", task_id="verified", seq=1,
                        kind="observation", source_ref=SOURCE, source_revision=1,
                        payload={"signal": "trace_sha256",
                                 "value": ledger["trace_sha256"]},
                        secret=keys["athenz"])
                    env = {k: os.environ[k] for k in (
                        "PATH", "SYSTEMROOT", "SystemRoot", "WINDIR",
                        "COMSPEC", "PATHEXT", "TMP", "TEMP", "TMPDIR", "HOME")
                        if k in os.environ}
                    env["PYTHONNOUSERSITE"] = "1"
                    root = Path(__file__).resolve().parents[1]
                    env["PYTHONPATH"] = str(root)
                    process = subprocess.Popen(
                        [sys.executable, "-m", "developmental_ai.d2_peer",
                         "--synthetic-d2-test", str(home)],
                        cwd=root, env=env,
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE, bufsize=-1)
                    expired = threading.Event()
                    def stop():
                        if process.poll() is None:
                            expired.set()
                            process.kill()
                    timer = threading.Timer(15, stop)
                    timer.daemon = True
                    timer.start()
                    try:
                        process.stdin.write(bundle)
                        process.stdin.flush()
                        result = synthetic_trace_roundtrip(
                            process.stdout, process.stdin, root_secret=bundle[:32],
                            producer_keys=keys, registry=grants, receiver=journal,
                            exchange=outbox, request=request, enabled=True)
                        process.stdin.close()
                        self.assertEqual(process.wait(timeout=5), 0)
                        self.assertFalse(expired.is_set())
                        self.assertEqual(result["acknowledgments_sent"], 2)
                        self.assertEqual(result["actions_executed"], False)
                    finally:
                        timer.cancel()
                        if process.poll() is None:
                            process.kill()
                        process.wait(timeout=5)
                        for pipe in (process.stdin, process.stdout, process.stderr):
                            if pipe is not None and not pipe.closed:
                                pipe.close()


if __name__ == "__main__":
    unittest.main()
