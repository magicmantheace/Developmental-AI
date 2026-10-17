# AthenZ D2 synthetic interoperability fixture (experimental)

**Status:** in-process demonstration only. No production IPC, chat integration,
unattended development loop, owner-consent binding, device action, model
promotion, training, public network listener or permanent outbound queue.

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
