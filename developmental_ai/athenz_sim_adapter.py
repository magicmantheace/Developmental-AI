"""Bounded, synthetic-only AthenZ ⇄ Developmental AI simulator adapter.

This is an offline, non-executing integration fixture. Source traces must be
independently replayable; signatures are producer-test authentication, NOT human
consent. Neither action nor policy/model promotion follows from an event.
"""
from __future__ import annotations

from datetime import datetime
from typing import Callable

from .athenz_bridge import BridgeError, _validate, synthetic_event
from .event_ledger import verify_ledger


def verified_synthetic_replies(
    inbound: dict, ledger: dict, trace: dict, *,
    athenz_secret: bytes, learner_secret: bytes,
    source_revision_check: Callable[[str, int], bool],
    learner_seq: int = 1, now: datetime | None = None,
) -> tuple[dict, dict]:
    """Project *one* verified simulator ledger into two non-authoritative events.

    Callers independently journal inbound/outbound envelopes for replay safety;
    this pure transformation never reads private memory, persists data or
    sends the returned events. It is NOT an authenticated IPC session.
    """
    if not callable(source_revision_check):
        raise BridgeError("Synthetic source revision checker required")
    _validate(inbound, {"athenz": athenz_secret, "learner": learner_secret}, now=now)
    if (inbound["producer"] != "athenz"
            or inbound["kind"] != "observation"
            or inbound["payload"].get("signal") != "trace_sha256"):
        raise BridgeError("Only synthetic AthenZ trace observations are accepted")
    if type(learner_seq) is not int or not 1 <= learner_seq <= 9999:
        raise BridgeError("Invalid response sequence")
    source, revision = inbound["source_ref"], inbound["source_revision"]

    def check() -> None:
        try:
            allowed = source_revision_check(source, revision) is True
        except Exception as exc:
            raise BridgeError("Synthetic source revision check failed") from exc
        if not allowed:
            raise BridgeError("Synthetic source revision was revoked")

    check()
    # The SHA-linked ledger does not prove identity or permission. Its
    # independently replayed source trace proves only synthetic consistency.
    try:
        verified = verify_ledger(ledger, trace)
        digest = ledger["trace_sha256"]
    except (ValueError, TypeError, KeyError, OverflowError) as exc:
        raise BridgeError("Unverified synthetic source trace") from exc
    if not verified.get("trace_bound") or inbound["payload"]["value"] != digest:
        raise BridgeError("Trace fingerprint does not match AthenZ observation")
    # No raw simulator payloads or private user text cross this interface.
    count = verified["events"]
    if type(count) is not int or not 1 <= count <= 1024:
        raise BridgeError("Unsupported simulator event count")
    check()  # Catch source changes during independently verified replay.
    common = {
        "producer": "learner", "task_id": inbound["task_id"],
        "source_ref": source, "source_revision": revision,
        "secret": learner_secret,
    }
    proposal = synthetic_event(
        **common, seq=learner_seq, kind="action_proposed",
        payload={"summary": "synthetic proposal only; no system action"},
    )
    receipt = synthetic_event(
        **common, seq=learner_seq + 1, kind="evaluation_receipt",
        payload={"result": f"independently replayed {count} simulator events"},
    )
    check()  # A final check before returning even non-executing proposals.
    return proposal, receipt
