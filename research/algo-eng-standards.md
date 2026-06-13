# Experimental algorithmics standards for demonstrable superiority claims

Scope: the rules that turn "my invention beats X" from an assertion into a defensible
empirical claim. Primary sources: David S. Johnson, *A Theoretician's Guide to the
Experimental Analysis of Algorithms* (DIMACS, 2002) — the ten-principles / Pitfalls /
Pet-Peeves canon; Catherine McGeoch, *Experimental Algorithmics* (CACM 2007) and
*A Guide to Experimental Algorithmics* (Cambridge, 2012); and the ML-evaluation
fair-baseline literature: REFORMS (Kapoor et al., *Sci. Adv.* 2024), Liao/Taori/Raji/Schmidt,
*Are We Learning Yet?* (internal/external validity taxonomy), the ML-Eval external-validity
guidelines (2021), the Nature ML reporting checklist, the Pineau ML Reproducibility
Checklist (v2.0), and Patterson et al., *Empirical Design in RL* (the RL "cookbook").

The throughline across all of these: **a superiority delta is only evidence to the extent
that the comparison was fair, the instances were representative, the win was attributed to
a specific cause, and the measurement was trustworthy and reproducible.** Each of those four
clauses is a named failure mode in the literature, and each maps onto machinery the plugin's
`rigor.md` already has — or exposes a gap it doesn't.

---

## 1. Johnson's ten principles (the canonical spine)

Verbatim headings from the paper:

1. **Perform newsworthy experiments.**
2. **Tie your paper to the literature.**
3. **Use instance testbeds that can support general conclusions.**
4. **Use efficient and effective experimental designs.**
5. **Use reasonably efficient implementations.**
6. **Ensure reproducibility.**
7. **Ensure comparability.**
8. **Report the full story.**
9. **Draw well-justified conclusions (and look for explanations).**
10. **Present your data in informative ways.**

The principles are illustrated by **Pitfalls** (temptations that waste the experimenter's
time) and **Pet Peeves** (paper-writing practices Johnson considers misguided). The ones
load-bearing for superiority claims are extracted below.

---

## 2. The tuned-baseline requirement (compare against the best incumbent, not a strawman)

This is the single most cited rule, and it appears independently in both literatures.

**Johnson:**
- **Pitfall 1 — Dealing with dominated algorithms.** An algorithm beaten by an existing
  competitor on *both* speed and quality is "dominated." Demonstrating you beat a dominated
  (obsolete, poorly-implemented) competitor proves nothing — it isn't newsworthy. You must
  beat the *current best* algorithm/implementation, or carve out a genuine niche where yours
  wins, or surface some other real insight.
- **Pet Peeve 7 — Irreproducible standards of comparison.** Comparing against a baseline
  nobody else can reproduce (unavailable code, unpublished numbers) is not a real comparison.
- **Pet Peeve 10 — Hand-tuned algorithm parameters.** Per-instance hand-tuning of *your*
  algorithm while leaving its tuning cost out of the reported budget inflates apparent
  performance. (Corollary, by symmetry: leaving the *baseline* untuned is the same crime in
  reverse — you must tune the incumbent as hard as you tune your invention.)

**ML-evaluation (the same rule, stated as a baseline-tuning discipline):**
- **REFORMS item 5f — "Justify that model comparisons are against appropriate baselines."**
  You must *detail how baseline models were trained and optimized*. If baselines were not
  chosen using the same model-selection / hyperparameter-search procedure as your method,
  they are "weak" and the apparent benefit of the new method is misleading. Cites Sculley
  et al. ("Winner's Curse?") and Lin as worked examples of weak-baseline inflation.
- **Liao et al., §3.4 "Comparison to inadequate baselines"** — a recurring internal-validity
  failure across CV/NLP/RL/recsys/graph ML. §3.4.1: simple methods (linear models, logistic
  regression + feature engineering, random search) are often *under-implemented and
  under-tuned*, so complex methods look better than they are. In graph learning, logistic
  regression with feature engineering matched neural nets at orders-of-magnitude less cost —
  a "win" that evaporated once the baseline was tuned.
- **RL cookbook (Patterson et al.), §6** — when comparing multiple agents "the claims are
  inherently much stronger and thus the standard of evidence and rigour goes up a notch."
  Fairness requires that hyperparameters, environments, run-length, and seeds be chosen so
  as not to silently advantage one algorithm; §6.3 cautions against ranking at all unless the
  comparison budget was genuinely equalized.

**The rule, distilled:** the incumbent must be run in its *best known configuration*, tuned
with the same budget and procedure as the challenger, on the same instances and machine,
with both tuning costs charged. A win over an untuned/strawman baseline is not evidence.

---

## 3. Instance diversity (testbeds that support general conclusions)

**Johnson, Principle 3**, with its peeves:
- **Pet Peeve 2 — Concentration on unstructured random instances.** Uniform-random inputs
  rarely resemble real-world structure; results on them support only weak conclusions about
  practical performance.
- **Pet Peeve 4 — The already-solved testbed.** Testing only on instances whose answers are
  already known biases toward easy cases.
