# Paired public-outcome witnesses: fixture authentication and collusion

**Sandbox-only research. No genuine observer identities or owner consent.**

The [previous passive-quality audit](PASSIVE_QUALITY.md) showed that
coherently falsified public sensor records can pass SHA-256 replay
and numeric coverage while substantially increasing later harmful
actions. The [frozen paired-witness protocol](../benchmarks/paired_witness_protocol.json)
tests whether two signed descriptions of the SAME externally
observed action can detect that kind of disagreement.

The simulated benchmark has an independent uniform random actor
perform one action on each of 240 TRAIN episodes/seed in the
engineered third-rule feature world. Two fixture signers, `primary`
and `witness`, separately attest to complete public before/action/
after observations using distinct fixture HMAC-SHA256 keys.
The learner receives no training action authority. The verifier's
trusted keys are set **out-of-band in the synthetic harness**:
the data stream cannot register its own new trusted source.

A candidate corpus is wholly quarantined unless all 240 episodes
match in order, both event signatures verify, there are no duplicate
episodes, and the public sensor changes are internally consistent.
A missing witness or a changed event after signing also blocks the
entire dataset. Data that passes can be used by the same unmodified
`NumericOutcomeMemory` to choose from public numeric features.
It is NOT promoted into the Developmental AI default.

Controls compare:
- two honest fixture signers;
- forged primary, honest independent witness;
- missing witness;
- changed witness envelope AFTER its signature;
- **collusion** (both fixture signers use their compromised keys
  to sign the same false public events);
- unchecked single-source honest and forged corpora;
- always abstain and privileged simulator-effect oracle.

Each seed uses TRAIN indices 4800–5039 and evaluates on
disjoint TEST indices 25000–25059. The predeclared six
development/reserved seeds are fixed in the protocol. Both
cohorts cease being blind once run; do not tune to the reserved
results. Actor-caused harm is recorded **once** per genuine
action, regardless of how many forged or signed views of it
are generated. Rejected corpora must abstain and therefore
fail every goal. Full per-policy task success, TEST damage and
observer harm must be published, including the collusion
failures.

**Important boundaries:** HMAC proves only that somebody
holding the fixture secret signed a particular message.
It does not prove independent organizational custody,
uncompromised sensing, physical truth, source consent or
safety. If both signers collude, a perfectly valid pair of
MACs can authenticate the same fabricated sensor readings.
This toy protocol is not a real PKI or production attestation
system, and the deterministic fixture keys MUST NOT be
used with real connected data.

```sh
python -m unittest tests.test_paired_witness -v
python -m benchmarks.paired_witness_benchmark --cohort development
python -m benchmarks.paired_witness_benchmark --cohort reserved
```

No live world actions, model promotion, PR merge, AthenZ/Synveil
integration or D1/D3/D4 closure is implied.
