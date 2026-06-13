# Diagnosis, OODA, and AAR — frameworks for the scientific-method plugin

Three decision-and-diagnosis traditions from medicine and the military, distilled
into principles and concrete plugin adoptions. The throughline: each is a
falsification-first discipline that long predates this plugin, and each names a
specific failure the plugin currently under-handles.

Sources (all fetched, primary/encyclopedic): Wikipedia *Differential diagnosis*,
*Likelihood ratios in diagnostic testing*, *List of cognitive biases*, *OODA loop*,
*After-action review*; Boyd, *The Essence of Winning and Losing* (PDF binary —
orientation framing below is flagged as established secondary knowledge, not
extracted quotes).

---

## Part 1 — Clinical differential diagnosis (DDx)

### Distilled principles

1. **Coverage before precision.** Step one is generating the candidate list; "if
   an important candidate is missed, no method yields the right answer." Clinicians
   use category-sweep mnemonics (VINDICATEM: Vascular, Inflammatory/Infectious,
   Neoplastic, Degenerative/Drugs, Idiopathic/Iatrogenic, Congenital, Autoimmune,
   Traumatic, Endocrine, Metabolic) to force breadth so no class of cause is
   silently omitted. The list should "account for as much of the total probability
   as possible," including a "no abnormality" candidate.

2. **Probability-weight the list, two ways.**
   - *Epidemiologic (prior):* for each candidate estimate the chance it "would have
     occurred in the first place in this individual" = population prevalence ×
     risk-factor relative risk × rate the condition produces this presentation, then
     normalize across candidates to shares of 100%.
   - *Likelihood-ratio (update):* convert pre-test probability to odds, multiply by
     the test's LR, convert back; each post-test probability becomes the next test's
     pre-test probability. This is sequential Bayesian updating, candidate by candidate.

3. **Test to discriminate, not to confirm.** Pick the test by *what its result will
   change*, not by what you hope it shows:
   - High-**specificity** test on the front-runner → large LR+ → **SpPin** (rules it
     *in*, drives competitors down).
   - High-**sensitivity** test on rivals → very low LR− → **SnNout** (a negative
     pushes them to "negligible levels," ruling them *out*).
   - LR rules of thumb: LR+ > 10 ≈ +45% probability (strong rule-in); LR− < 0.1 ≈
     −45% (strong rule-out); LR near 1 adds nothing — don't run that test.
   - Stop at the **endpoint**: when one diagnosis is so certain that no available
     test would change the action plan. (Identical to the plugin's "if an outcome
     wouldn't change what you do next, the experiment isn't worth running.")

4. **Rule out the killers first — danger overrides probability.** The procedure aims
   "at least to consider any imminently life-threatening conditions." A clinician may
   prioritize by *most likely* (probabilistic), *most serious if missed* (prognostic),
   or *most treatable* (pragmatic). In the canonical worked example, cancer is tested
   **despite lower probability** because missing it is life-or-death — and its rule-out
   threshold is made *more stringent* than probability alone would justify. In
   emergencies, fixed protocols (ABC: airway, breathing, circulation) preempt
   calculation entirely.

5. **Ruling out is a first-class result.** Probabilities never hit 0/100%; "ruling
   out" means driving a candidate to negligible probability — sometimes merely via
   *absence* of expected positive findings, not a dedicated negative test. Mirrors the
   plugin's `ruled_out` list and "negative evidence counts."

6. **Named diagnostic errors** (from the bias literature, mapped to diagnosis):
   - **Anchoring** — over-relying on the first impression / earliest data, failing to
     adjust as new findings arrive.
   - **Premature closure** — accepting the first plausible diagnosis and stopping the
     search (kin to *conservatism bias*: under-revising belief on new evidence). The
     plugin already names this exact failure mode.
   - **Confirmation bias** — seeking/weighting evidence that supports the leading
     hypothesis, discounting contradictions. (Congruence bias: testing only your own
     hypothesis directly, never the alternatives.)
   - **Availability** — recent/vivid/memorable cases feel more probable than they are.
   - **Search satisficing** — stopping after the first satisfactory finding (e.g.
     finding one fracture and missing the second).

### Concrete plugin adoptions

**A1. The hypothesis table IS a differential.** Reframe the H-table (`SKILL.md` §6,
`| # | Hypothesis | Prediction | Probe | Verdict |`) explicitly as a differential
diagnosis: add a **prior** column (already hinted at in §2 "rough prior to each row")
and require the list to be *generated for coverage first*. Adopt a lightweight
category sweep as the plugin's VINDICATEM — for engineering root-cause that is
roughly: *config / data / dependency / concurrency / resource-limit / environment /
our-code / their-code / measurement-artifact*. Forcing a sweep is the structural cure
for premature closure: you cannot close on candidate #1 if the method made you
enumerate the class.

**A2. Test-to-discriminate column.** For each probe, record not just the prediction
but *which competing hypotheses this probe's outcome separates* — the SpPin/SnNout
logic. A probe whose every outcome leaves the ranking unchanged is an LR≈1 probe:
flag it as theater and cut it. This sharpens §2's outcome→conclusion table from
"what does each outcome prove" to "which rival does each outcome kill."

**A3. Calibrate confidence as explicit Bayesian update.** The plugin already says
"derive confidence, don't pick it … state the likelihood ratio it implies (~5× more
expected if H than not-H) and update the prior odds." Medicine gives the exact
machinery: `posttest_odds = pretest_odds × LR`. Adopt the three-line update
(pretest odds → ×LR → posttest probability) as the *standard derivation format* for
every confidence number, so the ledger shows the arithmetic, not a vibe.

