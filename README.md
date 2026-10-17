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

## Optional consecutive-evidence selector (experimental)

`developmental_ai.streak_selection` adds a three-observation leader-consensus
selector, calibrated offline against separate training-namespace examples and
checkpointable across restarts. **It is not the default**: across development
seeds 17/23/41, correct/wrong/abstained outcomes were **346/3/947** versus
**358/3/935** for the existing conservative gate; across extra audit seeds
1009/1013/1031 they were **527/22/747** versus **498/21/777**. This mixed
result **does not justify replacing the conservative rule** or granting any
new autonomy. The learned dynamics models themselves need to improve.

```sh
python -m benchmarks.streak_selection_benchmark --seeds 17 23 41
python -m benchmarks.streak_selection_benchmark --seeds 1009 1013 1031
```

See [`docs/STREAK_SELECTION.md`](docs/STREAK_SELECTION.md) and
[`benchmarks/streak_selection_results.json`](benchmarks/streak_selection_results.json)
for per-seed, per-method details. The 2% calibration error parameter is an
empirical threshold on correlated simulated training steps, not a statistical
safety claim. Tests are local; GitHub Actions are not required.


## Validation-selected multi-start world-model experiment (experimental)

`developmental_ai.robust_world_model` tests whether multiple latent-state EM starting guesses, selected on disjoint **train-namespace** validation histories, yield better observation prediction than the existing single-start learner. This is an **optional** experiment, not a new default or an authorized deployment policy. It uses only initial position beacons, commands, odometry and landmarks; it never sees subsequent true positions or simulator regime labels during fitting/selection.

Across previously inspected development seeds 17/23/41 and audit seeds 1009/1013/1031, both tested regimes showed better held-out mean log-likelihood on **12/12 comparisons**. Navigation was mixed and sometimes **worse**, especially under high noise. Both models already selected the correct regime in all 12 full-episode probe tests, so no selection improvement has been demonstrated. This is development evidence, not an independently blind experiment.

```sh
python -m benchmarks.robust_world_model_benchmark --seeds 17 23 41 --train-episodes 90 --validation-episodes 30 --test-episodes 40 --iterations 6 --starts 3 --navigation-episodes 12
python -m benchmarks.robust_world_model_benchmark --seeds 1009 1013 1031 --train-episodes 90 --validation-episodes 30 --test-episodes 40 --iterations 6 --starts 3 --navigation-episodes 12
```

See [protocol and limitations](docs/ROBUST_WORLD_MODEL.md), [development results](benchmarks/robust_world_model_results.json), and [audit results](benchmarks/robust_world_model_audit_results.json). V2A affective cognition and V2B virtual-home plans remain future milestones; none are implemented here.

## Optional joint spatial/world-model inference (`mixture-navigation/v1`)

A bounded Bayesian filter now maintains a *joint* distribution over position and
which previously saved observation-only world model applies. It does not
receive hidden positions or the current environment label. An optional
observation-only pre-navigation probe biases the starting model probabilities;
fixed wrong/correct saved-model and true-physics references remain benchmarks.
Versioned mid-episode snapshots survive SQLite restart and refuse incompatible
model banks. This is an **experimental alternative**, not the default controller
or evidence of general spatial reasoning, independent physics discovery or new
autonomy. Read [method, protocol and limitations](docs/MIXTURE_NAVIGATION.md)
and [development](benchmarks/mixture_navigation_results.json) /
[audit](benchmarks/mixture_navigation_audit_results.json) per-seed data.

```sh
python -m benchmarks.mixture_navigation_benchmark --seeds 17 23 41 --fit 90 --iterations 6 --probe 40 --navigation 60
python -m unittest discover -s tests -v
```

The six-seed benchmark shows some robustness to a *wrong* saved model, but
no consistent improvement over a correctly selected learned model; changed
world navigation remains as low as 12–21% with mixture variants, compared
with 52–56% for the true-physics oracle. A 90% internal regime-choice
threshold abstained on most changed-world probe episodes. Therefore the
mixture is not promoted to default.

## Supervised spatial posterior calibration (experimental)

The optional `spatial_calibration` experiment temperature-scales an existing learned position posterior to make its **reported uncertainty** more faithful to measured outcomes. Unlike observation-only world-model fitting, temperature fitting **requires simulator ground-truth positions** from a separate, privileged `train/5000+` calibration dataset. Runtime posterior display sees no such labels, and **no navigation action, model choice or permission is changed**.

