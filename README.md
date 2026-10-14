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
