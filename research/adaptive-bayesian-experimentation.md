# Adaptive & Bayesian Experimentation: what the scientific-method plugin should adopt

Research date: 2026-06-11. Sources fetched via built-in WebFetch (WebSearch was
non-functional for this model; primary/canonical sources fetched directly).

## Why this matters for the plugin

The plugin today runs a **fixed-design** campaign loop: convert assertions to
hypotheses, pre-commit an outcome→conclusion table per hypothesis, run one
isolated probe each, record a verdict with hand-assigned calibrated confidence,
loop until a pass is dry. This is rigorous about *not fooling yourself* but it is
**static about resource allocation and stopping**:

- Probe budget is split implicitly evenly (one agent per hypothesis), regardless
  of which hypothesis is most uncertain or most decision-relevant.
- "Loop until clean" has no principled stopping rule beyond "a dry pass" —
  fatigue and premature closure are called out as failure modes but no
  quantitative gate prevents them.
- Confidence is assigned by a heuristic ladder (0.90+ for ground truth, 0.55–0.75
  for inference, "never default to 0.85/0.95"). It is audited qualitatively, not
  updated by an explicit likelihood-ratio rule, and never scored for calibration.
- Multi-agent fan-out designs probes *up front* and runs them all; it does not
  reallocate the next wave's budget based on what the first wave returned.

The methods below are the formal machinery for exactly these gaps: **which
experiment next, how much budget each hypothesis gets, when to stop, and how to
update belief.** Each entry: what it is, when it beats fixed design, and a
concrete slot into the campaign loop.

---

## 1. Bayesian optimization / sequential model-based optimization (SMBO)