On six previously inspected seeds, held-out location log-loss improved in all six original-regime comparisons and in three of six noisy changed-regime comparisons; the other three high-noise cases remained unchanged. The changed regime still trails a physics oracle substantially. See [methods and limitations](docs/SPATIAL_CALIBRATION.md), [development results](benchmarks/spatial_calibration_results.json), and [additional inspected-seed results](benchmarks/spatial_calibration_audit_results.json).

```sh
python -m benchmarks.spatial_calibration_benchmark --seeds 17 23 41
python -m benchmarks.spatial_calibration_benchmark --seeds 1009 1013 1031
```

V2A (affective cognition) and V2B (persistent virtual home) remain **planned, post-core** milestones.


## Observation-only structured landmark geometry (experimental)

The optional `developmental_ai.structured_landmarks` learns landmark *locations*
and categorical sensor/motion parameters using only a one-time starting-position
beacon and ordinary movement/odometry/landmark sequences. It is given a strong
**two-distinguishable-landmark ring geometry assumption**, not simulator
post-reset positions or regime labels. It never installs or promotes a model.

On inspected 17/23/41 seeds, high-noise navigation improved from 23.9% with
the unconstrained EM model to 56.1% with the structured model; on inspected
1009/1013/1031 seeds it improved from 13.3% to 55.0%. A newly introduced
landmark offset of 3 yielded 56.1% vs 25.6% on three development seeds.
The original-world performance sometimes regressed, no independent blind
task-family generalization is established, and the default navigation policy
is unchanged.

See [structured landmark experiment](docs/STRUCTURED_LANDMARKS.md),
[development results](benchmarks/structured_landmarks_results.json),
[audit results](benchmarks/structured_landmarks_audit_results.json) and
[unfamiliar offset results](benchmarks/structured_landmark_novelty_results.json).

```sh
python -m unittest discover -s tests -v
python -m benchmarks.structured_landmarks_benchmark --seeds 17 23 41 --train 90 --test 40 --iterations 6 --navigation 60
python -m benchmarks.structured_landmark_novelty_benchmark --seeds 17 23 41 --offset 3 --train 90 --iterations 6 --test 40 --navigation 60
```

## Experimental flexible landmark geometry (not the default)

`developmental_ai.flexible_landmarks` fits zero, one or two distinguishable landmark sites at independent ring positions using ordinary action, odometry and marker histories. It retains fixed 9/11-cell topology, a one-time initial beacon and engineered sensor symbols. The simulator harness still groups fitting histories by condition.

Compared with the unchanged half-spacing model, **unfamiliar unequal-spacing high-noise** navigation improved from **31.1% to 41.1%** (development seeds 17/23/41) and **32.2% to 54.4%** (inspected audit seeds 1009/1013/1031). The flexible model **regressed** in existing half-spacing and one/no-landmark conditions; it is not promoted. Detailed per-seed maps, log likelihood and navigation baselines: [flexible map protocol and limitations](docs/FLEXIBLE_LANDMARKS.md), [development data](benchmarks/flexible_landmarks_results.json), [audit data](benchmarks/flexible_landmarks_audit_results.json). The seed groups have been inspected and are not blind. Run `python -m benchmarks.flexible_landmarks_benchmark` for reproduction.

## Experimental discovery of models from mixed, unlabelled experiences

`developmental_ai.mixed_experience` can fit a one-model baseline and an optional two-model proposal from the **same unsorted collection of ordinary (command, odometry, landmark) observations**. No simulator regime labels, post-reset hidden positions or rewards reach fitting. The proposal uses observation-only clustering and latent-state EM, separate train-namespace validation, and read-only model choice on fresh unlabelled contextual probes. It **cannot authorize promotion or external actions**, and remains experimental.

With 72 mixed fit episodes, 24 separate training-namespace validation episodes, three EM iterations, two reassignments, and 24 navigation trials per seed/regime, changed high-noise navigation rose **15.3% → 48.6%** (development seeds 17/23/41) and **15.3% → 44.4%** (previously inspected audit seeds 1009/1013/1031), with slight original-world navigation regressions. All three original-only negative-control seeds rejected unnecessary model splitting. These are small, previously inspected synthetic evaluations, **not blind generalization**.

