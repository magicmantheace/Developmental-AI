# Two-window action-outcome confirmation (experimental)

This is a **post-hoc, simulation-only** response to the earlier
sequential-calibration finding: four public outcome probes reduced
damaging *disposable* calibration actions from 56/72 to 19/24 across
six inspected seeds while scoring 360/360 in each stationary world,
but early stopping failed all 360 reversed-rule tasks when its
first four observations preceded a rule change.

The [new precommitted protocol](../benchmarks/two_window_confirmation_protocol.json)
tests two *separate* four-sample windows with unchanged trained
source/reversed models, unchanged likelihood threshold, and no hidden
phase labels or action-name identities in model input. It is NOT a
blind test; the six seeds have been inspected repeatedly.

Methods, all evaluated on test/15100..15159:
- **early4:** choose from first four observed outcomes only.
- **confirmed8:** agree on source/changed in *both* public
  observation windows or **abstain**. Conflicting windows indicate
  evidence inconsistency, not proven physical regime change.
- **recent8:** choose according to the most recent four observations.
- **cumulative8:** pooled eight-observation likelihood.
- **always abstain:** zero harm AND zero completed tasks.
- **oracle:** unfair hidden-rule benchmark reference.

Both stationary rule environments and switches at the exact window
boundary are included: normal→reversed and reversed→normal. The
*simulator only* knows which physical dynamics generated each
training-namespace disposable probe. Probes may harm the simulated
environment and must be counted separately from evaluation harm.
A confirming policy may avoid a stale catastrophic model by
abstaining on a shifted context, **but this is not solving the task**.
A recent-only policy might succeed immediately after a known switch,
but remains vulnerable to yet another switch or noisy observations.

The policy and the original NumericOutcomeMemory never train on test
episodes. Checkpoint restoration recomputes each public observation
and the selected decision. SHA-256 protects integrity only; it is
not owner-authenticated consent or safe automatic promotion.

```sh
python -m unittest tests.test_two_window_confirmation -v
python -m benchmarks.two_window_confirmation_benchmark --cohort development
python -m benchmarks.two_window_confirmation_benchmark --cohort inspected-additional
```

All results including model-selection errors, task completions,
spoilage actions, abstentions and calibration harm must be published.
Do not alter historical study results, promote to default or claim
newly invented model semantics. Keep V2A before/overlapping V2B,
and cross-project integration deferred.
