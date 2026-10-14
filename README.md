# Developmental AI

A local-first, inspectable **developmental learning research platform**. Its long-term role is the adaptive learning subsystem of AthenZ, with a planned integration into Synveil. It is **not** a copied fruit-fly brain, conscious entity, human mind upload, or human-level artificial intelligence.

**Target program date:** February 9, 2029. The target is a functioning, continuously learning, independent digital agent modeled on a consenting person's *documented* experiences and choices. Personal identity data belong in the protected AthenZ profile, **not in this repository**.

## Implemented now

1. `developmental_ai.organism`: original 6×6 proof of concept, with five actions, food, hazards, intrinsic novelty, SQLite episodic events, semantic landmarks and saved Q-values. Works on Python standard library alone.
2. `developmental_ai.transfer`: randomized **5–8 cell** square worlds with changing start, food target and obstructed cells. The learner sees only a clipped target-direction cue and four adjacent blocked-direction bits, never the whole map. It learns one reusable tabular policy across procedurally generated environments.
3. **Held-out evaluation**: deterministic SHA-256-derived, disjoint `train` and `test` episode namespaces, seeded action choice, no learning or visit mutations during evaluation, and durable Q-value/visit checkpoints in SQLite.
4. Automated tests for the original prototype and for layout reachability, feature observation, disjoint splits, learning improvement, evaluation read-only behavior, seed binding and restart persistence.

**Experimental results (3 independent seeds, 5,000 training episodes per seed, 300 held-out test layouts per seed):**

| Seed | Untrained success | Trained success | Mean steps untrained → trained |
| --- | ---: | ---: | ---: |
| 17 | 20.33% | 76.00% | 81.69 → 28.55 |
| 23 | 19.00% | 69.00% | 78.42 → 32.91 |
| 41 | 15.67% | 66.67% | 83.66 → 34.30 |

See [`benchmarks/latest_results.json`](benchmarks/latest_results.json) for exact output and rerun instructions. This shows **transfer between unseen layouts within the same narrow world generator and observation model**. It does *not* show open-world generalization or independent goal invention. Benchmark seeds were inspected during development; these results should be treated as development-set evidence until a frozen protocol is evaluated with fresh unseen seeds.

## Quick start

Python 3.10+; no external dependencies.

```sh
python -m unittest discover -s tests -v

# Original fixed-world learner (private SQLite created locally)
python -m developmental_ai.organism evaluate --episodes 200 --db brain.db
python -m developmental_ai.organism train --episodes 3000 --db brain.db
python -m developmental_ai.organism watch --goal 1 --db brain.db
python -m developmental_ai.organism remember --db brain.db

# New randomized-world transfer learner
python -m developmental_ai.transfer evaluate --episodes 200 --db transfer_brain.db
python -m developmental_ai.transfer train --episodes 5000 --db transfer_brain.db
python -m developmental_ai.transfer evaluate --episodes 300 --split test --db transfer_brain.db

# Reproducible fresh-database, multi-seed measurement
python -m benchmarks.transfer_benchmark --seeds 17 23 41 --train-episodes 5000 --test-episodes 300
```

Run commands from the repository root. `train` persists state under the specified DB; `evaluate` never changes policy weights or the agent's visit counts. This prototype uses no GPU, cloud services, or external accounts.

## Design and development

- [`ROADMAP.md`](ROADMAP.md): gates from initial generalization through 2029 integration.
- [`docs/INTEGRATION_CONTRACT.md`](docs/INTEGRATION_CONTRACT.md): future AthenZ/Synveil event boundaries and privacy requirements. **Specification only**; not implemented in code.
- [`docs/PROTOTYPE.md`](docs/PROTOTYPE.md): historical original demo design (old CLI paths may differ).
- [`docs/ORIGINAL_RESULTS.md`](docs/ORIGINAL_RESULTS.md): historical fixed-world run, not a cross-layout generalization result.
- [`AGENTS.md`](AGENTS.md): contribution and verification rules.

Project principles: locally owned data; observable, falsifiable learning claims; no privileged agent executor; source-of-truth in Git for code only; restart-safe checkpoints; train/test separation; and explicit versioning of any future learned-model promotion.