```sh
python -m benchmarks.mixed_experience_benchmark --seeds 17 23 41 --out benchmarks/mixed_experience_results.json
python -m benchmarks.mixed_experience_benchmark --seeds 1009 1013 1031 --out benchmarks/mixed_experience_audit_results.json
python -m benchmarks.mixed_experience_benchmark --seeds 17 23 41 --schedule original_only --out benchmarks/mixed_experience_control_results.json
```

See [protocol, full results and limitations](docs/MIXED_EXPERIENCE.md). Default policies and existing candidate-approval gates remain unchanged. V2A affect and V2B virtual-home milestones remain future work.

## Within-episode model switching (optional research)

`developmental_ai.switching_belief` now retains a joint posterior over location and the identity of **previously discovered, immutable** world-model hypotheses, and permits a train-calibrated transition prior between them after each observation. The fit, hazard-selection and evaluation histories remain disjoint. A checksum-checked, model-bank-bound hazard receipt and restart-equivalent SQLite state are supported.

In six previously inspected seeds, train-calibrated switching improved changing-world sensor log-loss and spatial Brier score on four seeds and tied two, **but worsened some stationary-world results and greatly increased uncertainty-based abstention**. It is not the default, does not discover new models at runtime or authorize any deployment. See [protocol and full per-seed results](docs/SWITCHING_BELIEF.md), [development results](benchmarks/switching_belief_results.json), and [additional audit results](benchmarks/switching_belief_audit_results.json). Local targeted tests passed; a full reconstructed-suite run exceeded its time limit. The unchanged transfer benchmark still gives 76.0%, 69.0%, and 66.67% for seeds 17/23/41.

## Closed-loop navigation with live model uncertainty (experimental)

The new `developmental_ai.closed_loop_adaptation` connects previously discovered
mixed-environment model hypotheses with a model-bound train-calibrated switching
hazard and real *in-simulator* left/right/collect navigation decisions. It
records ordinary action/sensor evidence, rejects hidden regime/position fields,
restores checkpoints by replaying the evidence, and has **no external tools,
automatic learning, or authority to promote a model**.

Changing-world navigation was **62.5% switching vs 68.1% static mixture** on
development seeds 17/23/41 and **79.2% vs 63.9%** on previously inspected audit
seeds 1009/1013/1031, with 72 episodes per method and cohort. On continuously
high noise switching regressed in *both* cohorts. The old navigator remains
default; results are not blind. See
[closed-loop protocol and per-seed failures](docs/CLOSED_LOOP_ADAPTATION.md).

```sh
python -m unittest discover -s tests -p test_closed_loop_adaptation.py -v
python -m benchmarks.closed_loop_adaptation_benchmark --seeds 17 23 41
python -m benchmarks.closed_loop_adaptation_benchmark --seeds 1009 1013 1031
```


## Optional sensor novelty guard (experimental)

`developmental_ai.novelty_guard` monitors whether bounded action/odometry/landmark histories are poorly explained by the previously learned structured world-model bank. A model/hazard-bound **train-only** upper-tail surprise receipt provides a diagnostic; optional `GuardedNavigation` stops suggesting actions once unfamiliar evidence triggers a latch. It cannot create models or authorize tools or OS operations. Across six *previously inspected*, not blind seeds, the benchmark flagged **144/144** simulated stuck-landmark episodes, but only **44/144** stuck-odometry and **48/144** altered-map episodes; false alarms were **8/144** normal and **10/144** known-transition streams. Closed-loop stopping slightly reduced normal-world task success (**105/144 → 101/144**). It remains **off by default**. See [research details and limitations](docs/NOVELTY_GUARD.md) and [benchmark code](benchmarks/novelty_guard_benchmark.py).

## Optional sensor-channel novelty checks (experimental)

The optional `developmental_ai.channel_novelty` detector complements, but does not modify, the older model-surprise guard. It monitors long runs of zero odometry while moving and long runs of a repeated non-null landmark reading. An optional `LayeredNavigation` wrapper pauses further simulated action suggestions if either detector alarms, without choosing replacement actions. Restart is validated by replay. No model promotion, tool authorization or default-policy changes.

On six previously inspected seeds with 144 episodes per condition, stuck-odometry alarms improved from **44/144 to 144/144**; stuck-landmark detection stayed at 144/144. Rotated-layout detection remained weak (49/144). Normal false alarms increased from 8/144 to 10/144; known-shift false alarms from 10/144 to 12/144. The OR of two separately calibrated checks has no joint 10% false-alarm guarantee.