**What it is.** Treat the campaign objective (e.g. "how much headroom is past
this asserted ceiling", or a continuous tuning knob) as an unknown function you
can only sample noisily and expensively. Fit a cheap *surrogate model* (usually a
Gaussian process) to the results so far, then use an *acquisition function* to
score every candidate next experiment by trading off exploration (sample where
the surrogate is most uncertain) against exploitation (sample where it predicts
the best outcome). Run the highest-scoring experiment, update the surrogate,
repeat. Common acquisitions: Expected Improvement (EI), Upper Confidence Bound
(UCB), Probability of Improvement (PI), Thompson sampling, and entropy/
information-based ones (see §6).

**When it beats fixed design.** When each experiment is expensive and the search
space is larger than the budget — you cannot afford a grid or even dense random
sampling. Because each evaluation informs the next, BO "reasons about the quality
of experiments before they are run" and reaches a good answer in *far fewer*
evaluations than grid/random search. Its weakness is the opposite regime: cheap,
trivially-parallel evaluations where you'd rather just fan out (see §3).

**Slot into the campaign loop.** This is the formal version of step 0
("cheapest falsification first") generalized across a whole campaign. After each
probe, maintain a lightweight surrogate over the *space of remaining probes*
(even just a ranked table with an uncertainty estimate per hypothesis), and pick
the next probe by an acquisition score rather than running them in arbitrary or
fixed order. For ceiling-breaking sweeps (Pattern A), instead of pre-writing one
probe per asserted limit and running all of them, run the probe with the highest
expected improvement-over-baseline first; its result reshapes which remaining
probes are worth running at all. Concretely: add an "acquisition" column to the
hypothesis ledger and re-sort it after every verdict.

---

## 2. Multi-armed bandits / Thompson sampling

**What it is.** The multi-armed bandit problem: repeatedly choose among arms
(here: hypotheses, or competing fixes/explanations) with unknown payoff, aiming
to find/exploit the best with the fewest pulls. **Thompson sampling** is the
Bayesian solution: keep a posterior over each arm's value; each round, draw one
sample from each arm's posterior and pull the arm whose sample is highest; update
that arm's posterior with the result. Exploration is automatic — an arm is pulled
with probability equal to its posterior probability of being best, so plausible
contenders keep getting probed while clearly-bad arms are quickly abandoned. It
is "instantaneously self-correcting", matches UCB-style regret bounds, and beats
ε-greedy (which wastes a fixed fraction of trials uniformly, including on
obviously-bad arms).

**When it beats fixed design.** When you have several competing hypotheses /
candidate root causes / candidate fixes and a fixed probe budget, and you want to
concentrate that budget on the live contenders *as evidence arrives* rather than
splitting it evenly. Equal allocation (the plugin's current implicit default —
one agent per hypothesis) is exactly the wasteful uniform strategy bandits beat.

**Slot into the campaign loop.** In forensic root-cause campaigns (Pattern C)
with N candidate causes, treat each cause as an arm. After each probe, update
that cause's posterior probability of being the true cause, then sample to choose
which cause to probe next — budget flows automatically toward the surviving
contenders and away from those the controls have ruled out. The plugin's existing
`ruled_out` list is the degenerate (posterior→0) case of this; Thompson sampling
generalizes it to graded belief and tells you *where to spend the next probe*.

---

## 3. Random search vs grid search (Bergstra & Bengio 2012)

**What it is.** To search a multi-parameter space under a fixed trial budget,
draw each trial's parameters independently at random instead of laying them on a
regular grid. Grid search tests only a handful of distinct values per axis and
wastes most trials varying parameters that don't matter; random search tries a
new value of *every* parameter on *every* trial, so it covers the few important
axes densely regardless of which ones turn out to matter ("low effective
dimensionality"). Quantitatively: if near-optimal configs occupy ~5% of the
volume, ~60 random trials give ~95% probability of landing at least one in that
region — **independent of the dimensionality of the irrelevant axes**.

**When it beats fixed design.** Almost always beats *grid* search as a baseline:
trivially parallel, robust to failed trials, extendable (add more samples without
redesigning), reproducible by seed. It does *not* beat adaptive methods (§1, §2,
§4) — Bergstra & Bengio are explicit that random search is a strong, honest
*baseline*, not optimal; sequential methods that learn from past trials win when
evaluations are expensive.

**Slot into the campaign loop.** Two adoptions. (a) When a campaign has a
multi-knob space to sweep and the budget is small, the plugin should *default to
random sampling, never a grid* — and say so in references/campaigns.md as the
honest baseline. (b) Adopt the deeper lesson as a methodology rule: **most
hypotheses in a campaign don't matter, but you don't know which up front** — so
breadth of cheap independent probes (the fan-out) should precede depth on any one
hypothesis. This already matches the plugin's "cheapest falsification first"
instinct; make it explicit that breadth-first random coverage is the correct
*baseline* against which adaptive allocation (§1, §2, §4) must justify itself.

---

## 4. Successive halving & Hyperband (budget allocation across competitors)

**What it is.** **Successive halving (SHA):** start N candidates each with a small
budget (a cheap, short probe), evaluate, kill the worst half, double the survivors'
budget, repeat until one remains. Compute reclaimed from killed candidates is
reinvested in the promising ones. **Hyperband** runs SHA at several
N-vs-per-candidate-budget settings to hedge the central tradeoff (many candidates
probed briefly risks killing slow-starters; few probed deeply risks missing good
regions). **BOHB** replaces Hyperband's random candidate sampling with Bayesian
(model-based, §1) selection — sample-efficient *and* early-stopping.

**When it beats fixed design.** When you have many competing hypotheses and the
definitive probe for each is expensive, but a *cheap partial probe* is predictive
of the full one. Fixed design pays the full probe cost for every hypothesis,
including ones a 2-minute check would have killed. SHA pays the full cost only for
survivors.

**Slot into the campaign loop.** This is the formal backbone for "loop until
clean" plus the existing cheap/expensive **tool split** (Pattern C:
"investigators get expensive exploratory tools, synthesizers get cheap
confirmatory ones"). Structure each campaign pass as a halving rung: round 1 hits
*all* hypotheses with the cheapest possible falsifier (one grep / one HTTP GET /
one metric read); only hypotheses that survive earn a more expensive probe in
round 2; survivors of that earn a full controlled experiment with confounds
killed. The plugin already has the ingredients (cheapest-first, tiered tools);
SHA gives the explicit "kill the bottom half each rung, reinvest the budget"
rule and a principled budget ladder instead of ad-hoc looping.

---

## 5. Sequential hypothesis testing & always-valid stopping

**What it is.**
- **SPRT (Wald).** Test H0 vs H1 by accumulating the log-likelihood ratio after
  each observation: S += log Λ. Two thresholds set from the target error rates
  (a ≈ log(β/(1−α)), b ≈ log((1−β)/α)); keep sampling while a < S < b, accept H1
  at S ≥ b, accept H0 at S ≤ a. It stops as soon as evidence is decisive and is
  *optimal* (Wald–Wolfowitz): among tests with the same error rates it minimizes
  the expected number of observations.
- **E-values / anytime-valid inference (modern successor).** An e-value is a
  nonnegative statistic with expectation ≤ 1 under the null (a generalized
  likelihood ratio / a fair-bet payoff). Multiplying per-round e-values gives a
  test martingale; by Ville's inequality, P(it *ever* exceeds 1/α) ≤ α. So you can
  **monitor continuously and stop at any time** — even on a data-dependent or
  unknown rule — without inflating false positives. Inverting them gives
  *confidence sequences*: intervals valid simultaneously at every sample size.

**When it beats fixed design.** Whenever the cost of evidence is real and you'd
otherwise either (a) over-sample to hit a pre-set n, or (b) "peek" at a fixed-n
p-value and stop early — which silently inflates the false-positive rate.
Always-valid methods are the *correct* way to do the plugin's "stop as soon as the
cheapest probe kills it" instinct without the statistical sin of optional stopping.
Trade-off: some conservativeness (less power at a fixed n) bought in exchange for
validity under arbitrary stopping and easy evidence combination.

**Slot into the campaign loop.** This is the missing **stopping rule** behind
"loop until clean" and behind step 0. (a) Per hypothesis: frame each as H0 (claim
false / null) vs H1 (claim true), accumulate evidence as a running log-likelihood
ratio across probes, and stop probing that hypothesis the moment it crosses a
pre-committed decisive threshold — formalizing FALSIFIED / CONFIRMED. (b) Across
the campaign: when evidence arrives incrementally (log streams, repeated samples,
agent waves), use the **optional-continuation** property of e-values — the product
of e-values from successive probes stays valid even when the decision to run the
next probe depended on the last one's result. This legitimizes the plugin's
inherently adaptive "found stuff → run another pass" loop, which under naive
p-values would be p-hacking. Note in artifacts.md that the replication convention
("reproduce on ≥3 independent items before calling it a pattern") is a crude
fixed-n version of this; an e-value martingale gives a principled adaptive count.

---

## 6. Bayesian experimental design / expected information gain

**What it is.** Choose the next experiment to maximize *expected information
gain*: the experiment whose outcome, in expectation, most reduces uncertainty
(entropy) about the unknown. Formally, expected info gain = expected KL divergence
of posterior from prior = **mutual information I(θ; y)** between the parameters
and the observation. Pick ξ* = argmax I(θ; y). Sequentially: after observing a
result, the posterior becomes the new prior and you re-select the next experiment
greedily by the same criterion. This is the unifying principle behind the
information-theoretic acquisition functions in §1 (entropy search, predictive
entropy search).

**When it beats fixed design.** When experiments differ wildly in how much they'd
*tell* you and you want max learning per unit cost. A fixed plan can spend a probe
that, whatever its outcome, won't change any decision — exactly what the plugin's
own rule warns against ("if an outcome wouldn't change what you do next, the
experiment is not worth running"). Expected-information-gain makes that rule
*quantitative and comparative*: rank candidate probes by expected bits, not just
binary keep/drop.

**Slot into the campaign loop.** Upgrade the pre-committed outcome→conclusion
table (step 2) into an information-gain estimate. The table already enumerates
each outcome and what it would prove; add a rough prior probability to each row
and you can compute which *hypothesis's* probe has the highest expected entropy
reduction — then run that one first. This is the precise, defensible form of
"reallocate probe budget toward the hypothesis with highest expected information
gain." It also sharpens the model council (Pattern D): when seats disagree, route
the crux to whichever probe maximizes expected information about the disputed fact,
rather than to whichever is merely cheapest.

---

## 7. Bayesian confidence updating vs the plugin's calibrated-confidence ladder

**What it is.** Update belief in odds form: **posterior odds = prior odds ×
likelihood ratio**, where LR = P(evidence | H) / P(evidence | not-H). Each piece
of evidence multiplies your odds by how *diagnostic* it is. This is anchored to a
base rate (prior), quantifies evidence by diagnosticity (not vividness), and
combines consistently (multiply LRs). Heuristic confidence, by contrast, neglects
base rates and trends overconfident. Calibration is *audited* after the fact by
the **Brier score** and its reliability term: across all claims you tagged "0.7",
the claim should hold ~70% of the time. The Brier score is a *strictly proper*
scoring rule — you minimize your expected score only by reporting your true belief,
so it can't be gamed by hedging.

**When it beats the current approach.** The plugin's confidence ladder (0.90+ for
ground truth, 0.55–0.75 for inference, never default to 0.85/0.95) is a good
*anti-overconfidence prior* but it is (a) not updated by an explicit rule as
evidence accumulates and (b) never scored for calibration, so there's no feedback
telling the system whether its 0.7s actually come true 70% of the time.

**Slot into the campaign loop.** Two adoptions, both cheap and high-leverage. (a)
**Make confidence updates explicit:** when a probe returns, state the likelihood
ratio it implies ("this evidence is ~5× more expected if H true than if false")
and multiply the prior odds, rather than jumping to a ladder rung. This makes the
verdict's confidence *auditable* — the number now has a derivation, matching the
plugin's existing demand that "a factor without evidence is rejected." (b) **Score
calibration over time:** because every hypothesis ends CONFIRMED / FALSIFIED /
INCONCLUSIVE with a confidence, the ledger is a ready-made calibration dataset.
Periodically compute the Brier reliability term across past verdicts; if the
plugin's 0.9s only come true 70% of the time, the ladder is miscalibrated and
should be retuned. This closes the loop the current method leaves open: it not
only *assigns* calibrated confidence but *verifies* the calibration empirically —
exactly the falsification-first stance applied to the method's own numbers.

---

## Adoption priority (highest leverage first)

1. **Expected-information-gain probe ordering (§6)** — turns the existing
   outcome→conclusion table into a quantitative "run the most informative probe
   next" rule. Smallest change, directly sharpens the core loop.
2. **Always-valid stopping / e-values (§5)** — gives "loop until clean" and
   "cheapest falsification first" a principled, peeking-safe stopping rule and
   legitimizes the adaptive "found stuff → another pass" loop.
3. **Successive-halving budget ladder (§4)** — formalizes tiered cheap→expensive
   probing and the verification/discovery tool split into a kill-the-bottom-half,
   reinvest-the-budget structure.
4. **Bayesian confidence updating + Brier calibration scoring (§7)** — makes the
   confidence ladder explicit (LR × prior odds) and empirically audited against
   the ledger's own history.
5. **Thompson-sampling allocation across competing hypotheses (§2)** — replaces
   implicit equal budget-splitting with adaptive concentration on live contenders.
6. **BO/SMBO acquisition ordering (§1)** and **random-vs-grid baseline (§3)** —
   the conceptual frame (surrogate + acquisition; random search as the honest
   baseline adaptive methods must beat) that unifies the above.

## Sources

- Bergstra & Bengio 2012, "Random Search for Hyper-Parameter Optimization",
  JMLR 13 — https://www.jmlr.org/papers/volume13/bergstra12a/bergstra12a.pdf
- Bayesian experimental design / expected information gain —
  https://en.wikipedia.org/wiki/Bayesian_experimental_design
- Thompson sampling & multi-armed bandits —
  https://en.wikipedia.org/wiki/Thompson_sampling
- Hyperparameter optimization (BO/SMBO, successive halving, Hyperband, BOHB,
  random vs grid) — https://en.wikipedia.org/wiki/Hyperparameter_optimization
- Sequential probability ratio test (Wald) —
  https://en.wikipedia.org/wiki/Sequential_probability_ratio_test
- E-values / anytime-valid inference / confidence sequences —
  https://en.wikipedia.org/wiki/E-values
- Brier score, calibration, proper scoring rules —
  https://en.wikipedia.org/wiki/Brier_score
