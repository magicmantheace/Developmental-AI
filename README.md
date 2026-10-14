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

The new delayed-choice task presents an arbitrary cue, then hides it during 2–6 training distractors or 10–20 test distractors. At the final decision the learner selects one of four buttons. In retain mode a **hand-coded working-memory gate** stores the original cue; reactive and overwrite ablations do not preserve it. The response association is learned, but the retention rule is not.

Reproduce the recorded development-seed benchmark:

```sh
python -m benchmarks.delayed_choice_benchmark --seeds 11 31 73 --train-episodes 800 --test-episodes 400
python -m developmental_ai.delayed_choice train --mode retain --episodes 800 --db delayed_brain.db
python -m developmental_ai.delayed_choice evaluate --mode retain --band long --episodes 400 --db delayed_brain.db
python -m developmental_ai.delayed_choice trace --mode retain --index 3 --db delayed_brain.db > delay_trace.json
python -m developmental_ai.event_ledger export --trace-file delay_trace.json > events.json
python -m developmental_ai.event_ledger verify --ledger-file events.json --trace-file delay_trace.json
```

Across development seeds 11/31/73, the retained-cue policy reaches **100%** success on unseen long-delay sequences; the reactive baseline averages **22.08%**, near 25% chance. This is a deliberately small lookup task, **not** evidence of learned working-memory control, natural-language reasoning, personality, or independent agency. See [protocol and limitations](docs/DELAYED_CHOICE.md) and [raw benchmark results](benchmarks/delayed_choice_results.json).

The new simulation-only [event ledger](docs/EVENT_LEDGER.md) converts deterministic curriculum and delayed-choice traces into bounded hash-linked events for **future** AthenZ/Synveil adapters. It does not transmit data to those projects, authenticate event authors, or authorize any real action. Original transfer/curriculum baselines remain unchanged.