On 144 closed-loop stuck-odometry episodes, the layered wrapper paused 115 sessions versus 36 previously, reducing completed tasks from 37 to 21. Normal-world guarded completion stayed 101/144 for both variants. This is an experimental diagnostic trade-off, not improved goal success.

Reproduce with `python -m unittest tests.test_channel_novelty tests.test_novelty_guard -v` and `python -m benchmarks.channel_novelty_benchmark --seeds 17 23 41` (then with `--seeds 1009 1013 1031`). See [research results](docs/CHANNEL_NOVELTY.md). Versions 2A and 2B remain post-core roadmap milestones.


## Experimental counterfactual layout-novelty diagnostic (`layout-novelty/v1`)

An optional, simulation-only monitor scores whether **alternative landmark-map offsets** explain ordinary action/odometry/marker observations better than the existing frozen world-model bank. The complete offset-and-prefix search is calibrated against separate training-namespace normal and known-shift histories. **It is not the default; it does not pause, control actions or promote models.**

On previously inspected seeds (144 rotated-layout trials), the existing two-layer guard detects 49; adding the alpha=.10 map diagnostic detects **92**, but normal false alarms rise **10→22/144** and known-shift false alarms **12→23/144**. The expressly **post-result exploratory** stricter alpha=.04 setting detects **67/144**, with normal alarms **13/144** and known-shift alarms **14/144**. No setting is approved for rollout. Full per-seed results and reproduction: [docs/LAYOUT_NOVELTY.md](docs/LAYOUT_NOVELTY.md), [development benchmark](benchmarks/layout_novelty_results.json), [audit benchmark](benchmarks/layout_novelty_audit_results.json), and the two strict variants. Versions 2A and 2B remain post-core milestones.

## Cross-family D1/D2 environment interface (experimental, 2026-10-15)

`developmental_ai.environment_api` now provides one versioned, headless observe/act/checkpoint/replay contract for **grid navigation, occluded navigation, and delayed-choice memory**. `python -m developmental_ai.environment_service` starts a bounded JSON-lines service with action masks and stale-tick validation. It cannot execute shell/network/system actions. This is an unauthenticated **local prototype**, not production AthenZ/Synveil integration.

The [cross-family benchmark](benchmarks/environment_contract_benchmark.py) uses [a fixed protocol manifest](benchmarks/frozen_environment_protocol.json) and binds results to its SHA-256 checksum. In 48 development trials per family, family-specific policies succeeded 43/48 (grid), 45/48 (occluded), and 48/48 (delayed), compared with seeded random 6/48, 6/48 and 10/48. The delayed-choice association was trained using separate short-delay reward feedback; navigation heuristics and cue retention are engineered. These results **do not show that a single learned policy transfers skills across task families**, or that independent blind evaluation is complete.

[Protocol and limitations](docs/ENVIRONMENT_PROTOCOL.md). Run `python -m unittest tests.test_environment_api tests.test_environment_contract_benchmark -v`, `python -m benchmarks.environment_contract_benchmark`, and the original `python -m benchmarks.transfer_benchmark`. Existing model defaults, V2A and V2B plans remain unchanged.

## D3 zero-shot grid-to-occluded transfer study (exploratory)

A tabular Q policy trained **only** on visible-target grid episodes was reused without updating its weights in an occluded-goal environment through the new public environment adapter. The occluded observation requires an **engineered dead-reckoning memory encoder**; no learned perceptual transfer or general cognition is claimed.

On three previously inspected development seeds (192 trials per family), the frozen grid-trained policy succeeded on **142/192 occluded episodes**, against **34/192 random** and **178/192 engineered greedy**. Grid test outcomes were 136/192 trained, 32/192 random, 175/192 greedy. The transfer is real reuse of policy weights on a related family, but trails strong task-specific heuristics, is not independently blind and does not close D3.

Run `python -m unittest tests.test_cross_family_transfer -v` and `python -m benchmarks.zero_shot_navigation_transfer_benchmark`. See [study and limitations](docs/ZERO_SHOT_TRANSFER.md). No default behavior, consent boundaries, V2A or V2B plans were changed.


## Learned grid-to-occluded memory updates (D3 exploratory)