- **Pet Peeve 3 — The millisecond testbed.** Instances too small to stress the algorithm
  measure noise, not behavior.
- **Pitfall 4** — the inversion warning: you start using random instances to study the
  *algorithm* and end up using the algorithm to study the *instances* — losing the plot.

**McGeoch** adds the structural insight: instance difficulty is often governed by a single
control parameter with **phase-transition / easy-hard-easy** behavior (the SAT m/n ratio
being the canonical case). A testbed that doesn't sample *across* the hard region near the
threshold can't support a general claim — the win may live entirely on the easy side.

**ML-evaluation analog (external validity):**
- **ML-Eval guidelines (b/c):** compare SOTA methods on *your* benchmark *and existing*
  benchmarks; "baseline simple methods" to confirm the task isn't unintentionally easy
  (verify you can't score high by ignoring part of the input — i.e., check for spurious
  shortcuts). Liao et al. frame "does progress here transfer to related tasks?" as the
  external-validity question that single-benchmark wins systematically fail.
- **Nature checklist C** asks for dataset-bias disclosure; **5d/test-set hygiene** (below)
  is the companion.

**The rule:** the testbed must span structured/realistic instances, scale up to sizes that
actually stress the method, and cover the hard region — and a single-benchmark win must be
flagged as not yet shown to generalize.

---

## 4. Ablation (which component carries the win)

Johnson's Principle 9 ("draw well-justified conclusions and *look for explanations*") is the
conceptual root, but the explicit machinery is sharpest in the ML literature:

- **Nature ML checklist, item 4F — "Ablation experiments are included."** A first-class
  reporting requirement: a multi-component method must show which component is responsible
  for the gain. Without it, the headline delta could be carried by an incidental choice
  (a better data-loader, a longer schedule, a tuned learning rate) rather than the claimed
  contribution.
- This is the **"which knob carries the win"** question. A factorial / leave-one-component-out
  design isolates the main effect of the claimed novelty from the effects of the scaffolding
  it ships with. Liao et al.'s "implementation variations" failure mode is the negative case:
  gains attributed to the new idea that were actually due to incidental implementation
  differences between the new method and the baseline.

**The rule:** decompose the win. Run the method minus its claimed novel component (and,
ideally, the baseline *plus* that component) so the delta is attributed to the part you're
claiming credit for, not to confounded scaffolding.

---

## 5. Scaling behavior (the asymptotic claim, measured)

McGeoch's central thesis: asymptotic worst-case bounds are weak predictors of real running
time (Quicksort can run thousands of times faster than its O(n²) bound, and the gap *grows*
with n; cache effects can invert the conventional "minimize instruction count" wisdom). So a
superiority claim about *scaling* must be measured across a range of n, not asserted from
the analysis or read off a single size.

- Johnson's **Pet Peeve 3 (millisecond testbed)** is the lower-bound version: instances too
  small never reach the asymptotic regime.
- The companion reporting items: **Nature 5A/5B** (report hardware, runtime, and compute
  cost) and the Pineau checklist's "average runtime / estimated energy cost" make the
  speed/cost axis a *guardrail*, not an afterthought — a quality win that costs 100× the
  compute is not unconditionally a win.

**The rule:** demonstrate the claimed advantage holds (or report how it changes) as instance
size grows across the regime that matters, and report the compute/time cost alongside, so a
quality win can't hide a cost regression.

---

## 6. Reporting & reproducibility standards

**Johnson:**
- **Principle 6 (reproducibility)** in the *broad* scientific sense, not byte-identical
  reruns: a later researcher using similar-but-distinct apparatus should obtain data
  *consistent with the same conclusions*. This is the notion to design for.
- **Principle 7 / Pet Peeve 13 (uncalibrated machine):** report and benchmark the machine,
  or cross-paper time comparisons are meaningless. Prefer machine-independent metrics
  (operation counts) alongside wall-clock.
- **Pet Peeve 11 (the one-run study):** a single run of a randomized algorithm is an
  anecdote — report the distribution.
- **Pet Peeves 8/9 (running time / optimal value as stopping criterion)** and **Pet Peeve 12
  (best result found as the evaluation criterion):** these are *irreproducible or inflated
  metrics* — a stopping rule keyed to wall-clock isn't portable across machines, and reporting
  the best-of-many-runs without charging for all the runs is cherry-picking.
- **Pet Peeve 15 (false precision):** don't quote more significant digits than the variance
  justifies.
- **Principle 8 (report the full story):** including the runs that didn't work.

**ML-evaluation:**
- **Test-set hygiene** — REFORMS 5d / Pineau: evaluate on test data held out from *both*
  training *and* model selection; report the split sizes and per-class counts. Test-set reuse
  / overfitting from repeated benchmark use is a named internal-validity failure (Liao et al.).
- **Hyperparameter reporting** — REFORMS 5e / Pineau: report the search range *and a
  justification*, the selection method (grid/random/nested CV), and the final values — for
  *both* the method and its baselines (ties back to §2).
