# AthenZ D2 synthetic interoperability fixture (experimental)

**Status:** a trace-verified in-process adapter plus a new **opt-in one-shot
synthetic subprocess peer** are staged on this private draft branch. The peer
has not passed private CI. There is still no production IPC, chat integration,
unattended development loop, owner-consent binding, device action, model
promotion, training, or public network listener. The one-shot peer uses an
outside-Git private durable outbound queue only for synthetic fixtures.

## Supported adapter

`developmental_ai.athenz_bridge` implements the exact AthenZ D2 version-one
synthetic envelope validator and metadata-only SQLite replay/revocation journal.
The two projects have the same `tests/fixtures/d2_synthetic_vector.json`.
The fixture uses deliberately public, hard-coded HMAC keys **for tests only**.
They are not owner credentials. A test key does not confer human consent.

`developmental_ai.athenz_sim_adapter.verified_synthetic_replies` takes:

- An authenticated sandbox-only AthenZ `observation` envelope with
  `payload.signal=trace_sha256` and `payload.value` equal to the verified
  synthetic trace's SHA-256.
- The independently replayable, SHA-linked simulated ledger and original
  trace produced by `developmental_ai.event_ledger`.
- Separate test HMAC producer secrets and a mandatory, caller-supplied
  synthetic source-revision callback, checked before replay, after replay
  and again before return.
- A caller-owned next learner sequence number.

The adapter returns an authenticated `action_proposed` plus an
`evaluation_receipt` that say only a simulator trace was replayed.
The proposal is intentionally a **non-executable generic summary**, not
a learned physical action or permission to run anything.
The outputs identify `simulation_episode`, never a human biography.
No raw simulation trace, memory, user prompt, private file, training data,
or privileged state appears in their payloads.

An AthenZ `observation` is tagged `human_record` in the existing
synthetic wire allowlist. Here its payload is strictly a trace **reference**,
not evidence of a human-origin observation or simulated human experience.
Future wire versions should separate request provenance from observation
contents rather than interpret that tag as an actual person fact.

## Intentional exclusions and risks

The simulator hash chain detects record consistency but is not a signature.
The HMAC validates a test producer key, not the owner, nor the original
simulator source. The revision-check callback here is a synthetic fixture,
**not** a connection to AthenZ's authoritative reviewed-source database.
Matching counters and SQLite journals prevent local duplicate processing,
but this adapter does not persist its returned reply pair; if a process
crashes after marking an inbound message accepted, it may lose the reply.
Do not use it for production delivery or autonomous actuation.

For a real D2 bridge, implement OS-protected key provisioning, authenticated
local-only IPC on Windows/WSL2 and Linux, a durable authorized
input/output outbox, exact replay after restart, AthenZ-backed consent
lifecycle and revoked-derived-state deletion. Record process loss and
negative test results. Only then claim a trusted transport.

## Experimental verified simulator peer (2026-10-18)

`python -m developmental_ai.d2_peer --synthetic-d2-test <private-home>`
is an explicit one-shot development entry point. It has no general-purpose
shell/agent loop and does nothing unless invoked with the exact flag. An
already trusted AthenZ supervisor must open its **stdin and stdout binary
streams** and deliver 96 fresh random bytes (root HMAC key, AthenZ event key,
learner event key) via stdin *before* the strict authenticated D2 handshake.
No secret should appear in CLI arguments, public source, telemetry or
environment variables.

The peer uses the AthenZ Python package as an **optional integration
dependency**. Developmental AI remains standalone when the entry point is
not called. The AthenZ connection manages `synthetic:interop` approval
and the local D2 source registry, creates a fresh authenticated session,
and sends only a signed SHA-256 trace reference.

Unlike the public AthenZ test stand-in, the private peer generates a
**real, independently replayable simulator trace** from the unchanged
`CurriculumBrain(..., seed=11).trace("collect", 1, policy="oracle")`
and `export_trace` fixture. It verifies that both the original trace
and ledger match the signed SHA requested by AthenZ using
`verified_synthetic_replies`. The oracle policy is a privileged
**baseline**, not a learned cognition model. No simulator state leaves
the process. The two generic signed event envelopes are staged as one
transaction in an independent private SQLite outbox, delivered via the
session-authenticated binary stream, and not marked acknowledged until
both session-bound HMAC receipts are checked.

Tests in `tests/test_d2_peer.py` validate binary bootstrap, missing/bad
keys, an unchanged trace, and the default-disabled API. When AthenZ is
also installed, a separate-process integration test exercises the actual
private simulator-to-AthenZ roundtrip. Private GitHub Actions were previously
blocked before any job started; **do not claim these tests passed until
they have actually executed**. Keep this PR as a draft until validated.

Remaining blockers: verified operating-system peer identity, durable
restart reconciliation for partially acknowledged messages, protected
key provisioning/rotation, immutable owner-granted synthetic source
references and eventually real human-source consent, and an independently
tested receiver of learner episodes. This experiment does not grant
Developmental AI access to owner memories, tools, or model promotion.

## Fixed, preapproved local demonstration

The private integration branch also contains
`python -m developmental_ai.d2_demo`. The command is deliberately
**disabled unless** the exact `--synthetic-d2-demo` flag is present,
and it never implicitly approves a source, launches a user-supplied
executable, runs arbitrary shell commands, or reads a real owner profile.

With both repositories installed into one Python environment, use an
outside-Git private test home. First review the exact synthetic grant
using AthenZ's two-step CLI:

```sh
python -m athenz.developmental_consent_cli --home /private/test/home preview synthetic:interop approve
python -m athenz.developmental_consent_cli --home /private/test/home review synthetic:interop approve --review-sha256 <digest-from-preview> --confirm
```

Only after inspecting/confirming that **synthetic-only** preview:

```sh
python -m developmental_ai.d2_demo --synthetic-d2-demo --home /private/test/home
```

The first command approves no personal records or real-world actions.
The second generates all three 32-byte protocol keys in memory for
this one run, launches the **fixed** private module
`developmental_ai.d2_peer` under the current Python interpreter
(no shell and no externally provided executable path), and passes
bootstrap bytes over a binary stdin pipe. It computes the frozen
simulator trace digest locally, sends its signed SHA-only reference,
checks two signed proposals against the durable AthenZ receiver, then
requires two independent session-HMAC delivery receipts in the private
learner's outbox before reporting a no-action result. Both processes
have strict bounded lifetimes.

`tests/test_d2_peer.py` now includes tests for default disablement,
missing/invalid bootstrap, deterministic trace verification, denied
unapproved sources, and optional separate-process end-to-end behavior
when AthenZ is also importable. **None of these private tests is
reported as passed:** current private Actions infrastructure still
blocks job execution before any test begins. A successful public
AthenZ mock-peer test does not validate the private implementation.

This demo is a D2 research fixture, **not** a production training loop,
OS identity guarantee, authenticated human consent, independent mind
or model promotion system. Do not supply personal data or replace
ephemeral demo secrets with real owner credentials.
