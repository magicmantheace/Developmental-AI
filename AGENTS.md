# Worker instructions

**Purpose:** Build a verifiable local-first learning engine for the independent-twin research program, due 2029-02-09. Own simulations, policies, procedural memory, reproducible evaluation, and tested integration APIs only.

1. Inspect the current Git branch and tests before changes; do several coherent tasks per pass when practical. Use meaningful commits and verify result; do not claim CI/hardware passed without evidence.
2. Run `python -m unittest discover -s tests -v`. For algorithm changes, run `python -m benchmarks.transfer_benchmark` and report all seeds, not only the best result.
3. Never commit `.db`/SQLite/WAL, private model weights, user stories, biometric data, secrets or consenting-person records. Keep such data in separately protected, owner-controlled local storage.
4. Report held-out data contamination and test tuning. A frozen evaluation protocol should not be modified merely to improve a reported score. Preserve baseline outcomes.
5. State limits exactly: the present transfer experiment varies maps of one family, with engineered directional observations. It does not prove broad intelligence or emergence of identity.
6. Keep AthenZ and Synveil as optional, versioned external integrations. No policy-derived root shell, automatic sharing, publishing, or unrestricted action execution.
7. Make persisted schema migrations and restart/resume regression tests explicit.
8. Before committing changes, verify repository visibility; assume code becomes public even if it is currently private.

9. Run `python -m benchmarks.delayed_choice_benchmark` for changes touching the
   delayed-cue memory experiment; publish all three mode ablations and all
   development seeds. Never describe its hard-coded retention gate as learned.
10. Event-ledger SHA-256 links are not provenance signatures or evidence of an
    authorized user. Do not add network, shell or system-action execution to the
    simulation-only ledger exporter.
11. Learned selective-memory claims require running `python -m benchmarks.selective_memory_benchmark`, comparing learned vs first/last/random and oracle, and explicitly disclosing the engineered context/source features and inspected development seeds.

12. Changes to occluded navigation must rerun the multi-seed
    `python -m benchmarks.occluded_navigation_benchmark`, preserve separate
    train/test indices and compare against learned-reactive, random, greedy
    and privileged full-map oracle baselines. Never call engineered dead
    reckoning a learned memory mechanism.

13. For `adaptive_dynamics.py` changes, rerun the full three-seed adaptive benchmark and report old-regime regression as well as new-regime gains, oracle predictive loss and navigation scores. Calibrated physics uses explicit **privileged simulation labels**; do not portray it as an independently discovered latent world model. Named snapshots are retained knowledge, not automatic context switching.

14. Changes to `online_dynamics.py` must run the full three-seed
    `python -m benchmarks.online_dynamics_benchmark` and report per-regime
    model selection, likelihood, wrong-model and privileged-oracle baselines.
    Do not mislabel initial-position-beacon/known-topology latent-state EM as
    unsupervised discovery of general physics or automatic continuous learning.

15. For `continuous_dynamics.py` changes, run both the three-seed main benchmark
    and additional-seed audit with the **same full model-training budget**.
    Retain the published small-budget failure rather than tuning it away.
    The monitor scores unlabelled *per-episode* observation streams against
    manually pretrained models; this is not self-sufficient discovery of new
    dynamics, within-episode control or a calibrated anomaly detector.

16. `step_dynamics.py` experiments must compare each incremental log-likelihood
    to the full latent forward likelihood, test exact mid-episode restarts,
    reject unknown labels in sensor records, and disclose changed-regime
    detection failures. Never describe the simple digest approval token as
    authenticated consent or stage candidate training as automatic promotion.
    Run `python -m benchmarks.step_dynamics_benchmark` and the original
    `python -m benchmarks.transfer_benchmark` unchanged.


16. Offline-calibrated step detection must never consume `test` namespace
    histories during calibration. Use `train` indices `5000+`, disjoint from
    model-fit `train` indices `0..N-1`. Keep the original `margin=0.12`
    detector unchanged, publish per-seed correct/wrong/abstained selection on
    development and additional audit seeds, and state that offline labels
    calibrate a heuristic threshold, **not** confidence probabilities.

17. `decision_abstention.py` introduces *read-only selective abstention*, not new model accuracy or a confidence probability. Preserve the frozen StepDetector baseline, use offline `train`-namespace calibration disjoint from model-fit and `test` evaluation, and report every seed's correct/wrong/abstain counts **and** coverage. Historical audit seeds have been inspected and cannot become a new blind holdout. Do not give an abstention profile permission to install or promote a model.

18. Candidate promotion now requires `CandidateStore.review` with distinct held-
    out observation histories, followed by explicit approval of the **review**
    digest. Never use the old model digest as approval. Run the six-seed
    `python -m benchmarks.candidate_review_benchmark` and separate unchanged
    transfer benchmark. Do not treat predictive likelihood gain as safety,
    navigation improvement or signed owner authorization. Keep all failures.

17. `streak_selection.py` is experimental and must not replace
    `decision_abstention.py` or authorize any real actions. Reproduce both
    the 17/23/41 benchmark and 1009/1013/1031 audit at the same training
    budget. Report correct/wrong/abstained for every seed, including
    regressions; 2% empirical step error is not a safety/confidence bound.

19. For optional `robust_world_model.py` experiments, compare against the unchanged `online_dynamics.fit` on identical train histories and EM iterations; keep model selection in separate train-namespace validation histories and evaluation in test-only indices. Publish predictive scores *and* downstream navigation regressions on seeds 17/23/41 and 1009/1013/1031 with matching budgets. A predictive gain does not authorize deployment, candidate promotion or claims of independent blind generalization. Preserve baseline and V2A/V2B roadmap scope.
