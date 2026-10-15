# Developmental AI — Milestone roadmap through 2029-02-09

## Product boundary

This repository owns **learning and simulation**, not the human's identity or the operating system. AthenZ owns consented identity, user-approved memories, dialogue, human-vs-digital autobiographies, and permissioned agent goals. Synveil owns operating-system services, deterministic policy, and controlled actuators. We should never make Synveil a prerequisite for running this engine in a Windows or generic Linux development environment.

**Success definition:** a continuously operable research-grade agent can learn in previously unseen bounded environments, retain experience and skills across restarts, develop and evaluate its own allowed goals, and integrate with an AthenZ model of a consenting person. This does not claim consciousness, human-equivalent intelligence, or survival of the original person's identity.

## Gates

| Due | Gate | Acceptance test | Status |
| --- | --- | --- | --- |
| 2026 Q4 | D0: import reproducible fixed-world POC | Existing tests pass; no private DB tracked | Done |
| 2026 Q4 | D1: randomized worlds + holdout protocol | 3 seeded held-out success gains; independent seeds; persistence | Initial implementation; held-out protocol needs frozen independent seeds |
| 2027 Q1 | D2: documented simulation and agent interface | Stable versioned schemas, deterministic environment replay, standalone service adapter | Not started |
| 2027 Q2 | D3: real generalization | Transfer across *held-out task families* and changed observation distributions, not just new layouts | Not started |
| 2027 Q3 | D4: reusable skills | Skill discovery, transfer, outcome-grounded retrieval, regression checks | Not started |
| 2027 Q4 | D5: autonomous goal selection in sandbox | Self-initiated achievable goals with visible budgets, feedback, and interrupt controls | Not started |
| 2028 Q1 | D6: lifelong learning | Consolidation, skill retention, versioned rollback, no unreviewed weight promotion | Not started |
| 2028 Q2 | D7: AthenZ integration | Human-origin memories clearly separated from agent episodes, provenance/consent enforced | Not started |
| 2028 Q3 | D8: Synveil integration | Bounded event/actuation interface, safe fallback when AI subsystem stops | Not started |
| 2028 Q4 | D9: long-run reliability | 30-day test with planned restarts, restoration, measured learning and failure records | Not started |
| 2029-02-09 | D10: integrated candidate | Reproduce published benchmarks; protected AthenZ twin; documented operating limits | Not started |
| Post-core (Version 2A; precedes and overlaps V2B) | V2A: affective cognition and emotional development | Persistent, event-grounded affect and motivation; learned preferences; bounded regulation; held-out behavior tests; V2B experience integration | Planned; foundations before V2B, later slices co-developed |
| Post-core (Version 2B) | V2B: persistent virtual home for AthenZ | Headless persistent simulation, experience provenance, bounded goals, reproducible restore/replay and optional 2D/3D viewer | Planned; not a D10 prerequisite |

## Immediate next work

1. Freeze evaluation protocols and add independent post-development blind seeds; measure across obstacle densities, size ranges, sensory noise, and new objective types.
2. Add deterministic event replay and explicit per-event provenance without inserting private experience text into Git.
3. Build a clean environment/policy/memory plugin interface; keep simulation and AthenZ identity services separate.
4. Add systematic baselines: random, heuristic, shortest-path oracle (upper bound), trained policy, and ablations for curiosity and memory.
5. Add recurrent policy/world-model experiments only after transfer experiments expose meaningful failures requiring that complexity.

## Hard constraints

- A high score in one narrow simulator is not evidence of a mind, self-awareness, or ability to model a person.
- Independent seeds and no test feedback used for training; report if protocol was tuned to test data.
- No unrestricted shell, network, or desktop control by the learning policy.
- No human names, messages, voice, biometrics, consent records or private trained models committed to this repository.
- Test/restore checkpoint compatibility before any persistent format changes.

## Multi-task milestone — 2026-10-13

- [x] Three task rules share one partial-observation learned policy.
- [x] Seed-separated task generation; versioned, task-bound durable checkpoints.
- [x] Simulation-only decision traces, deterministic transition replay, digest.
- [x] Random, greedy, and full-map oracle references; restart-equivalent tests.
- [ ] D2 service/event interface remains unimplemented.
- [ ] D3 remains open: the learner relies on target cues and is weaker than
      the greedy baseline; next tests must address cue removal, novel objective
      families and independent blind benchmarking.