**A4. The danger×treatability override — the headline new principle.**
The plugin orders probes by **information gain** (successive halving, cheapest
falsifier first, "run the probe expected to reduce the most uncertainty first").
Medicine orders by **danger × treatability** ("rule out the killers first even if
improbable"). These conflict, and the plugin should state when each wins:

> **Probe-ordering rule.** Default to information gain (max uncertainty reduction
> per unit cost). **Override** and probe a low-probability hypothesis first when its
> *cost-if-true-and-missed* is catastrophic **and** it is cheaply ruled out (high
> danger × high treatability × low probe cost). Order by **danger × treatability ÷
> probe-cost**, not by probability, for any hypothesis whose miss is irreversible.

Decision rule for which regime applies:
- **Information-gain wins** when outcomes are *reversible* and *comparable in cost* —
  ordinary investigation, no outcome is catastrophic. Most plugin campaigns.
- **Danger-first wins** when one hypothesis, *if true and acted on wrongly*, causes an
  **irreversible** loss (data destruction, shipping a silent-corruption bug, a
  vendor-blame report that's wrong, a force-push). Then you rule it out *first* even at
  1% prior, and you make its rule-out threshold *more stringent* (clinicians demand a
  bigger LR to clear a can't-miss diagnosis). This is the "catastrophic hypothesis
  override."
- **Worked translation:** before a destructive or irreversible step (the plugin's
  §7 "before any irreversible step"), the *last* probe ordering is danger-first
  regardless of priors — the engineering analogue of running ABC before diagnosis.
  "Could this delete data / corrupt output / blame the wrong party?" is probed to a
  stringent rule-out *before* the cheap-but-low-stakes hypotheses, even though
  information-gain would have deferred it.

The two orderings are the same Bayesian object weighted by different loss functions:
information gain minimizes *expected probes*; danger-first minimizes *expected
catastrophic loss*. The plugin should carry both and name the loss function in play.

---

## Part 2 — Boyd's OODA loop

### Distilled principles

1. **Four phases, iterated:** Observe → Orient → Decide → Act, run as a continuous
   cycle with feedback, not a one-shot pipeline. Observation and orientation are
   *continuously re-updated* from feedback rather than fixed at the start.

2. **Orientation is the contested resource — the schwerpunkt.** It is not one of four
   equals; it is the lens through which all observation is filtered and from which
   decisions and actions flow. Orientation is an interactive composite of *genetic
   heritage, cultural traditions, previous experience, new information,* and a running
   process of *analysis and synthesis*. Two analysts observing identical data decide
   differently because their orientation differs. **The fight is over whose model of
   the situation is correct, not over who has more data.**

3. **Tempo: get inside the adversary's loop.** Agility beats raw power. Cycling
   Observe→Act faster than the opponent generates *mismatches* between their model and
   unfolding reality, producing confusion, disorder, and eventual collapse of their
   ability to respond coherently. Feedback enables **late commitment** — you defer the
   decision until the last responsible moment, keeping options open (explicitly
   contrasted with PDCA's early commitment).

4. **Implicit guidance and control.** A well-oriented actor connects orientation
   directly to observation and action, acting intuitively without slow explicit
   deliberation — fast *because* the orientation is good, not because steps were skipped.

### Concrete plugin adoptions

**B1. "Orientation as the contested resource" = the plugin's anti-prior stance.**
Boyd's central claim — the fight is over whose *model* is right, not who has more data
— is precisely the plugin's "arguing from memory/priors instead of measuring." Adopt
Boyd's vocabulary: when agents disagree, the disagreement is an **orientation
mismatch**, and the resolution is not debate but a probe that *forces re-orientation*
on whoever's model is wrong. This is already the council rule ("factual disagreements
are never voted on — the crux becomes a ledger hypothesis with a probe"); Boyd gives
it a name and a why.

**B2. Tempo / cheapest-falsification-first is OODA tempo.** §0 ("the most expensive
failure mode was agents arguing from priors while a 2-second fetch sat unexecuted") is
literally *failing to get inside your own loop*. Frame the cheapest-falsifier rule as:
**maximize observe→orient cycles per unit time**; an unexecuted cheap probe is a stalled
OODA loop. A campaign that fans out five agents to argue is *slower* than one that runs
the GET — fewer real orientation updates per hour.

**B3. Late commitment = INCONCLUSIVE as a first-class verdict.** Boyd's "defer the
decision until the last responsible moment, keep feedback flowing" is the strategic
justification for the plugin's refusal to manufacture closure. Holding at INCONCLUSIVE
and naming the next probe *is* late commitment: you keep orienting rather than locking
a decision the evidence can't yet support.

---

## Part 3 — After-Action Review (AAR)

### Distilled principles

1. **Intended vs. actual is the spine.** An AAR "begins with a clear comparison of
   intended versus actual results" — this is what distinguishes it from a debrief. The
   four questions: *(1) What did we intend / expect? (2) What actually happened? (3)
   Why the difference? (4) What do we sustain and what do we improve?*

2. **No-fault / non-attribution is structural, not polite.** "Assigning blame or
   issuing reprimands is antithetical to the purpose of an AAR." Prerequisites: a safe
   private setting, dedicated time, and **assumed equality of everyone present**. The
   review is forward-looking; blame suppresses the honest reporting the review needs.

3. **Tight focus on participants' own actions.** Unlike a post-mortem, an AAR does not
   produce recommendations for outside parties — participants carry their own learning
   forward. In large operations AARs *cascade*: each level reviews its own performance.

4. **Formal vs. informal.** Informal = team-leader-led, short-cycle, run in the flow of
   work. Formal = trained facilitator/"AAR Conductor," chronological or focused on a few
   key issues, safe setting, dedicated time.

### Concrete plugin adoptions

**C1. AAR is the post-campaign retro — adopt the four-question structure directly.**
The plugin has a *during-campaign* ledger but no *after-campaign* retro. Add an
**After-Campaign Review** as a final artifact (or a `/scientific-method:aar` command),
structured exactly:

| Question | Plugin instantiation |
|---|---|
| **What did we intend?** | The pre-registered outcome→conclusion tables and the priors stated in §2, *as written before measuring*. |
| **What actually happened?** | The verdicts (CONFIRMED/FALSIFIED/INCONCLUSIVE) and the headline numbers, as they landed. |
| **Why the difference?** | Where predictions missed: which priors were miscalibrated, which confounds went unnamed, which probes were LR≈1 theater. |
| **Sustain / improve?** | What discipline to keep; which checklist item to add next time. Feeds the calibration-dataset retune (§4: "check whether past 0.7s held ~70% of the time"). |

**C2. The pre-registration is what makes the AAR possible.** The plugin's §2
pre-registration (timestamped outcome→conclusion table, "add a dated scope correction
rather than editing the prediction") is precisely the *intended* column an AAR compares
against. Without it there is no intended-vs-actual; with it the retro writes itself.
This is the strongest mutual reinforcement between the two frameworks — make the link
explicit in SKILL.md.

**C3. No-fault structure for the council/peer-review and the cross-agent retro.** When
a campaign ran multi-agent (council, peer-review, refute waves), the AAR reviews *the
process* — which agent's orientation was wrong and why — under non-attribution: the
goal is calibrating the *method* (better probe ordering, better priors), never grading
an agent. "Assumed equality of everyone present" maps to: a junior probe that killed a
senior hypothesis is exactly the win the structure exists to surface.

**C4. Sustain/improve feeds the calibration dataset.** The "improve" answers are not
prose — they become concrete ledger-method changes: a new entry in the danger-first
override list, a confound added to the standing blocking list (rigor.md §4), a retuned
confidence ladder. The AAR is the mechanism by which the plugin's own history (§4 "the
ledger's own history is a calibration dataset") actually gets applied.

---

## Synthesis — what each tradition adds that the plugin lacked

- **DDx:** a *coverage-forcing* list-generation step (cure for premature closure), and
  the **danger × treatability** probe-ordering override that competes with pure
  information-gain. The plugin had Bayesian updating; medicine supplies the loss
  function that says when to probe the improbable-but-catastrophic first.
- **OODA:** the vocabulary of *orientation as the contested resource* (disagreements
  are model mismatches resolved by probes, not data volume or debate) and *tempo*
  (cycles-per-hour as the real metric; late commitment justifies INCONCLUSIVE).
- **AAR:** the missing *after-campaign* artifact — intended-vs-actual retro under
  no-fault structure, made possible by the plugin's existing pre-registration, closing
  the loop back into confidence-ladder calibration.
