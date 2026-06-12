# Statistical rigor: allocation, stopping, causal grading, trust checks

The campaign loop's instincts map onto the statistical canon — outcome→conclusion
table ≈ pre-registration, negative controls ≈ the but-for test, design/execute
split ≈ blinding, council/peer review ≈ an experiment review board. What the canon
adds is named machinery for four questions the loop otherwise answers ad hoc:
**which probe next, when to stop, how strong is a causal claim, and can this
delta be trusted at all.**

---

## 1. Which probe next (allocation)

- **Expected information gain.** The outcome→conclusion table already enumerates
  what each result would prove. Add a rough prior probability to each row and the
  most informative probe falls out: run the probe whose outcome distribution most
  reduces uncertainty about the campaign's central question — not the one that's
  merely next in the list. Re-rank remaining probes after every verdict. When a
  council deadlocks on a factual crux, route it to the probe with the highest
  expected information about the disputed fact, not the cheapest one.
- **Successive halving (the budget ladder).** Round 1 hits *every* hypothesis with
  the cheapest possible falsifier (one grep, one GET, one metric read). Only
  survivors earn a more expensive probe in round 2; survivors of that earn a full
  controlled experiment with confounds killed. Kill the bottom half each rung and
  reinvest the saved budget in the survivors. This is the formal version of
  "cheapest falsification first" applied across a whole campaign.
- **Thompson-style reallocation.** Splitting the probe budget evenly across N
  candidate causes is the wasteful uniform strategy. After each probe, shift the
  next wave's budget toward the hypotheses that are still live in proportion to
  how live they are. The `ruled_out` list is the degenerate case (posterior → 0);
  graded belief tells you where the *next* probe goes, not just which are dead.
- **Random, never grid.** When sweeping a multi-knob space under a small budget,
  sample configurations at random rather than on a grid — a grid wastes most
  trials re-testing axes that don't matter, random covers the few that do
  regardless of which they are (geometric corollary: ~60 random trials give
  ≈95% chance of hitting a near-optimal region occupying 5% of the volume,
  independent of irrelevant dimensions). Random breadth-first coverage is the
  honest baseline any cleverer allocation must beat.

## 2. When to stop (sequential validity)

- **Peeking is the failure mode.** Re-checking a metric repeatedly and stopping
  when it looks significant inflates the false-positive rate far above what the
  single look claims. Either fix the number of runs in advance, or use an
  always-valid sequential rule — e-values / confidence sequences for honesty
  under arbitrary data-dependent stopping, or classical SPRT when the
  hypotheses are simple and the stopping boundaries are pre-specified. The
  adaptive "found stuff → run another pass" loop is *legitimate* under
  sequential rules and p-hacking without them.
- **Early stops overestimate.** A result stopped early *because* it crossed the
  threshold is biased large — only inflated estimates cross early. Bank the
  verdict, discount the magnitude until a fixed-n replication confirms it.
- **Pre-commit decision thresholds.** "Loop until clean" gets its quantitative
  gate by deciding *before* probing what evidence ends each hypothesis
  (CONFIRMED / FALSIFIED thresholds), then stopping the moment one is crossed —
  no extra runs to make a verdict feel better, no quitting from fatigue. The
  ≥3-independent-replications convention is the crude fixed-n version of this;
  state which rule a verdict used.

## 3. How strong is a causal claim (the ladder)

Grade every causal verdict on the ladder, weakest → strongest, and say where it
sits:

1. **Correlation** — a story, not a finding.
2. **Temporality** — cause precedes effect in every observed case. Mandatory;
   no causal claim stands without it.
3. **Dose-response** — more of the cause yields more of the effect.
4. **Controlled experiment** — intervene, watch the effect move, with a control
   case (the but-for test: would the effect have occurred without the cause?
   Find the cases where the cause ran and nothing broke, and where it never ran
   but the symptom appeared anyway).

Discipline that goes with it:

- **0.90+ confidence on a causal claim requires temporality plus a control case
  (or dose-response) — not just strong correlation.**
- **Necessary ≠ sufficient.** Say which the evidence shows: "sufficient to
  trigger the symptom on affected hosts" is a different, more defensible claim
  than "caused the outage."
- **Before/after needs parallel trends.** A before/after delta in a treated
  group is only attributable to the treatment if a control group's trend shows
  both would have moved together absent it. Check the pre-period trend before
  trusting any difference-in-differences-style argument.
- **Check segments before declaring a winner.** An aggregate effect can reverse
  inside a segment (Simpson's paradox); a single headline delta can hide a
  confounded mix.
- **Prefer factorial over one-factor-at-a-time.** OFAT cannot see interactions;
  two probes that disagree may be an unmodeled interaction (flag × input size,
  batch × threads), not a bad measurement. A small factorial sweep estimates
  main effects *and* interactions for the same budget.

## 4. Can the delta be trusted (measurement discipline)

- **Benchmarking-confounds checklist** (the canonical blocking variables):
  thermal state (let clocks settle or lock them), cache warmth (discard warm-up
  runs or O_DIRECT), background load (quiet the box, verify idle before each
  probe), run-order drift (randomize or interleave A/B runs — running all of A
  then all of B confounds treatment with warm-up), replication (report n and
  spread, never a bare point number).
- **Two levels of replication.** Re-running the same binary measures measurement
  noise; rebuilding/rebooting/re-provisioning measures the variance that
  actually threatens reproducibility. Say which one your n refers to.
- **Power sketch up front.** State how many runs and why before measuring. A
  single run is an anecdote. Don't compute post-hoc power from the observed
  effect — it's circular.
- **Guardrail metrics.** Name the metrics that must NOT regress (latency, error
  rate, cost, memory) before running, and report each as a signed delta. A
  primary win that regresses a guardrail is not a win.
- **Pre-flight trust checks, before interpreting any delta:** allocation/sample
  sanity (did the runs split as designed — if not, the experiment is broken,
  don't read it), an A/A run (compare baseline to itself; any "significant"
  difference means the harness is miscalibrated), and Twyman's law (a result
  that looks surprisingly good is a measurement bug until proven otherwise).
- **Variance reduction across heterogeneous units.** When units differ in
  baseline performance (mixed hardware, warm vs cold), compare each unit against
  its own pre-measured baseline rather than raw across units — removes
  predictable variance with no bias and catches accidental baseline imbalance.

## 5. Confidence as a derived number (updating + audit)

- **Update in odds form.** When a probe returns, state the likelihood ratio it
  implies — "this observation is ~5× more expected if H is true than if not" —
  and multiply the prior odds, instead of jumping to a ladder rung. The
  confidence number then has a derivation, satisfying the same rule as verdicts:
  a number without evidence behind it is rejected.
- **Audit calibration against the ledger.** Every closed hypothesis carries a
  confidence and an outcome — the ledger is a ready-made calibration dataset.
  Periodically check whether claims tagged 0.7 held ~70% of the time (Brier
  reliability); if the 0.9s only come true 70% of the time, the ladder is
  miscalibrated — retune it. Falsification-first applied to the method's own
  numbers.