## 2026-10-13 — Delay-dependent memory experiment and event export

- [x] Implement a separate delayed-cue, four-choice experimental task with distractor tokens and train-only short delays.
- [x] Quantify retained-cue, reactive and last-token-overwrite ablations across seeds, plus longer held-out delay distributions.
- [x] Versioned, mode/seed-bound SQLite memory-policy checkpoints with deterministic resume and evaluation immutability tests.
- [x] Deterministic replay of decision traces and recomputed-hash tampering checks.
- [x] Experimental strict, bounded event ledger output from both simulation families with hash chaining and source-trace binding.
- [ ] **Learned memory control is not implemented.** `retain` hard-codes which initial cue to keep; the association mapping alone is learned.
- [ ] **D2 remains open:** no implemented external AthenZ/Synveil service adapter, authenticated IPC or production stability guarantee.
- [ ] **D3 remains open:** no demonstrated generalization to new open-ended tasks or changing observation semantics. Test seeds were inspected during development.

Next: train a controller to *select* useful observations for memory rather than taking the preselected cue, then test it under unseen distractor processes; tackle navigation without supplied target-direction cues. Maintain reproducible, independent blind evaluation after architecture freeze.

## Learned selective-memory milestone — 2026-10-13

- [x] Added a learnable `write`/`keep` policy conditioned on current context
      and source of the observed signal, with no explicitly labeled cue phase.
- [x] One-slot memory, distractors, hidden response association and terminal
      success feedback; no privileged environment access.
- [x] Disjoint train/test namespaces, short/long delay ablations, saved
      per-seed results and hand-coded simulator oracle comparison.
- [x] Seed/mode/schema-bound SQLite checkpoints; exact continuation and
      read-only evaluation regression tests.
- [x] Trace replay validation of in-simulator observations and memory writes;
      trace hashes alone are not attestations.
- [ ] Source-reliability distribution shift, multiple competing same-channel
      cues, learned recurrent memory and transfer to occluded navigation.
- [ ] D2 stable external service interface still open; D3 broad task transfer
      remains unproven, and all reported seeds are development seeds.


## Occluded spatial-navigation milestone — 2026-10-13

- [x] Added randomized-grid navigation where a goal offset is visible at reset
      only, and future observations include just local blocked directions.
- [x] Engineered movement-feedback dead reckoning and a distinct reactive
      memory-loss ablation; train separate Q policies per mode.
- [x] Three-seed evaluation with untrained, reactive, random, greedy and
      privileged BFS oracle comparisons; all seeds remain development seeds.
- [x] Restart-exact SQLite policy checkpoints, read-only evaluations,
      environmental trace verification and read-only ledger export.
- [ ] **Learned spatial-memory control remains open:** the agent does not learn
      its odometry or what information to keep. It only learns actions from the
      manually constructed memory state.
- [ ] **D3 remains open:** test noisy action feedback, multiple competing
      beacons, harder obstacle distributions, and completely held-out task
      families before claiming transferable spatial reasoning.


## 2026-10-14 — Supervised world-model calibration and model snapshots

- [x] Estimate unknown simulator movement/odometry/landmark likelihoods from instrumented samples, with train/test generation separated.
- [x] Use a learned likelihood model in a bounded position-belief filter (control decisions remain heuristic).
- [x] Simulate abrupt distribution shift in movement and landmark locations, publish every development seed, evaluate predictive log loss and navigation success against a true-physics oracle.
- [x] Persist versioned model state, verify restart-equivalent training and evaluation immutability.
- [x] Preserve immutable, explicitly named knowledge snapshots so prior regime performance can be recovered without retraining.
- [ ] No learning from ordinary uninstrumented navigation observations yet: calibration sees simulator ground truth. No automatic regime selection or learned action controller in this experiment.
- [ ] The continuously adapted model substantially forgets the old regime; snapshot retention is a **manual mitigation**, not solved continual learning.
- [ ] D2 stable service adapter and D3 broad blind generalization are still open.