`developmental_ai.learned_spatial_memory` learns action/outcome-dependent changes in remembered target offset **from public visible-grid training observations**, then reuses them with a frozen grid-trained policy in occluded navigation. The learned updater matches engineered memory: **133/192** successes on development seeds and **124/192** on additional seeds, while a cue-forgetting ablation gets **0/192** in both cohorts. The initial cue write, feature representation and event normalization are still engineered, so this is *not* general learned attention or completion of D3. Details: [protocol and limitations](docs/LEARNED_MEMORY_TRANSFER.md). Versions 2A and 2B remain post-core and unchanged.

## Cross-task retention choice from reward (experimental D3)

`developmental_ai.cross_task_retention` trains two fixed one-slot retention
hypotheses (keep the initial cue or overwrite with the latest distractor) and
a response mapping using **only ordinary D2 delayed-choice observations and
terminal feedback**. A separate train-namespace validation partition selects
one hypothesis. The selected retention choice is then reused without reward
retraining in occluded navigation alongside the existing separately learned
spatial updater. This is **strategy selection**, not general learned attention:
candidate rules, cue semantics, memory slots, navigation heuristic and cross-task
mapping remain engineered.

With six inspected seeds (40 test episodes per seed), learned retention matched
the engineered initial-cue control: **240/240** long-delay choices and
**225/240** occluded navigation successes, versus **59/240** for the
latest-cue delayed control and **0/240** for forgotten-cue navigation. These
are non-blind simulated development results; no learned general-purpose memory
policy or D3 completion is claimed. Existing defaults are unchanged. See
[protocol and per-seed results](docs/CROSS_TASK_RETENTION.md).

```sh
python -m unittest tests.test_cross_task_retention -v
python -m benchmarks.cross_task_retention_benchmark --seeds 2749 6607 9901
python -m benchmarks.cross_task_retention_benchmark --seeds 17431 24869 37021
```

## Per-observation reward-learned memory gate (optional D3 research)

`developmental_ai.online_memory_gate` adds a bounded one-slot WRITE/KEEP decision for each incoming source-labeled observation, learned from simulated terminal reward. A model-bound `CueMemory` snapshot is checked by exact decision-history replay. After training on competing-signal episodes, the gate selects between synthetic target cues for the public D2 occluded-navigation simulator. Six *inspected, nonblind* seeds gave **240/240** source-task successes and **217/240** occluded navigation completions, matching an engineered correct-channel selector and outperforming first/last/random choices. This is **not** general attention, natural language memory, independently blind transfer, or completed D3: finite channels/context, task translation, target cue generation, and the navigation heuristic are manually supplied. Existing defaults are unchanged. See [research notes and reproduction](docs/ONLINE_MEMORY_GATE.md). D1, production D2, D3 and V2A/V2B roadmap gates remain open.\n
## Experimental paired-cue grounding across renamed environments

`developmental_ai.grounded_aliases` uses **train-only paired PUBLIC target cues** to align unfamiliar source names/context strings to previously learned write/keep roles; evaluation gets only cue candidates and a context, never the public calibration reference. In six inspected seeds, the calibrated adapter completed **223/240** occluded-navigation episodes. A simpler *paired-source lookup without the old memory model* completed **the same 223/240**; there is **no measured transfer advantage** from the gate. Always-first/last/random cues completed 43/240, 51/240 and 42/240, respectively. The alias mapping, cue generation and exact-offset calibration are engineered assumptions, **not zero-shot generalization**. Evaluation seeds have been inspected and the study is not blind. This remains off by default; see [protocol and limitations](docs/GROUNDED_ALIASES.md). D1 and D3 remain open; V2A/V2B ordering is unchanged.

## Reward-only target-domain cue grounding (D3 experimental)

`developmental_ai.reward_aliases` now learns reliable unfamiliar cue sources from **terminal simulated navigation rewards only**, without paired reference cues supplied to its model API. The evaluation protocol was committed before testing (`benchmarks/reward_only_alignment_protocol.json`). In six previously inspected seeds, the reward-only contextual selector achieved **217/240** navigation successes, versus **97/240** with context omitted, and exactly **217/240** for a plain context/source lookup using the same rewards. This is useful target-domain adaptation but **not** a demonstrated advantage over lookup, zero-shot semantics, independent blind D3 evidence, or default model promotion. See [protocol and complete limitations](docs/REWARD_ONLY_ALIGNMENT.md). V2A and V2B remain post-core.


