---
name: scientific-method
description: >-
  Use this skill whenever someone doubts a number, demands rigorous proof of a
  cause, or wants something invented and proven — any time a benchmark,
  metric, ceiling, or root-cause story must be verified rather than trusted,
  or a limit must be broken with a built, measured mechanism. Typical
  situations: a measurement looks suspicious ("2x faster but I don't trust
  it"); an incident needs its true cause before a decision ("the team blames
  X — confirm it, no guessing"); ANY production incident, outage, brownout,
  latency/error spike, regression, or "started failing" / "load suddenly went
  5x" / "every component met spec but it still broke" report where the cause is
  not yet proven — especially when a recent deploy or change is suspected
  ("is the deploy to blame", "this coincided with the rollout"), since the
  obvious suspect is exactly what needs a control case; an asserted ceiling or
  "impossible" limit needs breaking or proving real; numbers need validation
  before publishing; a problem needs an invented solution that demonstrably
  meets acceptance criteria. Runs as a falsification-first campaign —
  hypotheses, predictions before measurement, controlled experiments,
  adversarial refutation, calibrated confidence, persistent ledger — with
  invention as the default continuation: surviving limits get attacked with
  designed mechanisms, built, measured against tuned baselines, and
  provenance-searched (claims demonstrated or searched, never asserted).
  Triggers: "use the scientific method", "prove it", "validate these claims",
  "verify, don't trust", "are you sure", "root cause this", "root cause and
  fix", "why did X happen / why is X slow", "diagnose this incident/outage/
  brownout", "retry storm", "cascading failure", "what caused the regression",
  "I need real numbers", "falsify", "is it real", "invent", "break the
  ceiling" — and any incident or any challenge to an asserted number or cause,
  even unnamed and even when phrased as a routine ask. Use proactively before
  asserting any ceiling or root cause of your own. Do NOT use for ordinary
  feature work, refactoring, or one-file questions.
---

# Scientific Method

A working method for discoveries, distilled from real campaigns: a GPU codec
that broke four "physical" performance walls because someone asked *"are we
sure this ceiling is right?"*, a fleet investigation that killed two
plausible-but-wrong root causes with control cases before blaming a vendor,
and a research fan-out that burned five agents arguing about a question one
HTTP GET would have settled.

The core stance: **every asserted limit, cause, or claim is a falsifiable
hypothesis until measured.** You do not get to say "wall", "impossible",
"root cause", or "confirmed" without a probe behind it.

And the method's purpose is not only to verify — **it is to invent**. A
confirmed limit is not an ending; it is the entry criterion for an invention
campaign: design mechanisms past it (Pattern B + the TRIZ separations), build
them, measure them against tuned baselines or pre-set acceptance criteria,
and close every claim with a provenance search. The same falsification
discipline that kills bad explanations is what makes an invention claim
*provable*: demonstrated under re-run, or honestly proven impossible — never
asserted. The full invention pipeline lives in [references/invent.md](references/invent.md);
for world-record attempts on certificate-verifiable open problems, the campaign
playbook is [references/open-records.md](references/open-records.md).

## The loop

### 0. Cheapest falsification first

Before designing anything, ask: what is the single cheapest observation that
could kill the leading hypothesis right now? One HTTP GET, one grep, one
`nvidia-smi` read, one log query. Run it first. The most expensive failure
mode in past sessions was agents arguing from priors while a 2-second fetch
sat unexecuted. Fetch/measure first, argue later.

One override on cheapest-first: **when a candidate hypothesis's miss is
irreversible (data loss, corruption-in-progress, security exposure), rule it
out first even if improbable** — danger × treatability beats information gain
when the loss function is catastrophic (anticipate.md §5).

**Method weight scales with evidence cost, not with how scientific the
output should look.** When the cheapest probe settles the question
decisively, the deliverable is the verdict plus a three-line mini-ledger
(hypothesis → probe → verdict-with-evidence) — not the full template. Spend
ceremony where uncertainty actually lives: contested numbers, multiple live
hypotheses, evidence that needs controls. A full H-table and pre-registered
outcome matrix for a question one file-read answers is theater, and theater
erodes trust in the cases where the scaffolding is load-bearing.

### 1. Convert assertions into hypotheses

Sweep the problem statement, your own prior claims, and any inherited
documentation for assertions: "the ceiling is X", "the daemon causes Y",
"Z can't work". Each becomes a numbered, labeled hypothesis:

- **Falsifiable claim** with concrete numbers where possible ("the PCIe
  bidirectional aggregate is NOT 32.9 GB/s — that was a single-buffer
  artifact"), not a vague direction.
- **Explicit null hypothesis (H0)** — what the world looks like if the claim
  is wrong, stated just as concretely.
- Deliberately include the *reversed* hypothesis when one explanation is
  suspiciously convenient ("assume it's our fault and prove it" / "assume
  it's their fault and prove it"). Convenient explanations die under controls
  more often than not.

Record them immediately in the ledger (step 6) — hypotheses that live only in
conversation get silently mutated to fit results.

Sweeping existing assertions is induction's raw material; **generating
hypotheses nobody asserted is abduction, and it needs its own machinery**
([references/anticipate.md](references/anticipate.md)):

- **Key-assumptions check first:** classify the problem statement's
  assumptions solid/caveated/unsupported; every unsupported load-bearing one
  becomes a numbered hypothesis. "It worked before" is an assumption to
  verify, not a credential.
- **IS/IS-NOT specification** before hypothesizing on incidents: what is
  affected vs what plausibly could be but is NOT — a candidate cause must
  explain both columns (structure.md §4).
- For risky/irreversible changes, run the **pre-mortem FMEA** (anticipate.md
  §1); for broad sweeps, the coverage generators (category sweep, the
  unsafe-control-action taxonomy, TRIZ separations) replace intuition.
- **Whenever you design a mechanism — including a fix or a solution built to
  pass a goal — close with the provenance partition** (anticipate.md): every
  part tagged known (named), no-prior-art-found (search log), or unsearched.
  This applies in solution mode too, where it's easiest to skip: a fix that
  quietly reimplements weighted fair queuing should say so.

### 2. Predict before measuring

For each hypothesis, write the prediction and an **outcome→conclusion table**
*before* running anything:

| Outcome | What it proves | Next action |
|---|---|---|
| A: DRAM <35%, stalls on dependency chain | latency-bound — the "140 GB/s ceiling" is false | ILP is the lever |
| B: DRAM >70% near spec | genuinely bandwidth-bound — ceiling is real | stop optimizing the kernel |
| C: warps-active ~33% | occupancy-capped | raise launch bounds |

Every plausible outcome maps to a verdict and an action. If an outcome
wouldn't change what you do next, the experiment is not worth running. This
table is what stops post-hoc rationalization — you committed to what each
result means while you still didn't know the answer. It is a
**pre-registration**: timestamp it, and when reality forces a deviation,
add a dated scope correction rather than editing the prediction.

Two additions that sharpen the table:

- **State n up front.** How many runs, and why that many. A single run is an
  anecdote; verdicts report central tendency and spread, never a bare point.
- **Add a rough prior to each row.** With priors on the outcomes, the most
  informative probe falls out — run the probe expected to reduce the most
  uncertainty first, and re-rank the rest after every verdict
  ([references/rigor.md](references/rigor.md) §1).

### 3. Design controlled experiments

One isolated probe per hypothesis. Discipline that mattered in practice:

- **Name the confounds, then kill them.** GPU contention → run probes
  serially on a clean device. Page cache → O_DIRECT. Cross-contamination
  between test passes → tighten isolation each pass. Clock variance → lock
  clocks and state which mode the numbers are from. If you can't kill a
  confound, state it next to the number. The canonical blocking list —
  thermal state, cache warmth, background load, run-order drift (interleave
  A/B, never all-of-A-then-all-of-B), replication with reported spread — is
  in [references/rigor.md](references/rigor.md) §4.
- **Linear causal tools assume a linear system.** When every component met
  its spec and the loss still happened, when multiple controllers share
  state, or when the symptom oscillates or runs away — stop hunting a broken
  component and model the control loop; in delayed loops, the event just
  before the symptom is usually the loop feeding back, not the cause
  ([references/structure.md](references/structure.md)).
- **Controls are mandatory for causal claims** — this is the **but-for test**:
  would the effect have occurred without the cause? "Our playbook caused the
  outage" requires hosts where the playbook ran and nothing broke (negative
  control) and hosts where it never ran but things broke anyway. A
  correlation with no control case is a story, not a finding. Grade every
  causal verdict on the ladder — correlation → temporality → dose-response →
  controlled experiment — and say where it sits (rigor.md §3).
- **Prefer factorial over one-factor-at-a-time** when more than one factor is
  in play. OFAT cannot see interactions; two probes that disagree may be an
  unmodeled interaction, not a bad measurement.
- **Baselines before treatments.** Record the baseline number first; report
  every change as a signed delta against it. "11.63% → 12.22% (+0.59pp
  regression)" is honest; "around 12%" hides the regression. Name **guardrail
  metrics** at the same time — the things that must NOT regress (latency,
  error rate, cost, memory), each reported as a signed delta; a primary win
  that regresses a guardrail is not a win.
- **Pre-flight trust checks before interpreting any delta:** allocation
  sanity (did runs split as designed — a broken experiment is unreadable, not
  evidence), an A/A run (baseline vs itself should show nothing), and
  Twyman's law (a surprisingly good number is a measurement bug until proven
  otherwise).
