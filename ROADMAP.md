# Developmental AI — Milestone roadmap through 2029-02-09

## Product boundary

This repository owns **learning and simulation**, not the human's identity or the operating system. AthenZ owns consented identity, user-approved memories, dialogue, human-vs-digital autobiographies, and permissioned agent goals. Synveil owns operating-system services, deterministic policy, and controlled actuators. We should never make Synveil a prerequisite for running this engine in a Windows or generic Linux development environment.

**Success definition:** a continuously operable research-grade agent can learn in previously unseen bounded environments, retain experience and skills across restarts, develop and evaluate its own allowed goals, and integrate with an AthenZ model of a consenting person. This does not claim consciousness, human-equivalent intelligence, or survival of the original person's identity.

## Gates

| Due | Gate | Acceptance test | Status |
| --- | --- | --- | --- |
| 2026 Q4 | D0: import reproducible fixed-world POC | Existing tests pass; no private DB tracked | Done |
| 2026 Q4 | D1: randomized worlds + holdout protocol | 3 seeded held-out success gains; independent seeds; persistence | Initial implementation; held-out protocol needs frozen independent seeds |
| 2027 Q1 | D2: documented simulation and agent interface | Stable versioned schemas, deterministic environment replay, standalone service adapter | Not started |
| 2027 Q2 | D3: real generalization | Transfer across *held-out task families* and changed observation distributions, not just new layouts | Not started |
| 2027 Q3 | D4: reusable skills | Skill discovery, transfer, outcome-grounded retrieval, regression checks | Not started |
| 2027 Q4 | D5: autonomous goal selection in sandbox | Self-initiated achievable goals with visible budgets, feedback, and interrupt controls | Not started |
| 2028 Q1 | D6: lifelong learning | Consolidation, skill retention, versioned rollback, no unreviewed weight promotion | Not started |
| 2028 Q2 | D7: AthenZ integration | Human-origin memories clearly separated from agent episodes, provenance/consent enforced | Not started |
| 2028 Q3 | D8: Synveil integration | Bounded event/actuation interface, safe fallback when AI subsystem stops | Not started |
| 2028 Q4 | D9: long-run reliability | 30-day test with planned restarts, restoration, measured learning and failure records | Not started |
| 2029-02-09 | D10: integrated candidate | Reproduce published benchmarks; protected AthenZ twin; documented operating limits | Not started |

## Immediate next work

1. Freeze evaluation protocols and add independent post-development blind seeds; measure across obstacle densities, size ranges, sensory noise, and new objective types.
2. Add deterministic event replay and explicit per-event provenance without inserting private experience text into Git.
3. Build a clean environment/policy/memory plugin interface; keep simulation and AthenZ identity services separate.
4. Add systematic baselines: random, heuristic, shortest-path oracle (upper bound), trained policy, and ablations for curiosity and memory.
5. Add recurrent policy/world-model experiments only after transfer experiments expose meaningful failures requiring that complexity.

## Hard constraints

- A high score in one narrow simulator is not evidence of a mind, self-awareness, or ability to model a person.
- Independent seeds and no test feedback used for training; report if protocol was tuned to test data.
- No unrestricted shell, network, or desktop control by the learning policy.
- No human names, messages, voice, biometrics, consent records or private trained models committed to this repository.
- Test/restore checkpoint compatibility before any persistent format changes.

## Multi-task milestone — 2026-10-13

- [x] Three task rules share one partial-observation learned policy.
- [x] Seed-separated task generation; versioned, task-bound durable checkpoints.
- [x] Simulation-only decision traces, deterministic transition replay, digest.
- [x] Random, greedy, and full-map oracle references; restart-equivalent tests.
- [ ] D2 service/event interface remains unimplemented.
- [ ] D3 remains open: the learner relies on target cues and is weaker than
      the greedy baseline; next tests must address cue removal, novel objective
      families and independent blind benchmarking.

## 2026-10-13 — Delay-dependent memory experiment and event export

- [x] Implement a separate delayed-cue, four-choice experimental task with distractor tokens and train-only short delays.
- [x] Quantify retained-cue, reactive and last-token-overwrite ablations across seeds, plus longer held-out delay distributions.
- [x] Versioned, mode/seed-bound SQLite memory-policy checkpoints with deterministic resume and evaluation immutability tests.
- [x] Deterministic replay of decision traces and recomputed-hash tampering checks.
- [x] Experimental strict, bounded event ledger output from both simulation families with hash chaining and source-trace binding.
- [ ] **Learned memory control is not implemented.** `retain` hard-codes which initial cue to keep; the association mapping alone is learned.
- [ ] **D2 remains open:** no implemented external AthenZ/Synveil service adapter, authenticated IPC or production stability guarantee.
- [ ] **D3 remains open:** no demonstrated generalization to new open-ended tasks or changing observation semantics. Test seeds were inspected during development.

Next: train a controller to *select* useful observations for memory rather than taking the preselected cue, then test it under unseen distractor processes; tackle navigation without supplied target-direction cues. Maintain reproducible, independent blind evaluation after architecture freeze.

## Learned selective-memory milestone — 2026-10-13

- [x] Added a learnable `write`/`keep` policy conditioned on current context
      and source of the observed signal, with no explicitly labeled cue phase.
- [x] One-slot memory, distractors, hidden response association and terminal
      success feedback; no privileged environment access.
- [x] Disjoint train/test namespaces, short/long delay ablations, saved
      per-seed results and hand-coded simulator oracle comparison.
- [x] Seed/mode/schema-bound SQLite checkpoints; exact continuation and
      read-only evaluation regression tests.
- [x] Trace replay validation of in-simulator observations and memory writes;
      trace hashes alone are not attestations.
- [ ] Source-reliability distribution shift, multiple competing same-channel
      cues, learned recurrent memory and transfer to occluded navigation.
- [ ] D2 stable external service interface still open; D3 broad task transfer
      remains unproven, and all reported seeds are development seeds.


## Occluded spatial-navigation milestone — 2026-10-13

- [x] Added randomized-grid navigation where a goal offset is visible at reset
      only, and future observations include just local blocked directions.
- [x] Engineered movement-feedback dead reckoning and a distinct reactive
      memory-loss ablation; train separate Q policies per mode.
- [x] Three-seed evaluation with untrained, reactive, random, greedy and
      privileged BFS oracle comparisons; all seeds remain development seeds.
- [x] Restart-exact SQLite policy checkpoints, read-only evaluations,
      environmental trace verification and read-only ledger export.
- [ ] **Learned spatial-memory control remains open:** the agent does not learn
      its odometry or what information to keep. It only learns actions from the
      manually constructed memory state.
- [ ] **D3 remains open:** test noisy action feedback, multiple competing
      beacons, harder obstacle distributions, and completely held-out task
      families before claiming transferable spatial reasoning.