## D3: reward-only dynamic cue reliability (optional, 2026-10-16)

`developmental_ai.dynamic_reliability` learns from *terminal simulated task rewards* to choose among five source cues whose reliability changes **every episode**. It compares each candidate's eight public forecasts against eight observed probes; the four agreement bins are engineered, not autonomously discovered. On development seeds the learned selector completed **102/120** navigation tasks versus **27/120** for fixed source lookup, **106/120** for hand-coded maximum agreement, and **111/120** for the correct-cue reference. On protocol-reserved seeds (executed without changing model settings) those results were **104/120**, **13/120**, **103/120**, and **110/120** respectively. Across both cohorts it does **not beat** the maximum-agreement heuristic (206/240 vs 209/240). This is not independent blind generalization or completed D3. The pre-evaluation [frozen protocol](benchmarks/dynamic_reliability_protocol.json), [full results and caveats](docs/DYNAMIC_RELIABILITY.md), and [benchmark](benchmarks/dynamic_reliability_benchmark.py) are reproducible. No default-policy or permission changes.

## Reward-only raw-token alignment (optional D3 research)

`developmental_ai.raw_token_transfer` learns a positive-vs-negative raw-symbol pair score from 360 training navigation outcomes and public, aligned eight-token observations; forecasts use a disjoint alphabet with an unknown seed-specific symbol permutation. Across six inspected seeds, it completed **203/240** tasks versus **45/240** for a source-identity bandit, but a simpler **unsupervised cooccurrence alignment completed 208/240** and exactly recovered the permutation in all six seeds. Slot alignment, synthetic forecasts, four-symbol vocabularies and navigator remain engineered. This is not blind task-family generalization or D3 completion. The model is optional and never authorizes real actions. Reproduce with `python -m benchmarks.raw_token_transfer_benchmark --cohort development`, then `--cohort additional`; see [research details](docs/RAW_TOKEN_TRANSFER.md).

## Unaligned symbolic sequence inference (optional D3 research)

`developmental_ai.unaligned_stream` scores independent symbol insertions in sensor and forecast streams with reward-conditioned token-pair weights and a **hand-designed monotone sequence alignment**. The precommitted [protocol](benchmarks/unaligned_stream_protocol.json) fixes 240 train and 40 test episodes per seed for six previously inspected seeds. Reward-trained alignment completes **122/240** navigation tasks versus **50/240** for fixed-source lookup and **58/240** for an unordered learned pair baseline. A stronger unsupervised symbol-permutation + alignment rule achieves **142/240**, despite having no reward labels. A correct-cue reference completes **222/240**. The missing slot alignment causes real regressions; the learner remains experimental, cannot promote itself or issue system actions, and does **not** close D1/D3. See [full per-seed results, methods and limits](docs/UNALIGNED_STREAMS.md).

## Temporal correspondence (optional D3 experiment)

`probabilistic_alignment.py` marginalizes over all possible monotone eight-pair correspondences rather than committing to one path. It uses a *fixed, engineered* generative model and the previously learned unsupervised four-token mapping, not a learned temporal mechanism. Same-index six-seed navigation: **153/240** successes versus **143/240** for the old unsupervised max-path baseline, **134/240** for the prior reward-trained path and **222/240** for the oracle. Five seeds improved; one regressed. No default promotion or completed D1/D3 gate. See [protocol and full results](docs/TEMPORAL_CORRESPONDENCE.md); V2A/V2B unchanged.


## Variable event correspondence under insertion/deletion uncertainty (D3 research, 2026-10-17)

An optional `variable_correspondence.py` models **3–8 candidate shared events** instead of hard-coding eight matching observations. It fits a bounded symbol-reliability and event-overlap prior using **120 pseudo-selected, observation-only training streams** per seed, then marginalizes possible monotone alignments. On the same new synthetic deletion/insertion episodes, navigation was **125/240** versus **113/240** for the prior fixed-eight marginal (five seeds improved, one regressed), and **226/240** for the privileged correct-cue benchmark. A post-hoc simple public-length rule estimates the true event count **more accurately** than the learned estimate (MAE 0.585 versus 0.811), so this is not proven event counting. See [full protocol and negative controls](docs/VARIABLE_CORRESPONDENCE.md). The experimental mode is not the default; D1/D3 remain open and versions 2A/2B keep their agreed order.