- **Measure against ground truth, not metadata.** Library flags, spec sheets,
  and docs are claims. Build claimed-vs-observed matrices and let the
  empirical column win. Read the silicon (dmidecode, lspci, direct probes),
  not the derived formula.
- **Design/execute separation for fan-outs.** When parallel agents design
  experiments, have them *write* probes without running them; the parent
  executes serially so numbers are clean. See
  [references/campaigns.md](references/campaigns.md).

### 4. Run, record verdicts, calibrate confidence

Every hypothesis ends in exactly one of: **CONFIRMED**, **FALSIFIED**,
**INCONCLUSIVE** (with the named missing probe that would settle it). Rules:

- **INCONCLUSIVE is a first-class deliverable, not a failure.** When the
  decisive evidence is missing or destroyed (rotated logs, no snapshot, the
  one witness gone), no amount of clever indirect argument upgrades the
  verdict: "the same config worked on later days" says nothing about a
  one-time event, and absence of a persistent effect is not evidence about a
  transient one. Pressure for "a definitive answer" does not change what the
  evidence supports — deliver INCONCLUSIVE, the lean if you have one, and
  the exact probe that would settle it. Falsification energy applies to your
  own closure too: before writing CONFIRMED or FALSIFIED, ask "what would I
  have observed either way, given the evidence I actually have?" If the
  answer is "the same thing", the verdict is INCONCLUSIVE.