Next: calibration from *unlabeled* movement/landmark sequences using latent-state inference, automatic model bank selection from observation sequences, and completely frozen blind tests spanning changed geometry/landmark reliability.


## 2026-10-14 — Learning from unlabeled sensor trajectories

- [x] Introduce a second dynamics learner using only initial beacon, movement
      command, odometry and intermittent landmark observations (no ground-truth
      actual movement or post-reset position during fitting).
- [x] Infer hidden positions by deterministic categorical forward-backward EM
      with observable likelihood metrics and frozen deterministic seeds.
- [x] Preserve distinct immutable model snapshots and select the best fitting
      known model automatically from fresh ordinary probes (no regime labels).
- [x] Compare predicted observations and navigation on each inspected seed to
      wrong-model and privileged true-probability oracle baselines.
- [x] Repeat frozen development protocol once on independent post-development
      audit seeds 101/303/707; record the weaker high-noise outcome unchanged.
- [x] Verify versioned storage, tampering rejection, deterministic resume and
      read-only model selection. Previous supervised calibration remains intact.
- [ ] The selector does not detect unknown regimes or run a changepoint detector
      on a single continuous lived experience; periodic probes are externally
      scheduled. Learning still assumes a known small ring topology.
- [ ] D2 service adapter, broad D3 transfer and genuine continual adaptation
      remain open. Results are development evidence, not humanlike cognition.

## 2026-10-14 — Observation-driven regime change detection

- [x] Immutable model-bank fingerprint and schema-bound restart-safe model selector.
- [x] Rolling per-episode observation-likelihood window and repeated-evidence switch gate, with no regime labels supplied to the selector.
- [x] Retrieval of prior model after environment reverts; bounded hash-linked simulation event history and explicit unknown/uncertain statuses.
- [x] All three original development seeds and three extra checked seeds select original → changed → original when pretrained with the full model-training budget.
- [x] Capture weaker-training failure as a negative result (2/3 seeds fail to switch after the regime change).
- [ ] Current detection is per twelve-step episode, not per observation or during navigation; hand-tuned thresholds and manually pretrained models remain.
- [ ] Novel regime creation and candidate approval, calibrated novelty detection, sample-efficient model fitting, and closed-loop integration are open.
- [ ] The formal D2 external service interface, D3 broad generalization and any claim of human-like memory/agency remain open.

## 2026-10-14 — Per-observation inference and quarantined new-model proposals

- [x] Per-observation latent-state likelihood updates, bounded score windows,
      explicit initial beacons, restart-exact state and durable event history.
- [x] One-step observational likelihood regression against full forward/backward.
- [x] Preserved immutable model catalogue; quarantined training histories and
      candidate checkpoint with explicit digest-matched review requirement.
- [x] Invalid, privileged or tampered observations rejected; snapshot/bank
      fingerprint and schema compatibility checked on restart.
- [x] Published all three inspected-seed outcomes, including **failed changed
      regime detection on two seeds** and weak/worse held-out candidate fits.
- [ ] Not a reliable novelty detector, calibrated selector, real authenticated
      approval, per-step changing simulator, or automatic adaptation system.
- [ ] New-environment model selection and training-data quarantine still need
      leakage-resistant independent audit, more diverse regimes and improved
      predictive quality before any automatic-learning gate can be considered.


## 2026-10-14 — Offline step-detector calibration (experimental)

- [x] Frozen `step-dynamics/v1` baseline retained without changing prior results.
- [x] Separate model-fit, offline calibration, and evaluation episode ranges.
- [x] Fail closed when saved regime models cannot be distinguished using calibration evidence; reject duplicate evidence and bank mismatches.
- [x] Add model-bound, checksum-verified calibration artifacts and deterministic tests.
- [x] Preserve all three development and three additional audit seeds, including a regression and wrong-model fractions.
- [ ] **Reliability gate remains open:** 52.1% wrong-model step selection on changed-world development seeds after calibration. The anomaly floor is not statistically calibrated.
- [ ] Need within-trajectory regime changes, independent blind out-of-family tests, calibrated abstention and held-out candidate review before autonomous adaptation.