- **Statistical testing with caveats** — REFORMS 7c: report the test and *justify its
  assumptions*; note that significance testing alone has led to false conclusions (report
  effect size + variation, not just a p-value).

**The rule:** report enough (machine, instances, code, seeds, splits, hyperparameter search,
n and spread, full results including failures) that an independent researcher reaches the
same conclusion with different apparatus — and never report a metric that is irreproducible
(time-based stopping) or inflated (best-of-runs, false precision).

---

## 7. Mapping onto the plugin's `rigor.md` machinery — coverage and gaps

`rigor.md` is organized around four questions — *which probe next, when to stop, how strong is
the causal claim, can the delta be trusted* — plus confidence-updating. That spine already
covers a large slice of the algorithm-engineering canon. The map:

| Algo-eng / ML-eval rule | `rigor.md` coverage today | Status |
|---|---|---|
| Same instances for all competitors; per-unit baselining | §4 "variance reduction across heterogeneous units" (compare each unit vs its own baseline) | **Covered** — this is McGeoch's CRN/variance-reduction idea in disguise |
| Benchmarking confounds (thermal, cache, run-order, background load) | §4 "benchmarking-confounds checklist" | **Covered** — maps directly onto Johnson Pet Peeve 13 + measurement discipline |
| Two levels of replication; report n and spread; no one-run anecdotes | §4 "two levels of replication," "power sketch up front" | **Covered** — equals Johnson Pet Peeve 11 + Pet Peeve 15 |
| A/A run, Twyman's law, allocation sanity | §4 "pre-flight trust checks" | **Covered** — Twyman's law is the inflated-delta guard |
| Factorial > OFAT; interactions | §3 "prefer factorial over one-factor-at-a-time" | **Covered** — and this is the *mechanism* for ablation (§4 above) |
| Random-not-grid config search under budget | §1 "random, never grid" | **Covered** — and is itself the honest-baseline-search argument |
| Guardrail metrics (cost/latency must not regress) | §4 "guardrail metrics" | **Covered** — equals the scaling/cost-guardrail rule (§5) |
| Pre-committed stopping; no peeking; early stops overestimate | §2 (sequential validity) | **Covered** — also subsumes Johnson Pet Peeves 8/9/12 (irreproducible/inflated stopping & best-of-runs) once those are named |
| Causal grading; necessary≠sufficient; segments/Simpson | §3 (the ladder) | **Covered** — supports "which component carries the win" attribution |
| Calibration audit against the ledger | §5 | **Covered** |
| **Tuned-baseline requirement** (beat the *best* incumbent, tuned with equal budget; no strawman; no dominated competitor) | — | **GAP.** `rigor.md` has rich *measurement* discipline but never states that the comparison target must be the best-configured incumbent. This is the #1 superiority-claim rule (Johnson Pitfall 1, REFORMS 5f, Liao §3.4) and it is absent. Add it as a named pre-flight gate: "before claiming a win, state how the baseline was tuned and that it used the same selection budget as the challenger." |
| **Instance-diversity / external validity** (structured + realistic + scaled + hard-region instances; single-benchmark wins don't generalize) | partial — §4 mentions heterogeneous units, but only as a variance concern | **GAP.** No rule that the *testbed itself* must be diverse and representative, span the hard region (phase transition), and that a single-benchmark win must be flagged as not-yet-general. Add Johnson Principle 3 + ML external-validity as a testbed-design gate. |
| **Ablation as a reporting requirement** (decompose the win to the claimed component) | implied by factorial design (§3) but never named as a *deliverable* | **PARTIAL GAP.** The factorial *machinery* exists; what's missing is the explicit standard "a multi-component win must ship a leave-one-out ablation attributing the delta." Name it (Nature 4F). |
| **Test-set hygiene** (holdout separate from model *selection*; no test-set reuse) | — | **GAP.** `rigor.md`'s sequential-validity section guards against *peeking at the metric over time* but not against *the test set leaking into tuning/selection* — the distinct ML internal-validity failure (REFORMS 5d, Liao §3). Add it. |
| **Reproducibility-as-conclusion-replication** + machine-independent metrics (op counts beside wall-clock) | partial — §4 names two replication levels | **PARTIAL GAP.** The *broad* reproducibility notion (different apparatus, same conclusion — Johnson Principle 6) and the op-count metric are not stated. Worth adding as the definition of what the replication is *for*. |

**Summary of what's missing:** `rigor.md` is essentially a complete *measurement-trust and
sequential-validity* manual — it nails "can this delta be trusted" and "when do I stop." What
it lacks is the **comparison-fairness and generalizability** half of the superiority-claim
standard: (1) the tuned-baseline requirement, (2) testbed diversity / external validity,
(3) ablation as a named deliverable, and (4) test-set hygiene. These are exactly the four
clauses the algo-eng and ML-eval literatures converge on — and adding them as four pre-flight
gates ("Is the baseline the best-tuned incumbent? Is the testbed diverse and scaled? Is the
win attributed to the claimed component? Was the test set quarantined from selection?") would
close the gap between *trusting a number* and *proving a superiority claim*.