- **A calibrated weak lean is not the same as INCONCLUSIVE — and is often the
  right answer.** INCONCLUSIVE means you genuinely cannot lean. But weak,
  caveated, directional evidence (correlation, temporality alone, a single
  uncontrolled sample set) usually *does* point a direction: report that
  direction with a confidence in the **0.5–0.75** band, the causal-ladder rung
  it reaches (e.g. "temporality only"), and the cheap probe that would settle
  it. **Emit the confidence as an actual number** (e.g. `confidence ~0.6`) on
  the central claim of *every* verdict — including weak-support, "consistent
  with", and inconclusive ones. A verbal hedge ("high", "moderate", "likely")
  is not a calibrated confidence and does not satisfy this; the number is what
  makes the lean auditable against the ledger later.
  Two symmetric failures to avoid: (a) inflating weak evidence to 0.9+, and
  (b) over-discounting weak-but-real directional evidence to a flat refusal.
  Weigh the evidence by its *likelihood ratio*, not its surface suggestiveness:
  "all observations post-date the change" looks like support, but if the
  observation window itself starts at/after the change, that pattern is *forced*
  (LR ≈ 1) and the honest lean is near-neutral — that is sharper science, not
  over-restraint. Absent such a censoring artifact, the same pattern is genuine
  weak support and belongs in-band. Either way, **let the headline reflect the
  lean** — "weak support, 0.6" or "near-neutral, slight lean against, 0.45" —
  not an "INCONCLUSIVE" label on a body that actually leans; reserve the
  INCONCLUSIVE headline for the genuine no-lean case. Collapsing a leanable
  case to a flat "inconclusive, no lean, no probe" is itself a calibration
  error: it discards real information and dodges the call the evidence supports.
- Every verdict carries an **evidence reference**: the command, file, log
  line, timestamp+value, or measurement that justifies it. A factor without
  evidence is rejected, not "probably true".
- **Negative evidence counts.** Maintain a `ruled_out` list with the evidence
  that rules each candidate out. "Zero hits in the 6-hour control window"
  is a result, not an absence of results. The same goes for surprises:
  every anomaly gets a ledger record — explained, promoted to a hypothesis,
  or explicitly dispositioned — never silently dropped (the discrepancy that
  goes to chat instead of the ledger is how spacecraft get lost).
