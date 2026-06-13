# DOE, causal inference, provenance, and online experimentation — lessons for the scientific-method plugin

Research wave for the `scientific-method` Claude Code plugin (investigations-as-falsification-campaigns).
Goal: import the statistical-experiment canon into the plugin so that "controlled experiments
with confounds named and eliminated" and the `EXPERIMENTS.md` ledger meet the bar that field
statisticians, ML-reproducibility reviewers, and industrial A/B platforms already hold.

Method: built-in WebSearch was unavailable for this model (API rejected the forced tool call), so
all sourcing was done with WebFetch against primary/authoritative pages. A few biomedically-framed
pages (Bradford Hill, causal inference) were blocked by the fetch sub-model's content filter; their
content is covered from the law/counterfactual and RCT pages plus general methodology.

Plugin files referenced throughout:
- `SKILL.md` — the loop (steps 0-7), esp. step 3 "Design controlled experiments"
- `references/campaigns.md` — Patterns A-E (fan-out, refute, forensics, council, peer review)
- `references/artifacts.md` — the `EXPERIMENTS.md` ledger and other artifact templates

---

## Topic 1 — Design-of-experiments canon (factorial, blocking, randomization, replication, power)

### Key sources
- Wikipedia, *Design of experiments* — Fisher's principles, orthogonality, multifactor designs.
- Wikipedia, *Statistical power* — power = 1−β; Lehr's rule n ≈ 16s²/d²; underpowered-study failure mode.
- Wikipedia, *Factorial experiment* / Hotelling weighing example (via the DOE page) — 8× precision
  from a combinatorial design at equal cost.

### Distilled principles
1. **OFAT is a trap; factorial designs dominate.** One-factor-at-a-time misses interaction effects
   entirely and is less efficient. Multifactor designs estimate main effects *and* interactions
   with the same or fewer runs (Hotelling: 8× precision at equal cost via a Hadamard design).
2. **Fisher's four pillars: comparison, randomization, replication, blocking.** Randomization
   mitigates confounding by balancing unknown nuisance factors; blocking *removes known* nuisance
   variation by grouping similar units; replication separates real effect from noise and lets you
   estimate variability.
3. **Interactions are first-class, not noise.** If factor A's effect depends on the level of factor
   B (compiler flag × input size, batch size × thread count), no single-factor sweep will reveal it.
   Two probes that disagree often disagree because of an unmodeled interaction.
4. **Power/sample-size is a pre-commitment, not a post-hoc number.** A priori power analysis sets the
   minimum runs needed to detect an effect of size d given variance s² (Lehr: n ≈ 16s²/d² per group
   for 80% power, α=0.05). Underpowered experiments are the single biggest driver of the replication
   crisis (median power ~10-36% across fields). *Post-hoc* power computed from the observed effect is
   misleading — don't report it.
5. **Blocking maps directly onto systems confounds.** Thermal state, cache warmth, background load,
   clock/turbo state, NUMA placement, and time-of-day are exactly the "known but irrelevant" nuisance
   variables blocking was invented for. Block on them (e.g., interleave A/B runs within the same
   thermal window) rather than hoping randomization averages them out in a tiny sample.
6. **Randomize run order to defang drift.** Thermal creep and cache state are *serially correlated*:
   running all of treatment A then all of B confounds the treatment with warm-up/drift. Randomizing
   (or interleaving) run order converts that systematic bias into noise you can quantify.
7. **Replication has two levels.** Repeating *measurements* (re-running the same binary) estimates
   measurement noise; repeating the *whole experiment* (rebuild, reboot, re-provision) estimates the
   variance that actually threatens reproducibility. Benchmarks usually report the first and pretend
   it's the second.

### Concrete suggestions for the plugin
- **`SKILL.md` step 3 ("Design controlled experiments")** — add an explicit benchmarking-confounds
  checklist alongside the existing GPU-contention/page-cache examples: *thermal state (let clocks
  settle / lock clocks), cache warmth (warm-up runs discarded or O_DIRECT), background load (quiet
  the box), run-order randomization/interleaving, ≥N replications with reported variance.* The skill
  already names confound-killing as the core discipline; this gives it the canonical list.
