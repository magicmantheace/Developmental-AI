"""Manual, one-shot local D2 simulator demonstration (NOT production).

Runs only the fixed developmental_ai.d2_peer Python module. Never launches
user-supplied shell commands, loads a person's memory or auto-approves grants.
All three transport/signing keys are fresh per invocation and passed via
binary stdin, never CLI arguments, environment variables or source files.
"""
from __future__ import annotations

import argparse
from contextlib import closing
import importlib.util
import os
from pathlib import Path
import secrets
import sqlite3
import subprocess
import sys
import threading
from uuid import uuid4

from .d2_peer import SOURCE, verified_fixture_trace
from .event_ledger import verify_ledger


def run_demo(home: Path, *, enabled: bool = False) -> dict:
    if enabled is not True:
        raise ValueError("Synthetic D2 process demonstration disabled")
    # Importing AthenZ is an explicit, optional integration, not a normal
    # dependency of the standalone developmental learning experiments.
    from athenz.developmental_bridge import BridgeError, synthetic_event
    from athenz.developmental_consent import SyntheticSourceRegistry
    from athenz.developmental_exchange import SyntheticExchange
    from athenz.developmental_receiver import SyntheticDurableReceiver
    from athenz.developmental_roundtrip import synthetic_trace_roundtrip

    with SyntheticSourceRegistry(home) as registry:
        if not registry.is_current(SOURCE, 1):
            raise ValueError(
                "Preapprove synthetic:interop revision 1 with AthenZ's review CLI")
        trace, ledger = verified_fixture_trace(registry.home)
        if verify_ledger(ledger, trace).get("trace_bound") is not True:
            raise ValueError("Simulator trace verification failed")
        material = secrets.token_bytes(96)
        producer_keys = {
            "athenz": material[32:64], "learner": material[64:96],
        }
        request = synthetic_event(
            producer="athenz", task_id="demo_" + uuid4().hex,
            seq=1, kind="observation", source_ref=SOURCE,
            source_revision=1,
            payload={"signal": "trace_sha256",
                     "value": ledger["trace_sha256"]},
            secret=producer_keys["athenz"])
        with SyntheticDurableReceiver(
            registry.home / "d2_demo_received.sqlite3",
            keys=producer_keys, revision_check=registry.is_current,
            enabled=True) as receiver, SyntheticExchange.from_registry(
            registry.home / "d2_demo_athenz_outbox.sqlite3",
            keys=producer_keys, registry=registry,
            enabled=True) as exchange:
            # Fixed module, current Python, no shell and no caller-provided
            # executable/path. Sanitized env intentionally omits credentials.
            root = Path(__file__).resolve().parents[1]
            env = {k: os.environ[k] for k in (
                "PATH", "SYSTEMROOT", "SystemRoot", "WINDIR", "COMSPEC",
                "PATHEXT", "TMP", "TEMP", "TMPDIR", "HOME")
                if k in os.environ}
            env["PYTHONNOUSERSITE"] = "1"
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            spec = importlib.util.find_spec("athenz")
            if spec is None or spec.submodule_search_locations is None:
                raise ValueError("Install AthenZ Python package for D2 demo")
            package = next(iter(spec.submodule_search_locations))
            env["PYTHONPATH"] = os.pathsep.join((str(root), str(Path(package).parent)))
            peer = subprocess.Popen(
                [sys.executable, "-m", "developmental_ai.d2_peer",
                 "--synthetic-d2-test", str(registry.home)],
                cwd=root, env=env, shell=False,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, bufsize=-1)
            timed_out = threading.Event()
            def expire():
                if peer.poll() is None:
                    timed_out.set()
                    peer.kill()
            timer = threading.Timer(15, expire)
            timer.daemon = True
            timer.start()
            try:
                peer.stdin.write(material)
                peer.stdin.flush()
                result = synthetic_trace_roundtrip(
                    peer.stdout, peer.stdin,
                    root_secret=material[:32], producer_keys=producer_keys,
                    registry=registry, receiver=receiver, exchange=exchange,
                    request=request, enabled=True)
                peer.stdin.close()
                if peer.wait(timeout=5) != 0 or timed_out.is_set():
                    raise ValueError("Developmental AI peer did not finish cleanly")
                with closing(sqlite3.connect(
                    registry.home / "d2_developmental_peer_outbox.sqlite3")) as db:
                    count = db.execute(
                        "SELECT count(*) FROM d2_outbox "
                        "WHERE request_id=? AND state='acked'",
                        (request["event_id"],)).fetchone()[0]
                if count != 2:
                    raise ValueError("Developmental AI peer ACK commit missing")
                return {
                    "status": "verified_synthetic_process_roundtrip",
                    "signed_replies": result["received_events"],
                    "authenticated_acknowledgments": count,
                    "actions_executed": False,
                }
            finally:
                timer.cancel()
                if peer.poll() is None:
                    peer.kill()
                peer.wait(timeout=5)
                for stream in (peer.stdin, peer.stdout, peer.stderr):
                    if stream is not None and not stream.closed:
                        stream.close()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Opt-in fixed synthetic D2 local simulator demo; no real owner data")
    parser.add_argument("--synthetic-d2-demo", action="store_true")
    parser.add_argument("--home", type=Path, required=True)
    args = parser.parse_args()
    if not args.synthetic_d2_demo:
        parser.error("The --synthetic-d2-demo flag is required")
    try:
        result = run_demo(args.home, enabled=True)
    except Exception as exc:
        print("D2 local synthetic demo failed: " + type(exc).__name__,
              file=sys.stderr)
        return 1
    # Only status metadata is displayed; no keys, inputs or traces.
    import json
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
