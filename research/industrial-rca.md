# Industrial Root-Cause-Analysis Frameworks & Their Critiques

Research for the `scientific-method` plugin. Goal: mine 60 years of industrial RCA
practice for structured tools the plugin lacks — chiefly **Kepner-Tregoe IS/IS-NOT
differencing** — and reconcile the "find the root cause" tradition with the modern
complex-systems critique that **root cause is a construct**, without losing the
plugin's decisive CONFIRMED/FALSIFIED/INCONCLUSIVE verdicts.

Sources fetched (primary where reachable):
- 5 Whys — en.wikipedia.org/wiki/Five_whys (Minoura, Card *BMJ Q&S* 2017 critiques)
- Ishikawa — en.wikipedia.org/wiki/Ishikawa_diagram
- 8D — en.wikipedia.org/wiki/Eight_disciplines_problem_solving
- A3 — lean.org A3 report lexicon
- Kepner-Tregoe — toolshero KT method (cites Kepner & Tregoe, *The Rational Manager*, 1965)
- Complex-systems critique — Richard Cook, *How Complex Systems Fail* (how.complexsystems.fail) — the foundational text of the Allspaw / Adaptive Capacity Labs / "Learning From Incidents" school.

---

## 1. The frameworks, distilled

### 5 Whys (Toyoda / Ohno, Toyota)
Ask "why?" ~5 times, each aimed at the prior answer, until you reach a *process that
is missing or broken* (not a person). Ohno called it "the basis of Toyota's scientific
approach." **Key nuance most people miss: it was not built for RCA** — it explained why
new features/techniques were needed. The good version ends at a process gap ("no shelf-
inspection routine"), not a part ("rusted shelf foot").

**Documented failure modes** (Minoura, former Toyota MD; Card, *BMJ Q&S* 2017):
- **Single-path bias** — "tendency to isolate a single root cause" when each *why* has
  many valid answers. It walks one branch of a tree and calls it the trunk.
- **Stops too early / at the knowledge ceiling** — "the investigator cannot find causes
  they do not already know"; halts at the first plausible symptom.
- **No answer validation** — nothing checks that each *why→because* link is real cause
  vs. story. No control, no but-for test.
- **Irreproducible** — "different people using five whys come up with different causes
  for the same problem." (A method whose output depends on who runs it is not a method.)
- **Arbitrary depth** — the *fifth* why is a ritual, not a stopping rule correlated with
  cause (Card: should be "abandoned"; recommends fishbone instead).

### Ishikawa / fishbone (Kaoru Ishikawa, 1960s)
Problem = fish head; major **cause categories** = ribs; candidate causes = sub-bones.
A *brainstorming-coverage* scaffold, not proof. Standard category sets:
- **6 Ms (manufacturing):** Machine, Method, Material, Man/Manpower, Measurement,
  Milieu/Mother-nature (environment). (Extended 8 Ms add Management, Maintenance, Mission.)
- **8 Ps (service/product):** Product, Price, Place, Promotion, People, Process,
  Physical-evidence, Performance.
- **4–5 Ss (service):** Surroundings, Suppliers, Systems, Skills, (Safety).

Value: categories are **prompts that force breadth** so you don't fixate on one
explanation. Limit: it shows *potential* causes only — "confusion can arise among
problems, causes, symptoms, and effects"; quality depends entirely on who brainstorms,
and **nothing here verifies anything**.

### 8D — Eight Disciplines (Ford)
Team-based PDCA-shaped recurrence-elimination. D0 plan/emergency-response → D1 team →
**D2 describe the problem (5W2H; an "Is/Is-Not" worksheet is standard here)** → **D3
interim containment (shield the customer NOW, separate from the real fix)** → **D4
verify root cause AND escape point** → D5 verify permanent correction → D6 implement
→ **D7 prevent recurrence systemically (fix the management system, not the instance)**
→ D8 recognize team. Two ideas worth stealing:
- **Escape point** = "the earliest control point that *should* have caught the problem
  but didn't." Distinct from root cause. You fix *both* the failure and the detection gap.
- **Containment ≠ correction.** A temporary shield is a first-class, separately-tracked
  deliverable — you don't withhold mitigation until the investigation closes.

### Kepner-Tregoe (Kepner & Tregoe, *The Rational Manager*, 1965) — the prize
Four rational processes, each answering one question:
1. **Situation Appraisal** — "What's going on?" triage: list concerns, set priority/urgency.
2. **Problem Analysis** — "Why did it happen?" the IS/IS-NOT engine (below).
3. **Decision Analysis** — "Which course do we take?" weighted criteria + risk.
4. **Potential Problem Analysis** — "What could go wrong next?" pre-mortem on the fix.

**Problem Analysis = structured differencing.** A deviation is specified on **four
dimensions**, each asked twice — what it **IS**, and what it plausibly **COULD-BE-BUT-
IS-NOT** (a tight comparison case, not the whole universe):

| Dimension | IS (the deviation) | IS-NOT (could be, but isn't) |
|---|---|---|
| **WHAT** — object & defect | which object, which defect? | which similar object / other defect could show it but doesn't? |
| **WHERE** — location | where geographically / on the object? | where else could it appear but doesn't? |
| **WHEN** — timing | first seen when? in the lifecycle/since? what pattern? | when could it have appeared but didn't? |
| **EXTENT** — magnitude | how many, how big, what trend? | how large/widespread could it be but isn't? |

Then the move that makes KT powerful:
- **DISTINCTIONS** — what is *different, unique, or special* about the IS versus the
  IS-NOT? (Only the night shift. Only lot #7. Only after the v2.3 deploy.)
- **CHANGES** — what *changed* in/around each distinction, and when relative to the
  deviation's WHEN? Causes hide in changes.
- **Candidate causes** are generated *from the changes*, then each is **tested against
  every line of the spec**: a true cause must explain *both* the IS *and* the IS-NOT
  without a "yes, but…". A cause that can't explain why the comparable case is unaffected
  is wrong or incomplete.

This is the tool the plugin is missing: **the IS-NOT column is a built-in negative
control.** It forces you to name the dog that didn't bark and demand your hypothesis
account for it.

### A3 (Toyota)
The whole investigation on one 11×17 sheet, left→right as PDCA: background → current
condition (with data) → goal → root-cause analysis → countermeasures considered/chosen →
plan (who/what/when) → follow-up (evidence it worked). Value is **the discipline, not the
paper**: the single page forces distilled evidence-based reasoning (no padding), it's a
*consensus/storytelling* artifact built from facts gathered at the gemba, and it carries a
named **owner**. "The thinking transfers whether or not it ever lands on a sheet."

---

## 2. The critique: "root cause is a myth" (Cook / Allspaw / Adaptive Capacity school)

Richard Cook, *How Complex Systems Fail*, is the canonical text behind John Allspaw's
Adaptive Capacity Labs and the "Learning From Incidents" movement. The load-bearing points:

- **#3 — "Catastrophe requires multiple failures — single point failures are not enough."**
  Each contributing fault is *necessary but not sufficient*; only the *combination*
  permits failure.
- **#4 — "Complex systems contain changing mixtures of failures latent within them."**
  The system always runs degraded; the latent-failure mix shifts constantly.
- **#7 — "Post-accident attribution to a 'root cause' is fundamentally wrong … there is
  no isolated 'cause' of an accident."** Root-cause findings reflect "the social,
  cultural need to blame specific, localized forces or events" — a *social* artifact, not
  a technical one.
- **#8 — "Hindsight bias remains the primary obstacle to accident investigation."**
  Knowing the outcome makes precursors look more obvious than they were; *ex post* human-
  performance analysis is therefore inaccurate.
- **#15 — Cause-blocking remedies are weak:** the exact pattern won't recur anyway because
  the latent-failure mix has already moved; "fixing the cause" adds complexity, not safety.

**What this does NOT mean:** it is not relativism, and it is not license to refuse a
verdict. It means: (a) prefer **contributing conditions / a causal set** over a singular
trunk; (b) treat any "the operator erred" stopping point as **hindsight bias until
proven**; (c) measure the system's **second story** — why the action was reasonable given
what the actor saw — not just the first.

---

## 3. Reconciling the two: decisive verdicts WITHOUT single-cause bias

The plugin already resists single-cause bias (SKILL.md explicitly flags "crowning one of
two jointly-necessary factors 'the root cause'" as a failure mode) and already demands
controls + but-for. The reconciliation it should state plainly:

> A **verdict** answers a *falsifiable claim* ("factor X is in the sufficient set / X was
> necessary"), which is decidable with controls. A **root cause** is a *narrative choice
> of where to stop* in a web of necessary conditions — and that choice is a construct.
> The plugin commits hard to the first and stays honest about the second.

Concretely: you can be 0.95 that "the v2.3 deploy was *necessary* for the outage (removed
it in a control window → no recurrence)" while refusing to call the deploy *the* root
cause, because the missing canary, the silent retry, and the alert gap were each equally
necessary. **Necessity/sufficiency is measurable; "the root" is editorial.** Report the
causal *set* and where each member sits on the evidence ladder. This is fully compatible
with CONFIRMED/FALSIFIED/INCONCLUSIVE — the verdict attaches to *each claim*, not to a
singular root.

---

## 4. CONCRETE plugin adoptions

### A. **IS/IS-NOT specification table** (highest-value — adopt into Step 1/3)
Add to the SKILL loop, in §1 (convert assertions → hypotheses) and §3 (controlled
experiments), as the **hypothesis-generation + built-in-negative-control** scaffold.
Drop a ready-to-fill template into `references/artifacts.md`:

```
## Problem specification (Kepner-Tregoe IS / IS-NOT)
Deviation in one line: ________ deviates from expected by ________.

| Dimension | IS | COULD-BE-BUT-IS-NOT | Distinction (what's unique re the IS) | Change (what changed there, & when vs onset) |
|---|---|---|---|---|
| WHAT  (object & defect) |  |  |  |  |
| WHERE (location)        |  |  |  |  |
| WHEN  (onset & pattern) |  |  |  |  |
| EXTENT(how many/big/trend)| |  |  |  |

Candidate causes (from CHANGES): C1 … C2 … C3 …
Cause test — each must explain BOTH the IS and the IS-NOT with no "yes, but":
| Cause | Explains every IS? | Explains every IS-NOT? | Assumptions needed | Verdict |
```
Why it fits: the **IS-NOT column is a pre-registered negative control** ("hosts where the
playbook ran and nothing broke") that the plugin already demands for causal claims — KT
just makes naming it *mandatory and structured*. The cause-test row is the **but-for test
applied to comparison cases**: a surviving cause must account for the unaffected twin.

### B. **Fishbone as hypothesis-generation scaffold** (adopt into Step 1)
Use the 6M / 8P category prompts as a **breadth checklist when enumerating hypotheses**, to
counter the 5-Whys single-path failure the plugin warns about. Recommend a software-tuned
category set so engineers don't have to translate "Machine/Material": e.g.
**Code · Config · Data/Input · Infra/Host · Dependencies/Upstream · Deploy/Release ·
Load/Traffic · Observability-gap.** One numbered hypothesis seeded per non-empty category
→ then ranked by prior and sent to cheapest-falsifier-first. Frame it exactly as the
sources do: fishbone *generates* candidates, it *verifies nothing* — every bone still needs
a probe and a verdict. (Pairs naturally with the multi-agent fan-out: one agent per bone.)

### C. **Escape point + containment** (adopt into Step 4/6, lightweight)
From 8D: when a verdict lands, ask two extra questions and record them in the ledger —
(1) **Escape point:** what control *should* have caught this and didn't? (the alert that
didn't fire, the test that didn't exist) — this becomes its own hypothesis/finding, not a
footnote; (2) **Containment vs. correction:** track any interim mitigation as a separate,
first-class item so the investigation never blocks shielding the user. Both honor Cook #7
by widening the fix from "the cause" to "the cause *and* the detection gap."

### D. **Hindsight-bias guard on human-error stopping points** (adopt into Step 4)
Add to the INCONCLUSIVE/closure discipline: **"operator/author erred" is a hindsight-bias
hypothesis until you've written the second story** — why the action was locally reasonable
given the information actually available at the time. This directly imports Cook #8 and
extends the existing "stops at human error" concern. A *why* chain that bottoms out at a
person, not a process/system gap, has stopped early (5-Whys failure mode + Cook).

### E. **"Root cause is a construct" framing** (adopt into Failure-modes section)
Add one bullet to "Failure modes this method exists to prevent": *Mistaking the narrative
stopping-point for a discovered fact.* State the §3 reconciliation — verdicts attach to
necessity/sufficiency claims (measurable, controllable, decidable), while "the root cause"
is an editorial choice of where to stop in a set of jointly-necessary conditions. Report
the **causal set** with each member's ladder position; reserve "root cause" language for
when one factor is genuinely *sufficient alone* and demonstrated so under control.

### Priority
1. **IS/IS-NOT table** (A) — net-new structured tool, directly fills the stated gap;
   doubles as enforced negative control. Ship first.
2. **Fishbone breadth checklist** (B) — cheap, counters single-path bias, slots into fan-out.
3. **Construct-framing + hindsight guard** (D, E) — text-only, sharpens existing verdicts.
4. **Escape point / containment** (C) — adds incident-grade completeness.