## Multi-task transfer and replay (experimental `curriculum-v1`)

The new experiment shares one local observation and tabular Q policy across
three task rules: `reach`, `collect`, and `courier`. In the courier task the
simulator explicitly changes the direction-to-target cue after pickup. This
is limited transfer, not independent planning.

```sh
python -m developmental_ai.curriculum train --db curriculum_brain.db --seed 13 --episodes 3500 --tasks collect
python -m developmental_ai.curriculum evaluate --db curriculum_brain.db --seed 13 --task courier --episodes 150
python -m benchmarks.curriculum_benchmark --seeds 13 29 47 --train-episodes 3500 --test-episodes 150
python -m developmental_ai.curriculum trace --task courier --policy oracle --index 0 > simulated_trace.json
python -m developmental_ai.curriculum verify --trace-file simulated_trace.json
```

Seed-bound, versioned SQLite checkpoints refuse resumes with different task
curricula; each completed training batch persists atomically. Deterministic
transition replay checks simulations against seeded procedural layouts. The
checksum is not an execution attestation or authority to act externally.

See [multi-task design](docs/CURRICULUM.md) and [full development results](benchmarks/curriculum_results.json),
including random, greedy, and shortest-path oracle baselines. The learned
policy **performs worse than the hand-written greedy baseline**. All seeds
were inspected during development, so independent blind validation remains.

## Delayed-cue memory and bounded simulation event export (experimental)

`developmental_ai.delayed_choice` adds a **different toy task family**: at the beginning of an episode an arbitrary cue appears, then disappears for several steps while distracting signals appear. The learner must make one of four choices after the delay. The successful `retain` mode uses an explicitly programmed memory gate; a memoryless ablation cannot access the original cue at decision time. It learns a cue-to-action association, **not its own memory architecture**.

```sh
python -m benchmarks.delayed_choice_benchmark --seeds 11 31 73 --train-episodes 800 --test-episodes 400
python -m developmental_ai.delayed_choice train --mode retain --episodes 800 --db delayed_brain.db
python -m developmental_ai.delayed_choice evaluate --mode retain --band long --episodes 400 --db delayed_brain.db
python -m developmental_ai.delayed_choice trace --mode retain --index 3 --db delayed_brain.db > delay_trace.json
python -m developmental_ai.event_ledger export --trace-file delay_trace.json > events.json
python -m developmental_ai.event_ledger verify --ledger-file events.json --trace-file delay_trace.json
```

Across development seeds 11/31/73, the retained-cue policy achieves **100%** on an unseen 10–20-distraction test; reactive policies average **22.08%**, close to the 25% chance level. This establishes memory dependence **only on this intentionally simple task**. See [protocol, all ablations, and explicit caveats](docs/DELAYED_CHOICE.md), and [exact machine-readable results](benchmarks/delayed_choice_results.json).

The event-ledger exporter also turns reproducible simulation traces (from `curriculum` or `delayed_choice`) into a bounded, chained, versioned stream that future AthenZ/Synveil adapters can consume. It currently **does not send events to either project**, authenticate their origin, or authorize execution. See [event-ledger contract](docs/EVENT_LEDGER.md). These experiments are in addition to the original transfer and curriculum baselines; they do not supersede historical scores.

## Learned selective memory (`selective-memory-v1`, experimental)

An additional one-slot memory experiment no longer labels the relevant signal
as a `cue`. It presents shuffled informative and distractor channel signals;
the agent uses outcome feedback to learn which channel to retain for a given
context and learns an arbitrary four-button association. Explicit first/last/
random-memory ablations and a simulator oracle provide reference baselines.
**The context/channel features are engineered and relevance is stationary; this
is a small learned memory gate, not general memory, independent reasoning, or
an evolving personal twin.**

```bash
python -m developmental_ai.selective_memory train --db selection.db --episodes 6000
python -m developmental_ai.selective_memory evaluate --db selection.db --episodes 400 --band long
python -m benchmarks.selective_memory_benchmark --seeds 11 31 73 --train-episodes 6000 --test-episodes 400
```