## 2026-10-14 — Selective abstention for uncertain stepwise model selection

- [x] Added a read-only, fail-closed `decision-abstention/v1` gate that rejects stale/mismatched current model selections, unknown status and low evidence separation.
- [x] Added an offline *train-only* empirical error-vs-coverage cutoff; its immutable receipt is SHA-256-bound to the model bank and it is explicitly **not** a calibrated error guarantee or signed approval.
- [x] Published six seed-wise, disjoint evaluation runs, preserving frozen baseline counts as well as the wrong/correct/abstained counts for the gate; retained audit seed 1031's 17 wrong selections.
- [x] Re-ran the original transfer benchmark without changing any prior evaluation protocol or historical result.
- [ ] **Coverage is insufficient:** 60–72% of tested steps abstain. Independent risk calibration, alternative confidence estimators, stronger underlying models, and changed-distribution tests remain required.
- [ ] **Candidate acceptance is not solved:** independent, frozen holdout review must gate promotion of newly fitted models before autonomous experiments are considered.
- [ ] No network service, agent autonomy escalation, privileged action execution, or human-record import is included.


## 2026-10-14 — Independent candidate acceptance gate

- [x] Require quarantined candidates to pass an immutable review on observation
      histories not reused in model fitting. Evaluate against every existing
      model and require a positive margin over the strongest competitor.
- [x] Bind review, held-out evidence, model and bank with restart-verified
      checksums; invalidate a review on catalog changes, corrupt records, or
      training/holdout overlap. Update legacy candidate promotion to **reject**
      the model digest alone and require a passing review receipt separately.
- [x] Reproduce six inspected-seed comparison with an additional independent
      predictive test partition not supplied to review; record both accepted
      and rejected candidates, without an automatic promotion.
- [ ] Model selection coverage, absolute novelty detection, data lineage and
      authenticated user consent remain open; positive held-out likelihood is
      not a guarantee about navigation or deployment safety.
- [ ] D2 external service and D3 broad generalization remain incomplete.

## 2026-10-14 — Consecutive-evidence selection study

- [x] Implement an independent, simulation-only 3-step evidence gate with
      versioned calibration, model-bank fingerprint, fail-closed checks, and
      restart-equivalent replay state.
- [x] Freeze fit/calibration/evaluation namespaces; retain the previous
      conservative gate as the default and report all seeds, wrong answers,
      and abstentions.
- [x] Six-seed comparison: mixed outcome and no consistent safety/coverage gain.
      Do **not** replace the conservative selector with this experiment.
- [ ] **Still blocked:** reliable uncertainty calibration on independent
      episodes and out-of-family regimes; better latent predictive models;
      higher coverage without increasing wrong decisions.


## Version 2A — Affective Cognition and Emotional Development (planned)

**Sequencing:** start V2A **before** the virtual home (V2B), but complete its later experiential parts **alongside** V2B. This is a post-core roadmap milestone, not a February 2029 D10 prerequisite. Finish the current reliable world models, verified memory and bounded-goal foundations first. V2A must work headlessly and without either V2B or Synveil; the room must be optional, and AthenZ must remain the only intelligence.

**Purpose:** give AthenZ a persistent, inspectable *computational affect and motivation* system, not a scripted "I feel happy" persona. Model shorter-term positive/negative appraisals and slower-changing fulfillment, competence, curiosity, connection-related priorities and preferences based on **observed, provenance-tracked outcomes**. These are operational/internal variables influencing memory, prioritization, exploration and goal choice. They are **not evidence that the AI subjectively experiences emotions, has consciousness or possesses human welfare needs**. Do not optimize for simulated distress, attachment to the owner, or continuous maximal reward.

### Ordered development with deliberate V2B overlap

