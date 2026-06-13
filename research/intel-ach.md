# Intelligence-analysis tradecraft → scientific-method plugin

Research notes + concrete plugin adoptions. Sources: Heuer, *Psychology of
Intelligence Analysis* (CIA, ch. 8 ACH); Wikipedia (ACH, pre-mortem, Tetlock);
CIA *Tradecraft Primer* (SATs); Klein (HBR 2007 pre-mortem); Tetlock & Gardner,
*Superforecasting*. The CIA-hosted PDFs 403 to automated fetch — claims below
are cross-checked against Wikipedia's summaries of the same primary texts.

---

## 1. Distilled principles

### Analysis of Competing Hypotheses (ACH) — Heuer's 7(/8) steps

1. **Enumerate hypotheses** — brainstorm the *full* set first (incl. diverse /
   unwelcome ones), before looking at evidence. Picking a lead hypothesis and
   hunting confirmation is the failure mode ACH exists to break.
2. **List evidence & arguments** — for and against *each* hypothesis; include
   assumptions and absent evidence ("the dog that didn't bark").
3. **Build the matrix; work across rows, not down columns** — evidence on
   rows, hypotheses on columns. For each *piece of evidence*, mark Consistent /
   Inconsistent / Not-Applicable against *every* hypothesis. Heuer calls this
   the most important step. Working across one evidence item at a time (vs. one
   hypothesis at a time) is the structural trick that defeats confirmation bias.
4. **Refine** — redraw: drop evidence/assumptions with no diagnostic value, add
   hypotheses, fill gaps.
5. **Draw tentative conclusions by trying to DISPROVE** — rank by *inconsistency*.
   **You keep the hypothesis with the least evidence AGAINST it — not the most
   evidence FOR it.** Confirmation is cheap (one datum can be consistent with
   many hypotheses); only inconsistent evidence has eliminative power. The
   surviving hypothesis is the one evidence has failed to refute.
6. **Sensitivity analysis** — for the few "linchpin" evidence items driving the
   conclusion, ask: what if this is wrong / deceptive / misinterpreted? A
   verdict resting on one fragile datum is unsound. Flag where deception would
   hurt most.
7. **Report all hypotheses** — state relative likelihoods, *why* rivals were
   rejected (not just why the winner won), and the **milestones/indicators** to
   watch that would signal the conclusion is going wrong.

**Diagnosticity** is the load-bearing concept: evidence consistent with *every*
hypothesis is worthless for discrimination, however "important" it feels.
Diagnostic value = how many hypotheses a datum is *inconsistent* with. Prioritize
collecting high-diagnosticity evidence; deprioritize the rest.

**Known limits (van Gelder, social-constructivist critiques):** ACH can't
fabricate the hypothesis you never thought of (garbage-in); treats evidence
items as independent when they're often correlated; is a static snapshot;
demands many low-value pairwise judgments at scale; empirical support for "it
debiases" is weak. Treat it as scaffolding for judgment, not a verdict oracle —
the matrix total must not overrule a reasoned analyst.

### Structured analytic techniques (SATs)

- **Key Assumptions Check** — list every assumption the current line of analysis
  rests on (explicit *and* implicit); challenge each: *why must this be true?
  what if it's false? could it have been true once but not now?* Classify each
  as **solid / correct-with-caveats / unsupported-or-questionable**. Unsupported
  load-bearing assumptions become the priorities to test.
- **Devil's advocacy / Red team** — assign someone to build the strongest case
  *against* the consensus, or to reason as the adversary does (defeats
  mirror-imaging — assuming the other side shares your values/logic).