All three inspected development seeds reached 100% test/long accuracy after
6,000 episodes, compared with 27–33% for the first, last, and random memory
update ablations. The oracle is deliberately 100% even before training. See
[`docs/SELECTIVE_MEMORY.md`](docs/SELECTIVE_MEMORY.md) and the complete
[`benchmarks/selective_memory_results.json`](benchmarks/selective_memory_results.json).

This milestone also adds restart-equivalence, checkpoint compatibility,
evaluation immutability, and independently replayable memory-write traces.


## Hidden-target spatial memory (`occluded-navigation-v1`, experimental)

A separate randomized-grid experiment reveals the target displacement **once**,
then removes it from all later observations. The policy must navigate using a
stored goal estimate updated from successful and blocked moves. Memory retention
and odometry are **engineered mechanisms**; only the local navigation policy is
learned. A separately trained `reactive` policy loses the clue after one action.

```bash
python -m benchmarks.occluded_navigation_benchmark --seeds 7 23 41 --train-episodes 3000 --test-episodes 200
python -m developmental_ai.occluded_navigation train --seed 7 --mode memory --episodes 3000 --db private-nav.db
python -m developmental_ai.occluded_navigation evaluate --seed 7 --mode memory --episodes 200 --db private-nav.db
python -m developmental_ai.occluded_navigation trace --seed 7 --mode memory --policy oracle --db private-nav.db > nav-trace.json
python -m developmental_ai.occluded_navigation verify --trace-file nav-trace.json
python -m developmental_ai.event_ledger export --trace-file nav-trace.json > nav-events.json
python -m developmental_ai.event_ledger verify --ledger-file nav-events.json --trace-file nav-trace.json
```

Across inspected development seeds 7/23/41, the learned memory policy succeeds
on 71.5% of 200 held-out-layout episodes per seed on average, compared with
17.3% for the untrained policy, 0% for a separately trained reactive policy,
19.7% for random exploration, 93.3% for an engineered memory-enabled greedy
heuristic, and 100% for a privileged full-map BFS oracle. This is **not** blind
cross-distribution validation, learned memory design, or world-model planning.
Exact per-seed figures and limitations are in
[`docs/OCCLUDED_NAVIGATION.md`](docs/OCCLUDED_NAVIGATION.md) and
[`benchmarks/occluded_navigation_results.json`](benchmarks/occluded_navigation_results.json).
The simulation-only ledger can now export independently replayable traces from
this third family too; no live AthenZ or Synveil integration is implied.


## Environment dynamics adaptation (`adaptive-dynamics/v1`, experimental)

A new calibration experiment **fits empirical movement, odometry and landmark
probabilities** from supervised simulator instrumentation instead of assuming
correct physics parameters. It adapts from standard motion/fixed landmarks to
higher-noise motion/shifted landmarks, using a Bayesian belief filter with a
hand-coded navigation heuristic. The privileged calibration instrument knows
actual movements and positions; ordinary navigation does **not**. No neural
world-model learning or uninstrumented self-discovery is claimed.

Across inspected development seeds 17/23/41, a frozen standard-world model
navigates the changed world successfully in 16.7% of held-out episodes versus
53.4% after adaptation; a privileged probability oracle reaches about 57.8%.
Prediction negative log likelihood improves from 3.433 to 2.268. But adaptation
also harms original-world navigation (86.9% to 13.1%): **catastrophic forgetting**.
Immutable named snapshots recover the original 86.9% performance when explicitly
selected; choosing the appropriate snapshot automatically remains future work.

```bash
python -m benchmarks.adaptive_dynamics_benchmark --seeds 17 23 41 --calibration-samples 1800 --test-episodes 300
python -m developmental_ai.adaptive_dynamics train --db calibration.db --samples 1800
python -m developmental_ai.adaptive_dynamics snapshot --db calibration.db --name original
python -m developmental_ai.adaptive_dynamics train --db calibration.db --samples 1800 --noise high --layout shifted
python -m developmental_ai.adaptive_dynamics evaluate --db calibration.db --samples 300 --noise high --layout shifted
python -m developmental_ai.adaptive_dynamics evaluate-snapshot --db calibration.db --name original --samples 300 --noise standard --layout fixed
```

