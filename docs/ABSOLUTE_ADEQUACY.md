# Absolute outcome adequacy: noisy known laws and untrained third rule

**Experimental, simulation-only; not real-world safe experimentation.**

The previous two-window study demonstrated a trade-off: comparing
first and recent public-action feedback can reject a stale rule
but can also abstain from useful work. This separate study asks
a harder question: *does either known model explain the observations
at all?* A simple likelihood comparison between two known models
does not answer that question.

A [frozen-before-code protocol](../benchmarks/absolute_adequacy_protocol.json)
defines a new independent synthetic action-feature generator with
exactly four productive actions under EACH of three hand-designed
laws. The original normal and reversed laws are optionally
perturbed: 10 percent of productive or damaging actions are
deterministically neutralized, independently for each event.
The new third law makes near-diagonal feature pairs productive,
and some off-diagonal pairs harmful. Numeric features remain
engineered. The agent is NOT given hidden names or rule labels.

The two familiar numeric-outcome memories are trained only on
the pre-existing 80 normal and 80 reversed episodes. In each
world, eight disposable `train/2000..2007` single-action probes
are chosen to maximize predictive disagreement. All damaging
probes count. Each four-sample window records absolute best-model
mean negative log likelihood. The candidate treats mean NLL
above 1.2 as **unknown**; otherwise uses the previous log
likelihood margin of 2 and requires the two windows to agree.
Unknown, uncertain, and abstention do not count as completed work.

The predeclared controls use relative-only two-window agreement,
recent-only relative selection, forced source, forced reversed,
always abstain, and unfair privileged true-consequence oracle.
Each is evaluated across 60 tasks per seed and world on
`test/22000..22059`, with development seeds
93001/93013/93031 and reserved 94011/94023/94029.
Once inspected, neither set is blind. This experiment is distinct
from and does not change the previous frozen benchmark.

**Major limitations:** This third law and noise model are handcrafted;
the agent does not learn a third dynamics model or solve it by
independent skill acquisition. Absence of test harm after declining
actions proves only abstention, while calibration may have damaged
the simulated environment. Source models and public evidence are
SHA-256 replay checked, not authenticated as real user consent.
The study cannot authorize unsafe interventions on people,
software, finances, or external systems. No default policy change,
branch merge, Synveil/AthenZ integration or D3/D4 completion.

```sh
python -m unittest tests.test_absolute_adequacy -v
python -m benchmarks.absolute_adequacy_benchmark --cohort development
python -m benchmarks.absolute_adequacy_benchmark --cohort reserved
```
