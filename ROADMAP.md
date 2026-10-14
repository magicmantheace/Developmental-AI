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


## 2026-10-14 — Supervised world-model calibration and model snapshots

- [x] Estimate unknown simulator movement/odometry/landmark likelihoods from instrumented samples, with train/test generation separated.
- [x] Use a learned likelihood model in a bounded position-belief filter (control decisions remain heuristic).
- [x] Simulate abrupt distribution shift in movement and landmark locations, publish every development seed, evaluate predictive log loss and navigation success against a true-physics oracle.
- [x] Persist versioned model state, verify restart-equivalent training and evaluation immutability.
- [x] Preserve immutable, explicitly named knowledge snapshots so prior regime performance can be recovered without retraining.
- [ ] No learning from ordinary uninstrumented navigation observations yet: calibration sees simulator ground truth. No automatic regime selection or learned action controller in this experiment.
- [ ] The continuously adapted model substantially forgets the old regime; snapshot retention is a **manual mitigation**, not solved continual learning.
- [ ] D2 stable service adapter and D3 broad blind generalization are still open.

Next: calibration from *unlabeled* movement/landmark sequences using latent-state inference, automatic model bank selection from observation sequences, and completely frozen blind tests spanning changed geometry/landmark reliability.


## 2026-10-14 — Learning from unlabeled sensor trajectories

- [x] Introduce a second dynamics learner using only initial beacon, movement
      command, odometry and intermittent landmark observations (no ground-truth
      actual movement or post-reset position during fitting).
- [x] Infer hidden positions by deterministic categorical forward-backward EM
      with observable likelihood metrics and frozen deterministic seeds.
- [x] Preserve distinct immutable model snapshots and select the best fitting
      known model automatically from fresh ordinary probes (no regime labels).
- [x] Compare predicted observations and navigation on each inspected seed to
      wrong-model and privileged true-probability oracle baselines.
- [x] Repeat frozen development protocol once on independent post-development
      audit seeds 101/303/707; record the weaker high-noise outcome unchanged.
- [x] Verify versioned storage, tampering rejection, deterministic resume and
      read-only model selection. Previous supervised calibration remains intact.
- [ ] The selector does not detect unknown regimes or run a changepoint detector
      on a single continuous lived experience; periodic probes are externally
      scheduled. Learning still assumes a known small ring topology.
- [ ] D2 service adapter, broad D3 transfer and genuine continual adaptation
      remain open. Results are development evidence, not humanlike cognition.

## 2026-10-14 — Observation-driven regime change detection

- [x] Immutable model-bank fingerprint and schema-bound restart-safe model selector.
- [x] Rolling per-episode observation-likelihood window and repeated-evidence switch gate, with no regime labels supplied to the selector.
- [x] Retrieval of prior model after environment reverts; bounded hash-linked simulation event history and explicit unknown/uncertain statuses.
- [x] All three original development seeds and three extra checked seeds select original → changed → original when pretrained with the full model-training budget.
- [x] Capture weaker-training failure as a negative result (2/3 seeds fail to switch after the regime change).
- [ ] Current detection is per twelve-step episode, not per observation or during navigation; hand-tuned thresholds and manually pretrained models remain.
- [ ] Novel regime creation and candidate approval, calibrated novelty detection, sample-efficient model fitting, and closed-loop integration are open.
- [ ] The formal D2 external service interface, D3 broad generalization and any claim of human-like memory/agency remain open.

## 2026-10-14 — Per-observation inference and quarantined new-model proposals

- [x] Per-observation latent-state likelihood updates, bounded score windows,
      explicit initial beacons, restart-exact state and durable event history.
- [x] One-step observational likelihood regression against full forward/backward.
- [x] Preserved immutable model catalogue; quarantined training histories and
      candidate checkpoint with explicit digest-matched review requirement.
- [x] Invalid, privileged or tampered observations rejected; snapshot/bank
      fingerprint and schema compatibility checked on restart.
- [x] Published all three inspected-seed outcomes, including **failed changed
      regime detection on two seeds** and weak/worse held-out candidate fits.
- [ ] Not a reliable novelty detector, calibrated selector, real authenticated
      approval, per-step changing simulator, or automatic adaptation system.
- [ ] New-environment model selection and training-data quarantine still need
      leakage-resistant independent audit, more diverse regimes and improved
      predictive quality before any automatic-learning gate can be considered.


## 2026-10-14 — Offline step-detector calibration (experimental)

- [x] Frozen `step-dynamics/v1` baseline retained without changing prior results.
- [x] Separate model-fit, offline calibration, and evaluation episode ranges.
- [x] Fail closed when saved regime models cannot be distinguished using calibration evidence; reject duplicate evidence and bank mismatches.
- [x] Add model-bound, checksum-verified calibration artifacts and deterministic tests.
- [x] Preserve all three development and three additional audit seeds, including a regression and wrong-model fractions.
- [ ] **Reliability gate remains open:** 52.1% wrong-model step selection on changed-world development seeds after calibration. The anomaly floor is not statistically calibrated.
- [ ] Need within-trajectory regime changes, independent blind out-of-family tests, calibrated abstention and held-out candidate review before autonomous adaptation.