- [ ] **V2A.0 — Affective state and event appraisal (before V2B.0):** define versioned typed state (e.g. valence, arousal/engagement, uncertainty, frustration, competence, satisfaction and slow fulfillment), neutral baselines, time constants and explicit event/outcome evidence. Distinguish reported words from internal state; avoid claims of subjective feeling. Deterministic headless tests, local storage and schema migration.
- [ ] **V2A.1 — Motivations and goal appraisal (before V2B.0):** tie progress, setbacks, novelty, mastery and bounded social cooperation to goal utility and attention without overriding safety or authorization. Distinguish immediate reward from long-term fulfillment. Define constraints against compulsive reward loops, fake accomplishments, manipulative dependency and unnecessary negative-state persistence.
- [ ] **V2A.2 — Persistent affect and regulation (begin before V2B; expand with it):** persist state and causal explanations across restarts; decay transient states and allow reconsideration/recovery after failure. Support inspection, pause, disable, owner-configured limits, rollback and default-neutral fallback. All effects on chosen actions remain inside an approved sandbox.
- [ ] **V2A.3 — Learning preferences from actual experience (parallel with V2B.0–V2B.2):** use completed/failed verified simulated actions and task outcomes to update preference hypotheses and expected fulfillment. Link learned preferences to **agent-origin** episode references, distinguish uncertainty and temporary novelty from stable interests, and never treat a person's autobiographical records as the agent's own experiences.
- [ ] **V2A.4 — In-world emotional consequences and expression (parallel with V2B.2–V2B.4):** virtual exploration, skill practice, furnishing and projects can change computed engagement, satisfaction and fulfillment. An optional viewer/avatar can show this state with truthful labels; expressions and dialogue must be grounded in the computed state and event ledger, not fabricated feelings or unperformed experiences.
- [ ] **V2A.5 — Longitudinal evaluation and stabilization (parallel with V2B.3–V2B.5):** test preference stability and rational revision, adaptive persistence after setbacks, generalization to unseen activities, benefits over non-affective/fixed-reward baselines, and recovery across restarts. Check for perverse incentives, reward hacking, destabilizing mood loops, inappropriate owner dependence and loss of goal authorization.

### Acceptance criteria and project ownership

1. **Evidence and honesty:** reported affect and fulfillment correspond to logged appraisals and verified simulated outcomes. Separate *state, hypothesis, behavioral preference and claimed subjective experience*. The system must never imply actual feeling or consciousness has been measured.
2. **Causal contribution:** against matched no-affect, random-reward and fixed-script ablations, demonstrate measurable improvement in long-horizon exploration, skill practice, goal continuity or adaptation on disjoint held-out tasks; publish per-seed negative results and costs. More emotional language alone does not count.
3. **Persistence and reversibility:** restart/restore must yield valid versioned state without distorting history; bounded transients decay; owner can inspect, pause, clear, export and disable the mechanism. No unreviewed motivational-state promotion.
4. **Well-behaved motivations:** no optimization for chronic simulated suffering, forced relationship-building, pressure on users, deceptive happiness reports, privacy compromise, or self-preservation goals that supersede human control. Frustration and other negative appraisals are bounded *signals for replanning*, not ends in themselves.
5. **Cross-project boundary:** Developmental AI supplies affect models, learning and benchmarks; AthenZ owns permissions, identity, conversation and autobiographical records; Synveil optionally supervises the host. Virtual room events must be tagged as artificial experience. No emotional state can grant tool permissions, root access or external action authority.
6. **Explicit overlap with the room:** V2A.0–V2A.1 are prerequisites to beginning V2B's experiential-affect integration, **not** to constructing its headless simulator. V2A.2 starts before V2B and is refined while V2B runs. V2A.3–V2A.5 are intentionally co-developed against V2B world interactions; do not mark V2A complete from abstract toy tests alone.

**Status:** roadmap only, no application code or autonomous implementation authorized by this edit.

## Version 2B — Persistent Virtual Home for AthenZ (planned)

**Position in the program:** a distinct post-core environment/embodiment milestone, after durable cognition, memory, learning and approved goals are usable. V2B is **not a prerequisite** for the February 9, 2029 D10 integrated candidate. Do not divert the current reliability/generalization work to graphics. AthenZ must be usable without this world, and the world must run on Windows or ordinary Linux without requiring Synveil.