- **`SKILL.md` step 3** — add a one-line rule: *"When more than one factor is in play, prefer a small
  factorial sweep over one-factor-at-a-time — OFAT cannot see interactions, and two probes that
  disagree may be an unmodeled interaction, not a bad measurement."*
- **`SKILL.md` step 2 (Predict before measuring)** — add: *"State how many runs and why (a power/
  sample-size sketch). A single run is an anecdote; report central tendency and spread."* This wires
  power thinking into the pre-commitment the plugin already enforces via the outcome→conclusion table.
- **`references/artifacts.md` ledger** — add a `Runs / variance` column or a per-hypothesis note so a
  verdict cell records *n* and spread, not just a point number. The walls-doc discipline ("% of a
  *measured* ceiling") already pushes this direction; make replication explicit.

---

## Topic 2 — Causal inference & trial design (strengthen "confounds named and eliminated")

### Key sources
- Wikipedia, *Randomized controlled trial* — randomization, allocation concealment, blinding, ITT,
  threats to validity, "design features that make causal claims credible."
- Wikipedia, *Difference in differences* — parallel-trends assumption, differencing out time-invariant
  confounders, Ashenfelter dip.
- Wikipedia, *Causation (law)* — but-for / counterfactual test; necessary vs sufficient; NESS test.
- Wikipedia, *A/B testing* — peeking, segmentation (Simpson-style reversals), practical vs statistical
  significance, CUPED reference.
- Bradford Hill's criteria (covered via methodology summaries; primary pages content-filtered):
  strength, consistency, specificity, temporality, dose-response gradient, plausibility, coherence,
  experiment, analogy — **temporality is the one essential criterion** (cause must precede effect).

### Distilled principles
1. **Counterfactual is the gold standard: "but-for".** X caused Y only if Y would not have occurred
   but for X. This is exactly the plugin's negative-control requirement ("hosts where the playbook
   ran and nothing broke" + "hosts where it never ran but things broke anyway"). Name it as the
   but-for test to make the logic legible.
2. **A causal-strength hierarchy, weakest→strongest:** correlation → temporal precedence → dose-
   response (more cause → more effect) → controlled experiment with randomization. The plugin should
   grade causal claims against this ladder, not treat all "evidence" as equal.
3. **Bradford Hill as a confound-discipline checklist.** Temporality (mandatory), strength,
   consistency (replicates across independent samples — already Pattern C's "≥3 independent items"),
   biological/dose gradient, plausibility, coherence, and *experiment* (can you intervene and watch
   the effect move?). These convert "named and eliminated" from a slogan into a rubric.
4. **Randomization > matching > differencing > raw correlation.** When you can randomize assignment,
   do (A/B). When you can't, difference-in-differences subtracts out *time-invariant* confounders by
   comparing the *change* in a treated group vs a control group — but only under the **parallel-trends
   assumption** (both groups would have moved together absent treatment). Always check pre-treatment
   trends before trusting a DiD-style before/after.
5. **Allocation concealment + blinding prevent the experimenter from leaking the hypothesis into the
   measurement.** The agent analog: design and execution should not be the same pass with the answer
   known (the plugin's design/execute split already does this), and outcome metrics should be defined
   *before* the run (already enforced by the outcome→conclusion table). Name these as blinding analogs.
6. **Peeking inflates false positives; segmentation can reverse the winner.** Looking repeatedly and
   stopping when significant is p-hacking (→ Topic 4's sequential testing). An aggregate "A wins" can
   flip inside a segment (Simpson's paradox) — so a single headline delta can hide a confounded mix.
7. **Necessary ≠ sufficient.** A cause can be necessary, sufficient, both, or neither (NESS test:
   necessary element of a sufficient set). Forensic verdicts should say *which* — "the playbook was
   sufficient to trigger the outage on affected hosts" is a different, more defensible claim than
   "the playbook caused the outage."

### Concrete suggestions for the plugin
- **`SKILL.md` step 3 ("Controls are mandatory for causal claims")** — relabel the existing negative-
  control requirement as the **but-for / counterfactual test** and add the **causal-strength ladder**
  (correlation → temporality → dose-response → randomized control). Require every causal verdict to
  state where it sits on the ladder.
- **`SKILL.md` step 4 (verdicts/confidence)** — gate 0.90+ confidence for *causal* claims on at least
  temporality + a control case (or dose-response), mirroring Hill. This extends the existing rule that
  0.90+ needs ground-truth proof, specialized to causation.
- **`references/campaigns.md` Pattern C (forensic)** — the prompt already asks for a control case;
  add two lines: *"(2b) Is there a dose-response — does more of the suspected cause yield more
  symptom? (2c) Did the cause precede the symptom in every case (temporality)?"* and a note that an
  aggregate effect can reverse within a segment, so check segmentation before declaring a single cause.
- **`references/campaigns.md` Pattern C** — for before/after observational claims, add a one-liner on
  the **parallel-trends check** (compare a control group's pre-period trend) so DiD-style reasoning is
  done honestly rather than as a naive before/after.

---

## Topic 3 — Experiment tracking & provenance (what `EXPERIMENTS.md` should record)

### Key sources
- Wikipedia, *Preregistration (science)* — HARKing/p-hacking prevention, what a prereg records,
  registered reports, "a plan, not a prison."
- MLflow Tracking docs (mlflow.org/docs/.../tracking) — run/experiment data model; params, metrics,
  artifacts, code versions, tags, datasets, models; nested runs; searchable comparison.
- DVC experiment-tracking docs (doc.dvc.org) — Git-native experiments tied to commits; auto-captured
  changeset (data + code + params + artifacts); content-hashed data/model versioning; reproduce-from-
  scratch or restore-from-cache.
- Pineau / NeurIPS *Machine Learning Reproducibility Checklist* (cs.mcgill.ca/~jpineau) — the concrete
  per-result items (hyperparameter ranges + selection method, exact #runs, central tendency + spread,
  compute infra, runtime/energy, exact commands, statistical significance, downloadable code/data).

### Distilled principles
1. **Pre-registration = the plugin's "predict before measuring," formalized.** A timestamped record of
   the hypothesis + analysis plan *before* data is what distinguishes a genuine prediction from
   HARKing (hypothesizing after results known). The plugin's outcome→conclusion table is already a
   prereg; the ledger should *timestamp* it and forbid silent edits.
2. **Record the full changeset, not just the number.** MLflow/DVC both teach: a result is reproducible
   only if you captured params, code version (git commit), data version, environment/compute, and the
   exact command. The ledger's `Reproduce` block should pin *commit hash + env + command*, not just a
   command that assumes today's tree.
3. **Tie every run to an immutable code+data version (Git-native).** DVC's core idea — experiments are
   first-class Git objects anchored to commits — is the tamper-evidence mechanism. A ledger entry that
   cites a commit hash and a content hash of the input can be re-verified months later; one that says
   "ran the benchmark" cannot.
4. **The reproducibility checklist is a verdict-completeness contract.** Pineau's list maps cleanly:
   hyperparameter/config ranges + how the final config was chosen, exact number of runs, central
   tendency + variation, evaluation-metric definition, compute infra, runtime, and exact commands.
   A verdict missing these is "INCONCLUSIVE pending repro metadata," not "confirmed."
5. **Append-only + visible retractions = tamper-evidence.** The plugin's existing rule (scope
   corrections stay struck-through and dated, never deleted) is exactly the audit-trail norm from lab
   notebooks and prereg deviation-reporting. Reinforce: deviations from the pre-registered plan must
   be *reported*, not hidden ("a plan, not a prison").
6. **Datasets and inputs are versioned artifacts, not ambient state.** Both tools log dataset
   identity/hash with the run. For systems work the analog is: record the exact input file/workload,
   machine identity (the walls-doc "The machine" table — probed, not spec-sheet), and config snapshot.
7. **Central tendency *and* variation, always.** The checklist forbids reporting a bare mean. The
   ledger should carry n + spread (ties back to Topic 1 replication) so a future reader can tell a
   real delta from run-to-run noise.

### Concrete suggestions for the plugin
- **`references/artifacts.md` ledger template** — extend the `Reproduce` block spec to a **provenance
  header** per campaign: `commit:` (git SHA), `machine:` (probed identity), `env:` (toolchain/driver
  versions), `inputs:` (file + hash or workload spec), `date:`. This makes the ledger re-verifiable
  months later, which is the stated goal.
- **`references/artifacts.md` ledger rules** — add a **repro-completeness checklist** (adapted from
  Pineau) that a verdict must satisfy to be CONFIRMED: config + how chosen, n runs, mean + spread,
  metric definition, exact command, machine/env. Missing items → INCONCLUSIVE with the missing item
  named (consistent with the existing INCONCLUSIVE-names-its-probe rule).
- **`SKILL.md` step 6 (Persist the ledger)** — state explicitly that the outcome→conclusion table is a
  **pre-registration**: write it with a timestamp before measuring, and on deviation add a dated scope
  correction rather than editing the prediction. This hardens the existing "hypotheses that live only
  in conversation get silently mutated" warning into a prereg norm.
- **`SKILL.md` step 6** — recommend the ledger live in Git and that headline-number entries cite the
  commit they were produced at (DVC-style), making the falsification log tamper-evident: a
  DO-NOT-RE-ATTACK entry pinned to a commit can't be quietly re-litigated.

---

## Topic 4 — Online experimentation platforms (sequential testing, CUPED, guardrails, review boards)

### Key sources
- Wikipedia, *Sequential analysis* — SPRT, alpha-spending (Pocock, O'Brien–Fleming, Lan–DeMets),
  e-values / always-valid inference, early-stopping effect-size inflation bias.
- Statsig blog, *CUPED* — variance reduction via pre-experiment covariate; variance × (1−ρ²);
  θ = cov(Y,X)/var(X); unbiased; also corrects accidental baseline imbalance.
- General experimentation methodology (sequential-testing + guardrails) — always-valid p-values /
  confidence sequences, guardrail metrics (latency, crash rate, revenue, retention) tested one-sided
  for harm, auto-halt on regression.
- Wikipedia, *A/B testing* — the 13-org (Airbnb/Amazon/Google/Microsoft/Netflix/…) challenges paper;
  scale (Google/Microsoft >10k tests/yr); traffic-routing ingress control (route n% to the new
  version to limit blast radius).

### Distilled principles
1. **Peeking is only safe with always-valid inference.** Fixed-sample tests assume one look at a
   pre-set n; checking repeatedly and stopping when significant inflates the false-positive rate far
   above α. Sequential methods (SPRT / mSPRT, alpha-spending, confidence sequences / e-processes) keep
   the *ever-cross* probability bounded so you can monitor continuously. The tradeoff is wider
   intervals (less power per look). This is the rigorous answer to the plugin's "premature closure"
   failure mode — an agent that keeps re-checking a benchmark is peeking.
2. **Early stopping for "success" overestimates the effect.** Trials stopped early because they hit
   significance systematically inflate the effect size (only large estimates cross early). An agent
   that stops the moment a probe looks good should *discount* the magnitude, not bank it.
3. **CUPED: explain away predictable variance using pre-experiment data.** Adjust the metric by a
   covariate (the same unit's pre-period value); variance drops by (1−ρ²) with no bias, and it
   incidentally corrects accidental baseline imbalance between arms. Systems analog: regress out the
   machine's *baseline* throughput/latency (warm-up reading) so you compare each unit against its own
   expected performance — directly attacks the thermal/cache/hardware-heterogeneity confounds from
   Topic 1. This is variance reduction the plugin currently has no concept of.
4. **Guardrail metrics: protect what you're not trying to improve.** Alongside the primary metric,
   track metrics that must *not* regress (latency, error rate, cost, memory). Test them one-sided for
   harm; wire them to auto-halt. The plugin's "quietly absorbing a regression" failure mode is exactly
   this — guardrails make the signed-delta-against-baseline discipline enforceable and automatic.
5. **OEC — one pre-agreed success criterion.** Large platforms force a single Overall Evaluation
   Criterion so a win can't be cherry-picked across metrics post-hoc. The plugin analog: the
   outcome→conclusion table *is* the OEC; reinforce that the success metric is named before the run
   and not swapped for a friendlier one afterward.
6. **Trust checks catch broken experiments before interpretation: SRM + A/A + Twyman's law.** Sample-
   ratio mismatch (the arms didn't split as designed → the experiment is broken, don't read it), A/A
   tests (run the system against itself; if it finds a "significant" difference, the platform is
   miscalibrated), and Twyman's law (any figure that looks too good/surprising is probably an error).
   These are cheap pre-flight validity gates the plugin should run before trusting *any* delta.
7. **Institutional review = the council/peer-review patterns the plugin already has.** Big-company
   experiment review boards and central platforms institutionalize exactly Patterns D (council) and E
   (peer review): a body that decides go/no-go on evidence, catches bad experiments, and gates
   shipping. The agent already has decorrelated council seats and execution-grounded peer review; the
   missing piece is the *guardrail/SRM/A-A pre-flight* and *sequential-validity* checks above.
8. **Limit blast radius with staged rollout.** Route a small % of traffic to the new version first
   (ingress control), expand on green guardrails. The plugin already prescribes "dry-run/canary before
   irreversible steps"; name the guardrail-gated expansion explicitly.

### Concrete suggestions for the plugin
- **`SKILL.md` step 4 / step 7 (verdicts, loop-until-clean)** — add a **sequential-validity rule**:
  *"If you monitor a metric repeatedly and stop when it looks significant, you are peeking — false-
  positive rate is inflated. Either fix n in advance, or use a sequential/always-valid stopping rule,
  and discount the effect size of anything stopped early."* This is the statistical backbone for the
  existing "declare done only from a dry pass, not fatigue" rule.
- **`SKILL.md` step 3** — add **guardrail metrics** as a named concept beside baselines: *"Name the
  metrics that must NOT regress (latency, error rate, cost, memory) before running. Report each as a
  signed delta; a primary win that regresses a guardrail is not a win."* Turns "quietly absorbing a
  regression" into an explicit, checkable gate.
- **`SKILL.md` step 3** — add a **pre-flight validity check** line: *"Before interpreting any delta,
  run cheap trust checks — sample-ratio/allocation sanity, an A/A (compare the baseline to itself; it
  should show no effect), and Twyman's law (a surprisingly large result is probably a measurement bug
  until proven otherwise)."* Cheap, high-leverage, and matches the plugin's cheapest-falsification-
  first ethos.
- **`SKILL.md` step 3 (baselines)** — add an optional **variance-reduction** note (CUPED analog):
  *"When units differ in baseline performance (heterogeneous hardware, warm vs cold), compare each
  unit against its own pre-measured baseline rather than across units — this removes predictable
  variance and is more sensitive than raw cross-unit comparison."*
- **`references/campaigns.md` Patterns D/E** — add a sentence framing them as the agent's
  **experiment review board**, and cross-reference the SRM/A-A/guardrail pre-flight as the validity
  gate that runs *before* council/peer-review, so reviewers aren't asked to interpret a broken
  experiment.

---

## Cross-cutting takeaways (the through-line for all four topics)

- The plugin's instincts are right and already map onto the canon: outcome→conclusion table ≈
  pre-registration + OEC; negative controls ≈ but-for/counterfactual; design/execute split ≈
  blinding/allocation concealment; refute + council + peer review ≈ institutional experiment review;
  scope corrections ≈ deviation reporting. The gaps are **named statistical machinery**, not
  philosophy.
- Three concrete additions would close most of the gap: (1) a **benchmarking-confounds + replication +
  power** checklist in step 3/step 2 (Topic 1); (2) a **causal-strength ladder + Hill/temporality gate**
  on causal verdicts (Topic 2); (3) a **provenance header + repro-completeness checklist + sequential/
  guardrail/SRM-A-A trust checks** for the ledger and the run loop (Topics 3 & 4).
- The single highest-leverage edit: make `EXPERIMENTS.md` pin a **commit hash + machine/env + n + spread**
  per headline number. That one change makes the ledger reproducible and tamper-evident months later —
  the stated goal — and is cheap to adopt.
