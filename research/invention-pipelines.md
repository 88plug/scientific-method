# Institutional Invention Pipelines, End-to-End

Research for the `scientific-method` plugin. Goal: mine how the great institutional
invention shops actually ran — Edison's Menlo Park, Bell Labs, PARC, Dyson, IDEO/d.school,
and the corporate disclosure→patent process — and extract (a) the recurring pipeline
stages, (b) the **notebook/disclosure discipline that makes an invention DEFENSIBLE**, and
(c) what **"reduction to practice"** demands. Then map all three onto the plugin's
campaign loop as a default **invention mode** (alongside its existing diagnosis/falsify
mode).

Sources fetched (Wikipedia primary articles + Edison Papers):
- Edison / Menlo Park — en.wikipedia.org/wiki/Thomas_Edison (quotas attributed via Edison
  Papers / standard biographies — the "minor invention every 10 days, big thing every
  6 months" goal is Edison's own oft-quoted Menlo Park target, 1876).
- Bell Labs — en.wikipedia.org/wiki/Bell_Labs
- Dyson — en.wikipedia.org/wiki/James_Dyson
- Design thinking (IDEO / Stanford d.school) — en.wikipedia.org/wiki/Design_thinking
- Invention disclosure — en.wikipedia.org/wiki/Invention_disclosure
- Reduction to practice — en.wikipedia.org/wiki/Reduction_to_practice
- Lab notebook — en.wikipedia.org/wiki/Lab_notebook

PARC is covered from general record (Smalltalk/GUI/Ethernet/laser-printer "build it to
believe it" demo culture); the Wikipedia Design-thinking and Bell-Labs articles supply the
transferable structure, so PARC is treated as a confirming instance, not a separate source.

---

## 1. The five shops, distilled

### Edison's Menlo Park (1876) — the *invention factory* with a quota
The first **industrial research lab** "concerned with creating knowledge and then
controlling its application" (Wikipedia). Three transferable inventions of method:

- **Output quota as a forcing function.** Edison's stated Menlo Park goal: *a minor
  invention every ten days and a big thing every six months.* Whether or not he hit it,
  the quota is the mechanism — it forces a **cadence** and converts "invent something
  great" into a schedulable rate. (Result over his career: **1,093 US patents**.)
- **Systematic variation at brute-force scale.** Not flashes of genius — exhaustive
  sweeps over a candidate space: carbon microphone "after testing **150 materials**";
  the lamp filament tried carbonized cardboard, hemp, palmetto, then bamboo
  (carbonized bamboo lasted "**over 1,200 hours**"); the storage battery "tested
  **10,000 combinations** of electrodes and solutions." Backed by deliberately
  stocking "**eight thousand kinds of chemicals**" + every screw/wire/hair so any
  variant was testable *now*. "**1% inspiration and 99% perspiration.**"
- **Division of labor + witnessed notebooks.** Upton, Batchelor, Ott, Dickson ran
  parallel lines; notebooks "**jointly signed 'E&B'**" recorded near-constant
  experimentation, and Ott's notebook testimony later **defended Edison's patents in
  litigation** — i.e. the lab record was built to be a *legal* artifact, not just a
  memory aid.

### Bell Labs (1925) — the research→development→manufacturing pipeline
Structurally placed *between* the maker (Western Electric) and the operator (AT&T), so
the **pipeline was the org chart**. Two halves coexisted: **mission-pull** ("supporting
the Bell System with engineering advances" → N-carrier, crossbar switch, direct distance
dialing) and **curiosity-push** (Jansky's radio astronomy and Penzias–Wilson's CMB came
from *investigating line static*). Documented research→product chains: transistor (1947)
→ surface passivation (1955) → planar process (1957) → working MOS device (1959–60);
modems-near-Shannon-limit → **invented DSL**. The lesson: a serendipitous finding still had
a **named development+manufacturing path** waiting to carry it to a shipped product
(Indian Hill colocated switching developers with Hawthorne Works engineers). Freedom was
real but **never terminal** — discovery had a downstream.

### PARC (1970s) — "build it to believe it"
Demo-driven invention: the GUI, Smalltalk, Ethernet, and the laser printer were made
*real and shown working* rather than argued on paper. The transferable rule: an idea is
not credited until it has been **reduced to a running prototype someone can sit in front
of**. (Famous failure-of-pipeline lesson too: invention without the disclosure/commercial
capture stage leaks the value to others — Xerox invented, others shipped.)

### Dyson (1979–1983) — iteration as the unit of work
**~5,127 prototypes over five years** before the G-Force launched. Dyson's own framing:
"5,126 failures. But I learned from each one… I don't mind failure." The discipline:
**one prototype = one learning event**, sequential, each change measured against the last;
the count *is* the engineering log. (One-change-at-a-time isolation is the widely-reported
practice though not in the WP article — it's the DOE/OFAT logic the plugin already knows.)

### IDEO / Stanford d.school — the structured ideate→prototype→test loop
A deliberately **non-linear, iterative** loop that "loops back through inspiration,
ideation, and implementation more than once." Stanford's five phases: **(re)defining the
problem → needfinding/benchmarking → ideating → building → testing.** Ideation
**alternates divergent then convergent** thinking (structured brainstorm to widen, then
"pattern finding and synthesis" to narrow). Prototyping is **low-fidelity and fast**:
"even a rough mock-up helps to gather feedback" — prototypes exist to *expose strengths
and weaknesses quickly*, not to be right.

---

## 2. The recurring pipeline (the cross-shop invariant)

Strip the brand names and the same six stages appear everywhere:

| Stage | Edison | Bell | Dyson | IDEO/d.school |
|---|---|---|---|---|
| **1. Problem framing / needfinding** | "what to invent" target | mission-pull need | the dust problem | (re)define problem, empathize |
| **2. Systematic ideation w/ a quota or breadth target** | 150/10,000-material sweeps; 10-day cadence | research portfolio | candidate mechanisms | divergent brainstorm (quantity, defer judgment) |
| **3. Rapid prototype** | bench variant from the 8,000-chemical stock | breadboard/lab demo | a physical prototype | low-fi mock-up |
| **4. Measured kill / iterate** | keep the filament that lasts 1,200 hrs | demonstrate vs. spec | 5,126 measured failures | test → iterate → converge |
| **5. Documentation / disclosure** | witnessed E&B notebook | patent + manufacturing handoff | engineering log | synthesis to actionable insight |
| **6. External validation** | patent grant / litigation survival | ships through Western Electric | market (Japan, then own co.) | user test, then implementation |

Two structural lessons the plugin should internalize:
- **A quota/breadth target at stage 2 is a forcing function**, not vanity — it defeats
  fixation on the first idea (exactly the single-path bias the plugin already fights in
  diagnosis mode). Ideation needs an **explicit N** ("enumerate ≥k mechanisms") the way
  the hypothesis ledger needs every candidate including the inconvenient ones.
- **Stage 6 (external validation) is mandatory, not optional.** PARC's lesson: invention
  without the disclosure+validation stages leaks the value. Maps directly onto the
  plugin's existing **refuter / peer-review / council** gates.

---

## 3. Defensibility: the notebook & disclosure discipline

This is the part most "ideation" frameworks omit and the part the plugin is *already
shaped to enforce*. To make an invention **defensible** (legally, scientifically, or just
auditably), the record must satisfy:

**The witnessed lab-notebook standard** (Wikipedia *Lab notebook*; Edison practice):
- **Permanently bound, sequentially numbered pages** — "data cannot be easily altered";
  no removed/inserted pages.
- **Permanent ink, contemporaneous** — written "as the experiments progress, rather than
  at a later date"; original record, "no copying."
- **Every page dated and signed** by the person who did the work.
- **Witnessed** — "inspected periodically by another scientist who can read and understand
  it." The witness is a **non-inventor who attests they understood it** — this is what
  turned Ott's notebook into court-admissible evidence defending Edison's patents.

**The invention disclosure** (Wikipedia *Invention disclosure*): a confidential, often
**standardized-form** document an engineer writes "to determine whether patent protection
should be sought" — capturing the invention, the inventors, and the dates of **conception
and reduction to practice**, routed to a **patent committee** that decides file / hold /
drop. (Modern corporate version: disclosures are scored/ranked and triaged by a review
board — the committee is the institutional **kill-or-advance gate**.)

The mapping is exact: **bound+numbered+dated = the plugin's append-only ledger;
witnessed-by-someone-who-understood = the refuter/peer-reviewer gate; the disclosure form
+ committee = the verdict + meta-reviewer decision.** The plugin already has the machinery;
invention mode just *names the artifacts as evidence* and adds the witness/date discipline.

---

## 4. "Reduction to practice" — the bar an invention must clear

From Wikipedia *Reduction to practice* (US patent law). The sequence is **conception →
reduction to practice**:

- **Conception** = "the formation in the mind of the inventor, of a definite and permanent
  idea of the complete and operative invention" (*Hybritech*, Fed. Cir. 1986). An idea, not
  yet proof.
- **Actual reduction to practice** = the claimed invention is physically built and **"works
  for its intended purpose"** (*Brunswick v. U.S.*). **A demo that functions** — this is
  PARC's "build it to believe it" and Dyson's working prototype, stated as a legal bar.
- **Constructive reduction to practice** = filing a sufficiently-detailed patent application
  (you've *described* it completely enough that a skilled person could build it), even
  absent a physical build.
- In **unpredictable arts** (chemistry/biology) conception and reduction to practice can
  **coincide** — you can't claim a definite idea until a successful experiment proves it
  (*Regents v. Synbiotics*). I.e. **the experiment IS the conception.**

The load-bearing requirement for the plugin: **an invention is not "done" at conception —
it is done when a built artifact is shown to work for its stated purpose, OR when it is
described completely enough to be reproduced.** That is the same standard as the plugin's
**0.90+-confidence-only-with-direct-ground-truth** rule, applied to *building* rather than
*diagnosing*: "it should work" is conception; **a passing demo or a reproducible spec** is
reduction to practice.

---

## 5. Mapping onto the campaign loop — a default "invention mode"

The plugin's `/investigate` loop is built for **diagnosis** (falsify hypotheses about an
existing system). Invention is the **dual**: instead of *ruling explanations out*, you
*build candidates up* — but the same machinery applies with the verdict polarity flipped.
Proposed invention mode = the campaign loop with these stage bindings:

| Campaign-loop step (diagnosis) | Invention-mode binding |
|---|---|
| Cheapest probe first | **Cheapest prototype first** — smallest mock-up that could *kill or de-risk* the leading design before any build-out (IDEO low-fi; Edison bench variant). |
| Hypothesis ledger (all candidates, incl. inconvenient) | **Idea ledger with a quota** — enumerate ≥k design candidates (the Edison/d.school divergence target). Include the boring/obvious one; it gets the same prototype test as the clever one. |
| Predict, then probe (outcome→conclusion table) | **Spec the success criterion before building** — what observable means "works for intended purpose" (the reduction-to-practice bar) vs. kill. |
| Verdicts: CONFIRMED / FALSIFIED / INCONCLUSIVE + confidence | **REDUCED-TO-PRACTICE / KILLED / NOT-YET-WORKING** + confidence. 0.90+ only on a *passing demo or reproducible spec*, never on "should work." |
| Append-only ledger (`EXPERIMENTS.md`) | **Witnessed, dated invention record** — every prototype = a dated entry; the ledger is the bound notebook. Add a `disclosure` block (inventors, conception date, reduction-to-practice date/evidence). |
| Refuter / peer-review / council gates | **The witness + patent committee** — refuter = the non-inventor who must understand it; meta-reviewer/verdict = the file/hold/drop committee. External validation is mandatory. |
| "Loop until clean" | **Iterate until reduced to practice** (Dyson's 5,127): a prototype that *teaches* without *working* is a logged FALSIFIED-design, not a failure; stop on a working+witnessed artifact. |

**Net adds the plugin doesn't already have:** (1) an **ideation quota** at the divergence
step (forcing ≥k candidates), (2) a **`disclosure` block** in the ledger capturing
inventors + conception date + reduction-to-practice evidence, and (3) a renamed verdict
triple (**reduced-to-practice / killed / not-yet-working**) so "it works" requires the same
ground-truth proof the diagnosis mode already demands for "it's confirmed." Everything else
— cheapest-probe-first, the append-only ledger, the adversarial witness gate, loop-until-
clean — is the existing campaign loop, reused unchanged.