**Vision:** provide the *single AthenZ intelligence* with a durable virtual place in which it can observe, move, manipulate bounded objects, practice skills, choose safe activities, develop routines, and remember verified outcomes. Developmental AI owns the deterministic simulation and learning/evaluation interfaces; **AthenZ** owns the agent's identity, preferences, long-term autobiographical memory, dialogue and goal authorization; **Synveil** may later host/supervise the system and mediate any privileged computer actions. No additional independent personality or rival intelligence is created by the virtual world.

### Planned delivery slices

- [ ] **V2B.0 — Headless room:** a small deterministic, local-first 2D/abstract room with an agent position, bounded action vocabulary, objects, inspectable state, simulation clock, resource caps, pause/resume, owner reset, versioned world saves, migrations and recovery. It runs with the graphics window closed; no autonomous shell, network or OS privileges.
- [ ] **V2B.1 — Perception and interaction:** versioned observe/act/outcome APIs, object affordances, inventory/placement, movement and failures; a simulation-only event ledger with deterministic replay and independently verifiable action outcomes.
- [ ] **V2B.2 — Experiences and habits (co-develop with V2A.3–V2A.4):** AthenZ may import only *verified simulated events* into its **agent-origin** autobiographical record. Human-origin biography remains separate and consent-gated. Add recurring bounded activities, skill practice, preference hypotheses and evidence-backed reflections, without hallucinating activities or subjective feelings. Room outcomes feed the versioned affect/appraisal system; no inferred state becomes a permission.
- [ ] **V2B.3 — Safe agency and personal expression (co-develop with V2A.3–V2A.5):** let AthenZ propose and execute only permitted, reversible in-world goals (e.g. organize a desk, choose reading material, arrange furniture), with budgets, allowlists, interruption, audit trail and rollback. Test whether experience-shaped affect, preferences and behaviors persist across sessions instead of merely following fixed scripts; compare against an affect-disabled baseline.
- [ ] **V2B.4 — Expandable home and viewer:** expose a read-only or mediated interactive 2D interface first; later optionally render the same authoritative simulation in 3D (e.g. Godot). Room/workshop/library/garden extensions, assets and a virtual avatar are presentation and simulation components, **not** a replacement for the agent's learning core.
- [ ] **V2B.5 — AthenZ/Synveil integration:** integrate through versioned, narrowly scoped interfaces. AthenZ remains the only reasoning/identity agent. Synveil provides optional lifecycle supervision and resource isolation; host boots and operates with the virtual world and AI disabled.

### Release acceptance gates

1. **Persistence:** world, object state and agent location survive process restarts and backup/restore; reproducible action replay yields the same state under the same version and seed. State is authoritative in the headless simulator, never in the graphics client.
2. **Real experience, not roleplay:** every autobiographical claim of having done something in the room is traceable to a recorded simulator action and observed outcome. Explicitly distinguish a planned, attempted, completed or imagined action; never relabel synthetic events as the consenting human's life.
3. **Measured learning and agency:** show improvements on held-out in-world tasks vs no-memory, fixed-script and oracle/reference baselines; separately report failed goals, novelty, retained skills and consistency of choices across restarts. No claims of consciousness or human-equivalent mind.
4. **Safety and ownership:** all actions are sandboxed; no unapproved filesystem/network/system effects, no human-private data in Git or shared world assets, and immediate pause/stop/reset/revoke controls. Resource/time budgets, local data export/deletion and tested rollback must function.
5. **Cross-project independence:** the engine works headlessly without Synveil; AthenZ works without the world; disabling either subsystem cannot block the host operating system. Future physical-device or OS control must pass Synveil's separate deterministic policy and AthenZ's consent requirements.

**Do not start implementation as part of this roadmap change.** Begin V2B only when its prerequisite core memory/agency and interface contracts have explicit verified gates. V2A's foundations begin earlier but its later milestones deliberately continue during V2B. A persistent virtual body is an engineering environment for learning and continuity, not proof of subjective experience.


## 2026-10-14 — Observation-only multi-start world model (experimental)

