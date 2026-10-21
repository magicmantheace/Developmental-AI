# Anonymous-action causal discovery across different dynamics

**Status:** Optional standalone research experiment, not a replacement for
`OutcomeSkills`, `TransferBrain`, or any other default. October 20, 2026.

## Why this exists

Earlier source/assembly/delivery benchmarks used a **fixed manually shared
glyph/fact vocabulary**. Merely rotating an action's opaque ID did not test
whether the learner could function in an unfamiliar action ontology.

This experiment reuses the *same* observable-feedback controller on two
separately hand-authored environments with **different underlying physics**:

- `relay`: latched Boolean switches, one two-input AND prerequisite, a
  gate chain, and distractors. State changes are monotonic.
- `cargo`: multi-unit extraction, a charge requirement, consumptive
  processing, loading, shipment, a spoilage operation that can irreversibly
  prevent success, and a distractor. State changes can be **negative**.

Neither public observation contains `relay`, `cargo`, action meanings,
hidden recipes, semantic glyphs, privileged solution paths or stable action
identifiers. Action IDs and numeric sensor channel order rotate every
episode. The public goal is only an anonymized sensor channel and threshold.
The model sees the before/after vector and whether its selected action was
accepted.

**Shared engineered priors:** Both worlds expose one numeric sensor vector,
a list of anonymous action handles, one goal predicate, and one Boolean
accepted/blocked feedback; the learner is handed those structured fields.
It is not learning how to parse raw multimodal observations or natural
language. Two hand-authored families do **not** constitute an independently
administered generalization benchmark.

## Separate protocol committed before model implementation

See `benchmarks/opaque_causal_protocol.json` at commit `d3e9845`.
It lists all development and reserved seeds, indices, budgets, baselines,
outcome measures and explicit nonclaims before any model was executed.
No result-driven change to this protocol is permitted.

- Development seeds: 1103, 1109, 1123.
- Reserved seeds: 2017, 2027, 2039. These must be evaluated only once with
  the frozen candidate; thereafter call them **inspected**, not blind.
- Relay source train: `train/0..47` (48 episodes per policy).
- Separate relay source-validation diagnostic: `train/500..523`.
- Evaluation for relay and cargo: `test/8000..8059` (60 episodes each
  per seed and family).
- Episode action budget: **18** steps. Exploration parameters are frozen.
- Baselines: three original fixed heuristics (`novel`, `retry`,
  `switch`), simple cyclic and random, and a privileged **oracle**.
- Outcomes: task completions, attempted/blocked actions, steps with
  decreasing sensor values, and true spoilage actions (privileged for
  **benchmark scoring only**). Negative sensor changes can be productive
  consumption, so decreasing channels do **not** necessarily mean harm.

## Actual model

`OpaqueEpisodePolicy` learns during each episode: it remembers which
anonymous actions were attempted, at what observable state, and whether
they were blocked. It avoids retrying a blocked action without a state
change, and reconsiders it when sensor readings change. Three prewritten
variants differ in the priority given to untried versus newly retryable
actions. No mapping of action IDs or channels transfers across episodes,
because the handles are newly randomized and *no invariant action
description is supplied*.

`StrategySelector` uses observed completions and action costs from the
**relay source family only** to select one of these three engineered
strategies. Its persisted selection and episode feedback are replayed.
The selected strategy then runs **without cargo training** on the second
family. This is a small study of transferring an *exploration-strategy
choice* rather than acquired action/effect knowledge. Its design creates
an intrinsic ceiling on true zero-shot skill transfer; note failures.

**No hidden recipe access in the candidate:** `_relay` / `_cargo`
and `_privileged_plan` live in the simulator/benchmark and are not read
by `OpaqueEpisodePolicy` or `StrategySelector`.

Journal integrity: versioned SHA-256 with replay-validated policy decisions
and public state continuity. The digest is NOT authenticated provenance and
cannot prove a wholly forged yet internally consistent history is real.
The experiment does not touch human data, OS privileges, networks, or
third-party integrations.

## Experimental results

The original one-family raw-token alignment and outcome-skill benchmarks
remain unchanged. Both cohorts here should be reported completely rather
than cherry-picking selected-policy successes.

**Validation status:** To verify this branch, run the tests and benchmarks
below on the *exact HEAD*. Do not quote earlier CI green checks for a new
commit or imply results before execution.

```sh
python -m unittest tests.test_opaque_causal -v
python -m benchmarks.opaque_causal_benchmark --cohort development
python -m benchmarks.opaque_causal_benchmark --cohort reserved
python -m unittest discover -s tests -v
python -m benchmarks.transfer_benchmark --seeds 17 23 41 --train-episodes 5000 --test-episodes 300
```

## Next discriminating gate

The next real test should give the model a *learnable stable action
description* (rather than a meaningless rotating ID) that is expressed in
independently changing observation modalities; infer a latent
action/effect representation and compare it with a matched from-scratch
agent. Also evaluate unseen dynamics, longer tasks, stochastic and
nonstationary consequences, **matched total training cost**, and
forgetting on earlier tasks.

Until then, successful causal probing would demonstrate a bounded generic
algorithm on two structured toy simulators, not cognitive independence,
general intelligence, transferable semantic understanding or consciousness.
AthenZ/Synveil integration remains deferred. V2A computational affect stays
before/overlapping V2B virtual environment.