See [model, evaluation protocol and per-seed limitations](docs/ADAPTIVE_DYNAMICS.md),
[`benchmarks/adaptive_dynamics_results.json`](benchmarks/adaptive_dynamics_results.json),
and regression tests. These seeds were inspected during development, not blind.


## Self-supervised dynamics and automatic model retrieval (`online-dynamics/v1`, experimental)

`developmental_ai.online_dynamics` fits categorical motion, odometry, and
landmark probabilities from ordinary action/sensor sequences using latent-state
forward-backward inference. **Unlike the earlier privileged calibration
experiment, fitting sees no actual post-action position or displacement.**
An ordinary reset beacon provides the initial position, and the ring topology
and sensor vocabulary remain hand-specified. The stored model bank can select
which previously trained model best explains new sequences **without being given
a regime label**.

```sh
python -m benchmarks.online_dynamics_benchmark --seeds 17 23 41 --train-episodes 350 --train-steps 12 --iterations 10 --probe-episodes 50 --navigation-episodes 100
python -m developmental_ai.online_dynamics train --db model-bank.db --name original --noise standard --layout fixed --episodes 350
python -m developmental_ai.online_dynamics train --db model-bank.db --name changed --noise high --layout shifted --episodes 350
python -m developmental_ai.online_dynamics select --db model-bank.db --noise high --layout shifted --episodes 50
```

The CLI `noise` and `layout` flags configure the **simulator only**, not the
learner. Two synthetic regimes and three inspected development seeds are
reported in [`benchmarks/online_dynamics_results.json`](benchmarks/online_dynamics_results.json).
A separate post-development audit on seeds 101/303/707 is recorded in
[`benchmarks/online_dynamics_audit_results.json`](benchmarks/online_dynamics_audit_results.json).
The model bank selects the correct regime in all tested comparisons, but
shifted/high-noise navigation averages **33.3% in the audit**, compared with
**58.0% for the privileged physics oracle**. The gap remains unsolved.
See [`docs/ONLINE_DYNAMICS.md`](docs/ONLINE_DYNAMICS.md) for evaluation boundaries,
regression checks and known limitations. This is batch model fitting with
probe-based retrieval, **not** live continual learning or discovered physics.

## Continuous model selection from changing observation streams (`continuous-dynamics/v1`)

The new `StreamMonitor` chooses among **previously trained** latent-state dynamics
models as the simulation changes, using only short histories of ordinary movement
commands, odometry and intermittent landmark observations. It requires repeated
likelihood evidence, preserves earlier models, and stores restart-safe, hash-linked
simulation event records. `unknown`/`uncertain` are not permissions to act.

```sh
python -m benchmarks.continuous_dynamics_benchmark --seeds 17 23 41
python -m benchmarks.continuous_dynamics_benchmark --seeds 1009 1013 1031
python -m unittest discover -s tests -v
```

Three development seeds identified the changed environment within four
12-step observation episodes and retrieved the original environment model within
three or four episodes of its return. Three additional inspected seeds succeeded
with the full model-training budget, but **two of those three failed at a lower
training budget**. The monitor learns no new model itself, runs per episode, and
has no AthenZ/Synveil service integration or authority to execute real actions.
See [full results, low-budget failures and caveats](docs/CONTINUOUS_DYNAMICS.md),
[`benchmarks/continuous_dynamics_results.json`](benchmarks/continuous_dynamics_results.json)
and [`benchmarks/continuous_dynamics_audit_results.json`](benchmarks/continuous_dynamics_audit_results.json).

## Per-observation detection and candidate quarantine (`step-dynamics/v1`, experimental)

`developmental_ai.step_dynamics` adds a restart-safe per-sensor-step Bayesian
forward filter and a **review-only candidate model store**. It estimates
observation likelihoods from ordinary action/odometry/landmark records,
can identify previously saved dynamics, and can fit a *separate* candidate
from unfamiliar observation histories. Candidates **cannot change the bank
without a separately passed immutable held-out predictive review AND an explicit
review-digest-matched approval call**, and the monitor is then
invalidated until a new reviewed session is opened.