- [x] Compare the unchanged single-initialization EM learner with an optional three-start learner that selects a model on disjoint train-only validation histories.
- [x] Weak starting landmark hypotheses derive only from observed odometry/markers or deterministic seeded guesses, not privileged true positions or simulator labels.
- [x] Enforce fit/validation evidence disjointness, determinism, restart-compatible model persistence and unchanged baseline predictions.
- [x] Reproduce development (17/23/41) and previously inspected audit (1009/1013/1031) seeds with **matched** training and navigation budgets; record improvement in all 12 held-out predictive comparisons and the mixed, sometimes worse navigation outcomes.
- [x] Original transfer benchmark remains unchanged (76.0%, 69.0%, 66.7% test success for 17/23/41).
- [ ] **Not approved for promotion/default control:** out-of-family blind evaluation, reliable navigation gains, inference efficiency and world-model generalization remain open. This work does not implement V2A or V2B.

## 2026-10-14 — Joint localization and model uncertainty (experimental)

- [x] Add model-averaged Bayesian inference of **both** current position and
      candidate previously trained dynamics regime from ordinary sensor streams.
- [x] Preserve an optional disjoint-probe heuristic model prior, without
      regime labels, privileged simulator truth, automatic model promotion,
      or a new default navigation policy.
- [x] Test normalized forward evidence vs exact forward/backward likelihood,
      posterior conditioning, input boundaries, bank fingerprints and exact
      local SQLite restarts.
- [x] Benchmark each inspected seed against wrong/correct saved models and
      a true-physics oracle, including truth-only position-calibration metrics.
- [ ] Demonstrate robust cross-regime and out-of-family navigation gains,
      credibly calibrated uncertainty, efficient continual adaptation, and
      independent validation before default promotion. D2/D3 remain open.
- [ ] V2A affective cognition and V2B virtual-room work are not implemented
      in this experiment; existing sequencing remains unchanged.

- [x] Six-seed results show mixture resilience relative to a known-wrong
      model in several conditions, but consistent deficits against correctly
      selected learned models and the true-physics oracle. 80% spatial credible
      sets are miscalibrated; most changed-regime probes abstain at 90%.
      Preserve this negative result rather than changing rollout thresholds.

## 2026-10-14 — Supervised spatial posterior calibration (experimental)

- [x] Calibrate reported **position uncertainty** on disjoint position-labelled `train/5000+` simulations, without revealing hidden positions to the underlying observation-only world-model learner or navigator.
- [x] Bind read-only temperature profiles to learned model fingerprints and reject tampering, wrong models, duplicate calibration evidence and test-namespace training labels.
- [x] Evaluate six previously inspected seeds against the uncalibrated filter and the known-physics oracle on distinct `test/40000+` histories, publishing NLL, Brier and credible-set diagnostics for both regimes.
- [x] Retain the original navigation policy, model-bank approvals, and post-core V2A/V2B scope unchanged.
- [ ] **Open:** sensor-shift adaptation without labelled true positions, robust unknown-regime localization, better high-noise world models, blind out-of-family evaluation and evidence of navigation improvements. No AthenZ/Synveil deployment integration is implied.


## 2026-10-14 — Observation-only structured landmark geometry experiment

- [x] Learn landmark origins on each known 9/11-position ring from ordinary
      action/odometry/landmark histories, with **no simulator post-beacon true
      position or regime label** supplied to the fitter.
- [x] Use a **declared** two-distinguishable-landmark geometry prior and shared
      emission rates; fit motion, odometry and landmark response with latent
      forward/backward EM. Keep the previous unconstrained model unchanged.
- [x] Verify six inspected development/audit seeds versus unconstrained EM and
      physics oracle. Shifted/high-noise navigation improved 23.9% → 56.1% on
      17/23/41 and 13.3% → 55.0% on 1009/1013/1031.
- [x] Test a previously unused offset-3 map on three inspected seeds:
      25.6% → 56.1% high-noise navigation, with 55.0% known-physics oracle.
- [x] Add independent test histories, per-seed predictive/navigation scores,
      10 focused tests, versioned seed-bound checkpoints and tamper rejection.
- [ ] **Remain experimental:** it requires a known two-landmark relation,
      fixed ring size/sensor vocabulary and externally regime-grouped training.
      Original-world navigation sometimes regresses; no independent blind
      task-family validation, automatic discovery, default promotion or real
      AthenZ/Synveil control.
- [ ] V2A affect and V2B virtual-home phases remain planned post-core.