- **Simplification gate before any single-cause CONFIRMED:** does one cause
  explain both the IS and IS-NOT columns? Were the other factors shown
  *unnecessary*, or just less narratable? With ≥3 live hypotheses, prefer
  the ACH matrix — keep the hypothesis with the least evidence *against*,
  not the most support (structure.md §5). Tag every CONFIRMED with its
  evidence environment (`lab` / `relevant` / `operational`) — a sandbox
  confirm is not a production claim.
- **Confidence calibration:** 0.90+ requires direct ground-truth proof
  (binary disassembly, silicon probe, reproduced on demand) — and for
  *causal* claims, temporality plus a control case as well. 0.55–0.75 is
  plausible inference. Never default to 0.85/0.95, and never report 1.0
  while a named unknown remains — but there is no magic ceiling either:
  direct, reproduced, structural evidence can honestly earn 0.98–0.99, and a
  real residual can honestly cost you down to 0.85. The number comes from
  the evidence, not from a safe-sounding convention. A confidently-wrong
  verdict anchors everyone downstream to a bad hypothesis; it is strictly
  worse than saying "inconclusive, next probe is X".
- **Derive confidence, don't pick it.** When a probe returns, state the
  likelihood ratio it implies ("~5× more expected if H than if not-H") and
  update the prior odds — the number gets a derivation, like every other
  claim. Watch for a house number: if every verdict lands on the same value
  (0.95, 0.97), you are templating, not estimating — evidence of different
  strengths must produce different numbers, and the residual must name a
  *specific* unknown, not a boilerplate caveat. Even among strong verdicts,
  let the residual's severity set the gap: a reproduced-on-demand control
  with a cosmetic residual is not the same number as a single-pass inference
  with an untested environment assumption. The ledger's own history is
  a calibration dataset: check periodically whether past 0.7s held ~70% of
  the time, and retune the ladder when they don't (rigor.md §5).
