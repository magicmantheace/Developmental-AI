# Variable observation-schema outcome learning — October 22, 2026

**Status: opt-in development experiment, draft/unmerged, simulation-only.**

## Hypothesis

A persistent experience-based outcome model that does not require one fixed
length and vocabulary of numeric action descriptors can encounter a *third*
synthetic rule family, learn a new schema from public effects, and retain
earlier family competence. It must be compared with a source-frozen model,
an independent target-only learner, recent-48 memory, random actions,
abstention, and a privileged simulation-only oracle.

**Frozen before new learner/benchmark:** [protocol](../benchmarks/variable_affordance_protocol.json),
commit `0cc4cf6`. Implementation on the same established
`developmental_ai/observable_affordances.py` numeric outcome architecture:
`VariableOutcomeMemory`, commit `eb82085`. The new worlds exist exclusively
inside the bounded benchmark; no new OS/network/controller authority.

## Environment setup

Three distinct, manually authored task families (not renamed versions of a
single rule) each expose new per-episode opaque action IDs and a list of
observed numeric features. The learner never receives the simulator's family
name, hidden action rule, true effect function, or stable action identifier.

- **Quarry**: `grade`, `moisture`, signed magnitude difference determines
  productive/damaging/neutral outcomes, goal 3 productive actions.
- **Coolant**: `flow`, `heat`, `seal`, three-way thresholds determine
  outcome, goal 4.
- **Relay**: `phase`, `pulse`, `shield`, `noise`; modulus relationship
  and protection distinguish productive from damaging actions, goal 2.
  This rule deliberately stresses ordinary Euclidean nearest neighbors.

Each independent episode has five productive, four harmful, and three neutral
possible actions (sampled without revealing which is which). One damage
ends the episode; fewer than the specified productive actions is failure.
The agent sees only the current public goal counter, damage counter, and
available actions/observations; action names are shuffled/new each episode.
Its pre-trained knowledge cannot match opaque identifiers by name.

### Experience and evaluation separation

The learner receives `features,progress,damage` from a **separate
random one-action simulator actor**, using public before/after observations;
it never initiates training exploration. Training:

1. 180 quarry and 180 coolant outcomes per seed.
2. At evaluation checkpoints, 0, 16, 48, or 160 new relay outcomes.
3. At each checkpoint, the unchanged learned state is tested on 40 separate
   TEST episodes per family per seed, while recording all task failures and
   simulated harmful actions. The same TEST episodes recur across checkpoints
   and are **not independent** across time.
4. Full history remains append-only and has a deterministic SHA-256 replay
   checkpoint, with old source observations retained for revisit.

Frozen development seeds: 142003/142021/142039. Separately frozen additional
seeds: 143001/143017/143041. All become **inspected** once results are read.
A real independent environment author/generator would be required for a
stronger D3 result.

### Explicit information constraints

The learner is not given a domain label or effect rule, but the set of
observed feature **keys** uniquely distinguishes these three worlds. It
partitions examples by exact observed key set: this is an **engineered**
schema-isolation inductive bias, not learned language meaning or semantic
alignment. Its nearest-neighbor classifier is the existing fixed Euclidean
algorithm generalized to varying-dimensional vectors.

Good target-family performance after feedback is **adaptation**, not
zero-shot transfer. Good old-family retention may result from schema
partitioning rather than an independently discovered memory-consolidation
mechanism. No model update is allowed on held-out TEST episodes.

The random actor incurs potentially harmful simulator actions; report its
harm separately from TEST-policy harm. Checkpoint hashes prove internal
replay only; they do not authenticate observational truth or prevent
colluding source forgeries. This does not resolve the earlier witness
poisoning findings or authorize real-world probing.

## Status / reproduction

Dedicated focused CI:
[Variable schema outcome learning](https://github.com/magicmantheace/Developmental-AI/actions/runs/39815731144).

Full historical validation is a **separate** exact-HEAD requirement; prior
successful CI does not prove that these new code changes are regression-free.

```bash
python -m unittest tests.test_variable_affordance tests.test_observable_affordances -v
python -m benchmarks.variable_affordance_benchmark --cohort development
python -m benchmarks.variable_affordance_benchmark --cohort additional
```

Do not promote to default controller, alter AthenZ/Synveil, or merge PR #2
without measured evidence and owner review. Preserve the established D1-D10
sequence and V2A preceding/overlapping V2B.

## Current open research questions

- Does performance on the genuinely new rule **increase** with feedback
  enough to beat random/frozen baselines?
- Does source-family success survive target adaptation when old source events
  remain in the same *checkpoint*?
- How often does the non-smooth modulus rule defeat nearest neighbors, and
  is a simple target-only learner just as good?
- Can the next pass learn useful *relations* despite completely different
  feature-key vocabularies, rather than partitioning them by designer names?