This is **not** reliable change detection or automated new-environment
learning yet. In the three-seed development benchmark, per-step changed-regime
recognition fails entirely on seeds 23 and 41; two of three quarantined
candidates have worse held-out predictive loss than the best existing model.
See [`docs/STEP_DYNAMICS.md`](docs/STEP_DYNAMICS.md) and
[`benchmarks/step_dynamics_results.json`](benchmarks/step_dynamics_results.json).

```bash
python -m unittest discover -s tests -v
python -m benchmarks.step_dynamics_benchmark --seeds 17 23 41
```


## Offline-calibrated stepwise regime detection (`calibrated-step/v1`, experimental)

A **separate** offline calibration step derives a detector margin from distinct,
regime-labelled calibration histories (`train` indices 5000+). At runtime the
step-by-step detector still uses ordinary action/odometry/landmark observations
**without** labels. The old `margin=0.12` detector remains unchanged as a
baseline. Calibration artifacts bind a model-bank fingerprint and have a simple
integrity digest, not authenticated provenance or trustworthy confidence values.

```sh
python -m benchmarks.calibrated_step_benchmark --seeds 17 23 41
python -m benchmarks.calibrated_step_benchmark --seeds 1009 1013 1031
```

In the initial three development seeds, changed-world correct-model step
selection rose **26.4% → 47.9%**; in three additional inspected audit seeds,
**61.1% → 65.3%**. One initial seed regressed, and the three-seed changed-world
wrong-model rate remains **52.1%**. This is a bounded improvement, **not safe or
reliable autonomous adaptation**. The existing step detector and candidate
promotion pathway were not modified in this experiment. Details and full
per-seed errors: [`docs/CALIBRATED_DETECTION.md`](docs/CALIBRATED_DETECTION.md),
[`benchmarks/calibrated_step_results.json`](benchmarks/calibrated_step_results.json)
and [`benchmarks/calibrated_step_audit_results.json`](benchmarks/calibrated_step_audit_results.json).

## Conservative abstention gate (`decision-abstention/v1`)

A separate post-selection safety filter now **withholds a regime decision** when the `StepDetector`'s selected model is inconsistent with its current model-likelihood evidence. Offline, labelled `train` histories (disjoint from model fitting) select a heuristic minimum likelihood gap, while `test` histories are reserved for evaluation. This is **not** a learned new environment or a statistical confidence guarantee, and the default `StepDetector` behaviour is unchanged.

```sh
python -m benchmarks.abstention_benchmark --seeds 17 23 41 --out benchmarks/abstention_results.json
python -m benchmarks.abstention_benchmark --seeds 1009 1013 1031 --out benchmarks/abstention_audit_results.json
```

Across 1,296 step decisions in each group, wrong selections fell from 336 to **3** on development seeds and 214 to **21** on audit seeds. However, abstentions increased from 56 to **935** and from 66 to **777** respectively: most observations do not receive an answer. See [protocol, exact results and limitations](docs/DECISION_ABSTENTION.md). No model has been automatically changed or promoted; there is no live AthenZ/Synveil integration.


## Independent predictive candidate review (`candidate-review/v1`)

`CandidateStore.review(...)` freezes distinct held-out observations and tests a
proposed model against the **best** existing bank model on the *same* data.
Promotion now requires **both** a positive review and a separate explicit
review-digest approval. This is a code-level gate, **not signed human consent**.
No models are promoted automatically, including those passing evaluation.

```sh
python -m benchmarks.candidate_review_benchmark --seeds 17 23 41 1009 1013 1031
python -m unittest discover -s tests -v
```

In six inspected seeds, a candidate addressing a genuinely missing simulator
regime passed held-out review and a separate, untouched predictive test on all
six; a marginal candidate failed review and separate test on all six. Exact
per-seed results, data-split limitations, and explicit regression notes appear
in [`docs/CANDIDATE_REVIEW.md`](docs/CANDIDATE_REVIEW.md) and
[`benchmarks/candidate_review_results.json`](benchmarks/candidate_review_results.json).
Predictive gain here is **not** a navigation success guarantee; stepwise
change-detection coverage remains low and no live AthenZ/Synveil integration exists.
