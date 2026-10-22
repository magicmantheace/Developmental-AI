# Passive public-outcome observation under an unfamiliar rule

**Experimental simulation-only. No claim that observational data is
harmless to obtain, causally sufficient, or safe for real-world action.**

The previous [absolute adequacy study](ABSOLUTE_ADEQUACY.md)
identified all six already-inspected third-rule contexts as unknown,
but completed zero tasks. It used 48 disposable probes in that new
rule, **16 of which caused simulated harm**. This next experiment
separates WHO takes actions to generate evidence from the learner
which reads already observed outcomes.

The [frozen pre-implementation protocol](../benchmarks/passive_outcome_protocol.json)
uses the same hand-authored third-rule simulator, a disjoint TRAIN
observation namespace and two new precommitted seed cohorts.
An independent **simulated external actor** chooses actions from
public frames, with no true action labels. Its consequences are
observed by `PassiveOutcomeArchive`, which **cannot choose an
action or call the world simulator**. The actor is not a real person;
the provenance is controlled by a benchmark harness, not an
authenticated source. Exact before/action/after public sensor
changes are recomputed and replayable with SHA-256 integrity.

- Each seed: 240 random one-step actor observations from
  `train/3000..3239`, and 240 observations from a separate
  source-trained *normal-law* actor in `train/3300..3539`.
- 24-observation comparison uses the exact first 24 of random240,
  with no independently sampled data.
- Candidate is an ordinary numeric five-nearest-neighbor outcome
  learner fitted ONLY on the passive transitions. The guarded policy
  requires at least five neighbors, mean productive effect >=0.6,
  and **zero estimated damage in its five neighbors**; otherwise
  it declines the action. This is a heuristic, not a credible
  upper bound on unseen hazards.
- Read-only held-out test namespace `test/23000..23059` on the
  third rule (60 goals per seed). Controls: raw passive learner,
  guarded 24/240 observations, bias-affected actor observations,
  the unchanged old normal/reversed models, zero-action abstention,
  and unfair simulator-privileged oracle.
- The benchmark reports **learner-issued calibration actions = 0**,
  but separately reports EVERY *external simulated actor* action
  and its damage, productive effects and neutral results, plus
  later test completion, harmful actions and aborted tasks.
  An externally sourced dataset may have profound harms,
  distribution bias, consent, provenance, and privacy concerns.
  None of these are solved by a passive API.
- Original old-model memories and passive archives remain
  immutable throughout held-out testing. All seed lists are frozen;
  after either group is inspected it is not blind.

These results cannot establish transferable biological
perception, independent self-development, causal identification,
zero-risk learning or real-world action safety. Third-rule
physics and numeric features remain fixed and engineer-defined.
No automatic policy promotion, no actual external observer
connection, no changes to Synveil/AthenZ or project priorities.

```sh
python -m unittest tests.test_passive_outcome -v
python -m benchmarks.passive_outcome_benchmark --cohort development
python -m benchmarks.passive_outcome_benchmark --cohort reserved
```