- **What-if analysis** — assume a surprise event *has already happened*, then
  reason backward to plausible paths that produced it (frees you from "it
  can't happen here").
- **High-impact / low-probability** — explicitly analyze the tail outcome that's
  being dismissed as unlikely, because the cost of being wrong is asymmetric.
- **Indicators / signposts of change** — *before* events unfold, define a list of
  observable, concrete things that, if seen, would show which scenario is
  emerging (or that your lead conclusion is breaking). Pre-committing the
  indicators stops post-hoc rationalization and turns monitoring into a
  tripwire, not a vibe.

### Klein's pre-mortem

Before committing, assume the project *has already failed* — state it as fact,
then have everyone independently write down what killed it. Reframing failure
from hypothetical ("what might go wrong") to assumed-fact ("what did go wrong")
licenses candid dissent, breaks groupthink, and exploits **prospective
hindsight** (people generate ~30% more, more-specific causes when imagining a
fact vs. a possibility). Counters overconfidence and the planning fallacy. The
mirror image of a post-mortem, run while you can still act.

### Tetlock — superforecasting

- **Fox > hedgehog.** Hedgehogs force everything through one big idea and do
  *worse*, especially on long-horizon calls in their own specialty; foxes
  aggregate many partial models, are self-critical, and update. Media fame
  correlates *inversely* with accuracy.
- **Granular probabilities.** Top forecasters distinguish many gradations across
  0–1 (e.g. 63% vs. 68%), not a 7-word verbal scale. Vague words ("likely")
  hide disagreement and dodge scoring.
- **Frequent updating in small increments.** "Incremental belief updaters are
  better forecasters" (Atanasov et al. 2020) — but balance: don't under-react
  to real news, don't over-react to noise.
- **Fermi-ize.** Break an intractable question into tractable sub-questions and
  estimate each.
- **Outside view first.** Anchor on the base rate of the reference class, *then*
  adjust for case specifics (inside view).
- **Keep score (Brier), admit error, change course.** Calibration is trained by
  scoring; accountability improves it.

---

## 2. Concrete plugin adoptions

The plugin currently evaluates hypotheses **one at a time** (each gets its own
probe → CONFIRMED/FALSIFIED/INCONCLUSIVE). ACH adds a *cross-hypothesis*
verdict mechanism that is structurally different and, when several live
hypotheses share evidence, superior. Three adoptions, in priority order.

### A. ACH evidence×hypothesis matrix — a new verdict mechanism for multi-hypothesis campaigns

**When to use:** any campaign with ≥3 live hypotheses competing over a *shared*
body of evidence (forensics, "what's the root cause", ambiguous-result
interpretation). When one cheap probe settles it, skip this — same
cost-scaling rule the SKILL already states.

**The mechanism (drop-in to SKILL §4 "Run, record verdicts"):**

> When multiple hypotheses survive their individual probes, do not pick by
> "most evidence for". Build the matrix: **evidence on rows, hypotheses on
> columns.** For each evidence item, score it against *every* hypothesis —
> `C` (consistent), `I` (inconsistent), `–` (n/a). Work **across each row**
> (one evidence item vs. all hypotheses), never down a column. Then:
>
> 1. **Drop non-diagnostic rows.** Any evidence item that is `C` for every
>    surviving hypothesis discriminates nothing — strike it, however
>    intuitively important. Diagnosticity = count of `I`s in the row.
> 2. **Rank columns by inconsistency, ascending.** Tally the `I`s per
>    hypothesis. **The verdict is the column with the FEWEST `I`s — least
>    evidence against — not the most `C`s.** A single hard `I` can eliminate a
>    hypothesis; a stack of `C`s cannot confirm one.
> 3. **Sensitivity pass.** Identify the linchpin evidence — the few rows whose
>    flip would change the ranking. For each, ask: could it be wrong,
>    mismeasured, or planted? A verdict resting on one fragile/`I`-deciding row
>    is INCONCLUSIVE until that row is hardened. (This is the existing
>    "what would I have observed either way?" test, applied per-row.)

**Matrix template** (add to `references/artifacts.md`):

```
Diagnosticity: count of I per row. Verdict: hypothesis with FEWEST I (not most C).

| Evidence                    | H1 | H2 | H3 | diag |
|-----------------------------|----|----|----|------|
| E1 log shows X at T0        | C  | I  | C  | 1    |
| E2 control host clean       | I  | C  | I  | 2    |  ← high diagnosticity
| E3 metric elevated globally | C  | C  | C  | 0    |  ← strike, non-diagnostic
|-----------------------------|----|----|----|------|
| Inconsistency (I count)     | 1  | 1  | 2  |      |
| ⇒ keep H1/H2 (1 I each), H3 weakest. Break tie w/ a probe, not a vote.   |
```

**Why it's better than one-at-a-time here:** isolating each hypothesis lets a
convenient story collect confirmations and look strong. ACH forces every datum
to testify against *all* rivals at once, so a hypothesis only "wins" by
surviving refutation relative to its competitors — the same falsification-first
stance the plugin already takes, extended to the *comparative* case. Ties are
not resolved by vote or matrix arithmetic — they become the next ledger
hypothesis with a diagnostic probe (consistent with Pattern D: "never vote
facts").

### B. Key-Assumptions Check as an explicit campaign step

Add as **step 1.5** (between "convert assertions into hypotheses" and "predict
before measuring") and as a line in the ledger:

> **Key-assumptions check.** Before predicting, list every assumption the
> campaign's framing rests on — including the ones inherited silently from the
> problem statement, the tooling, or "everyone knows". For each, classify:
> **solid** (evidence in hand) / **caveated** (true under stated conditions) /
> **unsupported** (load-bearing but untested). Every *unsupported, load-bearing*
> assumption is promoted to a numbered hypothesis with its own cheapest-falsifier
> probe. This is where "measure against ground truth, not metadata" gets its
> worklist: spec sheets, library flags, and "the daemon obviously does X" are
> assumptions until probed.

Ledger gets an **Assumptions** block: `| assumption | load-bearing? | status |
| probe-if-unsupported |`. Catches the failure mode where the whole H-table is
built on a false premise nobody wrote down.

### C. Indicators / signposts — monitoring after a verdict

Add to SKILL §6 (ledger) and §7 (loop until clean): a CONFIRMED verdict is a
snapshot, not a permanent truth (ACH's static-matrix limitation made concrete).

> **Signposts block.** When you close a campaign with a verdict, write the
> observable indicators that would show the verdict is **going wrong** — the
> specific log line, metric threshold, alert, or recurrence that, if seen later,
> reopens the ledger entry. Pre-commit them *now*, while reasoning is fresh and
> before any motivated interpretation. This converts "CONFIRMED" from a
> full-stop into a tripwire and gives DO-NOT-RE-ATTACK a defined reopen
> condition (the SKILL already asks for "reopen condition" on rejects — this
> generalizes it to every verdict).

Ledger template addition:

```
| verdict | confidence | signpost (what reopens this) | where to watch |
|---------|-----------|------------------------------|----------------|
| H2 CONFIRMED | 0.9 | error rate >0.5% returns on prod | grafana panel X |
```

### D. Smaller borrowings (fold into existing sections, no new structure)

- **Pre-mortem before irreversible steps.** SKILL §7 already requires "one final
  adversarial review before going live". Sharpen it: phrase as Klein's
  pre-mortem — "assume the rollout/vendor-report/published-number **has already
  failed**; each reviewer writes what killed it" — not "what might go wrong".
  Prospective-hindsight framing surfaces ~30% more failure modes. Pairs
  naturally with the existing `refuter` agent.
- **Granular, scored confidence (Tetlock).** Reinforces the SKILL's existing
  "derive confidence, don't pick it / watch for a house number" rule: forbid
  verbal-only confidence, require a number, and use the ledger's history as a
  Brier-style calibration set (the SKILL already says "check whether past 0.7s
  held ~70%" — name it: this is calibration scoring).
- **Outside view first / Fermi-ize.** Before the inside-view probe, state the
  base rate of the reference class ("how often is the vendor actually at
  fault?") and decompose the question into sub-questions — complements the
  existing prior-on-each-row guidance in step 2.
- **Fox stance** is already the plugin's implicit ethos (many hypotheses,
  self-refutation, frequent updates). Worth one explicit line in "failure modes":
  *the hedgehog failure — forcing every campaign through one favored root-cause
  story — is single-cause bias, which the SKILL already names.*