- Tag every claim **verified** (testable from evidence in hand, with the
  reference) or **discovery** (a hypothesis needing a probe you haven't run).
  Every discovery claim must end with the exact next probe — the specific
  query/command that would verify it.

### 5. Adversarial verification before trusting findings

A finding you produced is a hypothesis someone else hasn't tried to kill yet.
Before acting on it or reporting it as fact:

- Spawn the plugin's `refuter` agent (or apply its rubric inline): try to
  **refute the finding first**, then judge what survives. Does it actually
  beat the measured baseline, or secretly still pay it? Is the per-component
  win also an end-to-end win? Default to the lower verdict when uncertain.
- Verdict enum: `confirmed` / `prototype` (promising, needs one more
  measurement) / `research` (real but speculative) / `kill` — with a
  `kill_reason`.
- For findings sourced from research agents or the web: verify before
  relaying. Fetch the primary source yourself. One agent catching another's
  hallucination via contradiction (star counts that disagree by 5x) saved a
  past session; the same check costs seconds.

### 6. Persist the ledger

Write findings to a durable artifact in the repo (default
`EXPERIMENTS.md`, or the project's incident/docs convention) — not just the
conversation, which gets compacted. The ledger's size tracks the campaign's
*uncertainty*, not its importance: a question settled by one decisive probe
gets the three-line mini-ledger; the full structure below is for campaigns
with multiple live hypotheses. The ledger holds:

- The hypothesis table: `| # | Hypothesis | Prediction | Probe | Verdict |`
- A **falsification log**: every dead end with the evidence that killed it,
  marked **DO-NOT-RE-ATTACK** so no future session re-litigates it.
  "This codec is the residue of a falsification campaign" — the kills are
  the moat.
- A **Reproduce** block: copy-paste commands that regenerate the key numbers,
  under a **provenance header** — commit hash, machine identity, env/toolchain
  versions, input files with hashes, date. A headline number pinned to a
  commit can be re-verified months later; "ran the benchmark" cannot, and a
  DO-NOT-RE-ATTACK entry pinned to a commit can't be quietly re-litigated.
- **Scope corrections** when you retract a claim: keep the wrong version
  visibly struck through with the correction dated. Hiding retractions
  destroys the audit trail that makes the verdicts trustworthy.

Templates: [references/artifacts.md](references/artifacts.md).

### 7. Loop until clean

A found defect means the search was incomplete — run another pass. Stop only
when a full pass produces no new findings (dry), every hypothesis has a
verdict, and every INCONCLUSIVE names its missing probe. "You found stuff,
which means there could be more masked issues — always do more backtesting
until clean."

A dry pass only counts if the generator was varied: before declaring dry,
cycle the abduction modes — logical, analogical, recombinative,
probabilistic (anticipate.md §4). And before any irreversible step, one
**second-order pass**: what loop does the fix feed back into, what's its
expected long-term sign, what guardrails watch the fix itself
(structure.md §6)? Close the campaign with a short after-action review —
intended vs actual, why, sustain/improve — and log **opened questions**
and **reopen tripwires** in the ledger; verdicts should generate the next
campaign, not just end this one.

Two statistical guards on this loop (rigor.md §2):

- **Peeking rule.** Re-checking a metric until it looks significant inflates
  the false-positive rate. Fix n in advance or use an always-valid sequential
  stopping rule — and discount the magnitude of anything stopped early
  *because* it crossed the threshold (early stops are biased large).
- **Budget ladder.** Structure passes as successive halving: every hypothesis
  gets the cheapest falsifier first; only survivors earn the expensive
  controlled probe. Kill the bottom half each rung, reinvest the budget.

Before any irreversible step (going live, sending the vendor report,
publishing the benchmark): one final adversarial review pass against the
ledger, plus a staged rollout (dry-run/canary) where the domain allows it.

## Scaling up: multi-agent campaigns

For campaigns with many hypotheses (breaking performance ceilings, fleet
forensics, "figure it all out" investigations), fan out one agent per
hypothesis with the design/execute split, then a refute wave, then synthesis.
Prompt templates, structured-output schemas, and Workflow scripts are in
[references/campaigns.md](references/campaigns.md) — read it before spawning
agents so the deliverable contract and verdict schema are consistent.

Two escalation gates sit above the refute step, and both are correction
loops — their feedback gets applied to the work during the round, not filed:

- **Model council** (judgment calls: design choices, ambiguous results,
  go/no-go): the same question posed independently to 3-5 seats on
  *different models* (plus an out-of-family local-LLM seat when available),
  blind to each other. Same-model replicas share blind spots; diverse seats
  decorrelate them. Aggregate by evidence not votes; unanimity with no
  probes behind it is a shared prior, not a conclusion. Factual
  disagreements are never voted on — the crux becomes a ledger hypothesis
  with a probe, and the data rules. Surviving counterarguments become
  immediate corrections.
- **Peer review** (inventions/findings that survived refutation, before
  build/merge/publish): 3-5 blind reviewers with distinct lenses
  (soundness, prior-art, reproducibility, significance, fatal-flaw) who must
  *execute* — run the Reproduce block, actually search prior art — then a
  rebuttal answered only with new evidence or applied revisions, re-scores,
  and an area-chair decision that weighs evidence over vote counts. The
  decision maps straight to the ledger (accept→CONFIRMED,
  reject→falsification log with DO-NOT-RE-ATTACK).

Pattern D and E in references/campaigns.md carry the full contracts; the
`/scientific-method:council` and `/scientific-method:peer-review` commands
run them end to end.

## Failure modes this method exists to prevent

- **Asserting derived numbers as physical facts.** A "16.4 GB/s wall"
  computed as 32.9/2 from one flawed test gated weeks of work; a real
  measurement already exceeded it. Derived ceilings are hypotheses.
- **Premature closure.** "We're done, nothing left to squeeze" and "no, we
  didn't invent anything" both got reversed under one more falsification
  pass. Declare done only from a dry pass, not from fatigue.
- **Arguing from memory/priors instead of measuring.** The cheapest probe
  beats the smartest argument.
- **Manufactured closure under verdict pressure.** "The postmortem needs a
  definitive answer" is not a reason one exists. When the decisive evidence
  is gone, a confident verdict built from indirect inference is the
  confidently-wrong failure this method exists to prevent — hold at
  INCONCLUSIVE and name the probe.
- **Blaming the convenient party.** Both "it's our fault" and "it's their
  fault" need control cases before either is filed.
- **Crowning one of two jointly-necessary factors "the root cause."** When
  the evidence shows neither factor sufficient alone and both necessary,
  the headline must say exactly that — demoting one to "contributing
  trigger" is single-cause bias sneaking back in through the narrative.
- **Quietly absorbing a regression.** Baselines and signed deltas, always —
  and pinned to the *origin* baseline across campaigns: per-campaign deltas
  can each look acceptable while the baseline walks (normalization of
  deviance).
- **Stopping at "human error."** A terminal human-error verdict is almost
  always hindsight bias — the real question is what made the erroneous
  action look reasonable at the time.
- **"It's complex" as a terminal verdict.** Loops, emergence, and joint
  causation change which hypotheses exist, never the standard of proof —
  every complexity move ends in a probe or a named-probe INCONCLUSIVE.
