# NASA Systems Engineering & Risk Governance → scientific-method plugin

Research for the scientific-method Claude Code plugin. Question: what does NASA's
SE/risk machinery (TRLs, stage gates, PRA/CRM, post-Columbia Technical Authority +
dissent) teach us, and what should we concretely adopt?

Primary sources (all fetched, not recalled):
- NASA SE Handbook NASA/SP-2016-6105 Rev2 (PDF, text-extracted locally) — reviews,
  Technical Authority, dissent, CRM definition, "test as you fly", margins.
- NASA SCaN TRL page — per-level TRL definitions.
- Feynman, Rogers Commission Appendix F (via feynman.com summary).
- CAIB (Columbia Accident Investigation Board) — organizational causes,
  independent Technical Authority recommendation.
- NPR 8000.4 / NASA/SP-2011-3422 (Risk Management Handbook) and NASA/SP-2010-576
  (RIDM Handbook) — referenced by the SE Handbook as the RIDM+CRM source.
- Wikipedia "Design review (U.S. government)" — per-review entry/exit criteria
  (derived from NPR 7123.1), used to corroborate the handbook.

---

## Part 1 — Distilled principles

### 1.1 Technology Readiness Levels (TRL 1–9)

A 9-rung maturity ladder. The key property worth stealing: **maturity is defined by
the fidelity of the evidence environment, not by how finished the thing looks.** A
TRL is not "how good is it" — it's "where has it been demonstrated".

| TRL | NASA definition (paraphrased from SCaN) |
|-----|------------------------------------------|
| 1 | Basic principles observed; scientific research beginning to translate into R&D. |
| 2 | Technology concept formulated; practical applications of principles; speculative, no experimental proof. |
| 3 | Active R&D begins; analytical + laboratory studies; proof-of-concept model often built. |
| 4 | Component validation in lab; multiple component pieces tested together. |
| 5 | Breadboard tested under more rigorous, near-realistic simulated environment. |
| 6 | Fully functional prototype / representative model demonstrated in relevant environment. |
| 7 | Prototype demonstrated in the operational ("space") environment. |
| 8 | Technology built and "flight qualified" through test and demonstration; ready to integrate. |
| 9 | "Flight proven" — succeeded in an actual mission. |

The two phase boundaries that matter most for us: **TRL 3** (first proof-of-concept —
the thing has been shown to work at all) and **TRL 6** (works in a *relevant*
environment, not just a lab toy). The recurring failure NASA fights is **claiming a
high TRL on low-TRL evidence** — exactly our "asserting derived numbers as physical
facts" failure mode.

### 1.2 Stage-gate reviews (SRR → PDR → CDR → TRR → FRR)

Each review is a control gate with **entrance criteria** (you may not even hold the
review until these exist) and **success/exit criteria** (you may not pass until these
are met). The gates ratchet maturity; you cannot skip rungs.

- **SRR — System Requirements Review.** Are the requirements and the chosen concept
  right and sufficient to meet the mission? Exit: requirements validated and the
  selected concept shown to satisfy mission need.
- **PDR — Preliminary Design Review.** *Entry:* a preliminary design exists, options
  selected, interfaces identified, verification methods described. *Exit:* all
  requirements allocated/validated with adequate flowdown; design expected to meet
  functional+performance reqs; design is verifiable; risks identified, characterized,
  and mitigated. Establishes the basis to proceed to detailed design.
- **CDR — Critical Design Review.** *Entry:* completed "build-to" detailed design.
  *Exit:* design maturity supports proceeding to fabrication/integration/test; design
  audited by production/verification/ops/specialty groups; final design fulfills the
  PDR specs; on track for cost/schedule.
- **TRR — Test Readiness Review.** *Entry/exit:* the test article, facility, personnel,
  and procedures are all ready, and data acquisition/reduction/control are ready,
  *before* the test runs.
- **FRR — Flight Readiness Review.** *Exit:* certification that flight can proceed
  safely at acceptable risk; all interfaces compatible; system configured and "go".

Principle: **readiness to *do* the expensive irreversible step is itself a reviewed
artifact with pre-stated criteria.** You don't earn the right to run the test (TRR) or
ship (FRR) by fiat — you earn it by meeting a checklist written in advance.

### 1.3 Risk: RIDM + CRM, the 5×5 matrix, and PRA

Since NPR 8000.4 (2008), NASA RM = **two complementary processes**:

- **RIDM (Risk-Informed Decision Making):** informs *direction-setting* decisions
  (design choices, baseline performance requirements) by using risk + uncertainty
  information to select among alternatives. This is a **front-loaded, decision-time**
  process — it runs *before* you commit to a path.
- **CRM (Continuous Risk Management):** manages risks *over the lifecycle* once a path
  is chosen, to assure safety/technical/cost/schedule requirements are met. Handbook
  definition: "a systematic and iterative process that efficiently **identifies,
  analyzes, plans, tracks, controls, communicates, and documents** risks." Those seven
  verbs are the CRM loop.

Together: RIDM picks the baseline; CRM defends it. RM is defined as *both*, not CRM
alone (an explicit 2008 correction — pure CRM was reactive).

- **5×5 risk matrix:** each risk scored on **Likelihood (1–5) × Consequence (1–5)**,
  plotted on a grid; red/yellow/green cells set the response priority. Risks carry a
  **trigger threshold** (a defined risk level) that fires a mitigation/contingency
  action plan, plus named stakeholders to inform.
- **PRA (Probabilistic Risk Assessment):** scenario-based quantification — enumerate
  failure scenarios, their likelihoods (with uncertainty distributions), and
  consequences. The handbook stresses "uncertainties are included in the evaluation of
  likelihoods and consequences" — risk numbers are distributions, not points.

### 1.4 Test as you fly

"**Test as you fly, and fly as you test.**" Verify the system in the configuration and
environment it will actually operate in; do not certify on a convenient proxy and
assume it transfers. Maps directly to our **"measure against ground truth, not
metadata"** and **but-for/control-case** discipline.

### 1.5 Margin management

Designs carry explicit **margins** (factors of safety) and **contingency / Unallocated
Future Expenses (UFE)** held in reserve and drawn down as maturity rises. The discipline:
margin is *tracked and reported* (it shrinks as you approach reality), and a component
"may not be usable" if it violates required margins. Principle: **state your margin
against the limit explicitly, and watch it burn down** — never quietly consume it.

### 1.6 Technical Authority + formal dissent (the post-Columbia core)

CAIB's organizational finding: foam shedding was a known anomaly accepted because past
damage was minor — "over time, management gained confidence that it was an acceptable
risk" (**normalization of deviance**; Diane Vaughan was on CAIB staff). Program
management had been allowed to **waive its own technical requirements**, and the burden
of proof was inverted — engineers had to prove it *unsafe* rather than management
proving it *safe*.

CAIB Recommendation: an **independent Technical Authority** "responsible for technical
requirements and all waivers to them," structurally **separate from program/project
management** (which owns cost/schedule). The TA chain owns the technical/safety
baseline; the program owns delivery; they are deliberately different people so
schedule pressure cannot silently waive a technical limit.

**Formal dissent process** (SE Handbook, decision-record template): when a participant
disagrees with a recommendation, the dissent is **documented in the decision record** —
the position, and **how the dissent was addressed** (decision matrix, risk analysis).
Appendices preserve "previous related dissent." The obligations:
1. An individual has the **right and duty to raise** a dissenting technical opinion.
2. It must be **recorded in writing**, not resolved verbally and forgotten.
3. It is **escalated up the Technical Authority chain** (independent of the program
   chain) until resolved by someone with authority.
4. The **resolution + rationale** is written down and preserved — dissent is part of
   the permanent record even when overruled.

### 1.7 Feynman, Appendix F — the load-bearing lesson

Feynman found management estimated shuttle failure at ~**1 in 100,000** while working
engineers estimated ~**1 in 100** — a 1000× gap. The gap came from management
substituting wishful/PR numbers for the engineers' evidence-grounded ones. He got the
real number by going "**straight to the people who put the shuttle together**." Closing
line: **"For a successful technology, reality must take precedence over public
relations, for nature cannot be fooled."**

This is the single sharpest statement of our entire thesis: **the estimate must come
from the evidence and the people touching the hardware, not from the convenient number
the chain wants to hear.** Two operational lessons:
- **Bottom-up risk numbers beat top-down ones.** Aggregate the people-near-the-silicon
  estimates; distrust a clean round number handed down.
- A **1000× confidence gap between layers** is itself a red flag — when our council
  seats or a refuter disagree with the orchestrator's lean by orders of magnitude,
  that *gap* is the finding.

---

## Part 2 — CONCRETE plugin adoptions

### 2.1 Should `confirmed/prototype/research/kill` become a finer TRL-like scale?

**Recommendation: No — do not replace the 4-enum with a 9-rung scale. Instead, add an
orthogonal "evidence-environment" axis to each verdict.**

Reasoning (KISS + Four-Ds "Different"): our enum already carries an action semantics
(kill → falsification log; confirmed → CONFIRMED). A 9-level scale invites false
precision and bikeshedding over rung boundaries — the exact thing TRLs are criticized
for in practice. The *valuable* TRL insight is not the count of levels, it's that
**maturity = fidelity of the demonstration environment.** Capture that as a tag, not a
re-scale.

Concretely, add an **Evidence Environment** tag to every verdict, mirroring TRL's three
phase-boundaries (toy lab / relevant env / operational env):

```
evidence_env: lab | relevant | operational
  lab         — measured in a synthetic/isolated harness, proxy inputs (≈TRL 3–4)
  relevant    — measured under near-production conditions, real-ish inputs (≈TRL 5–6)
  operational — reproduced in the real deployment / on the real workload (≈TRL 7–9)
```

Rule (the load-bearing part): **a `confirmed` verdict may not claim it holds in
production unless `evidence_env: operational`.** A `confirmed` at `evidence_env: lab` is
"confirmed in the lab" — honest, and explicitly *not* a claim about the real system.
This directly encodes "test as you fly" and blocks the TRL-inflation failure mode
(claiming a high readiness on low-fidelity evidence) using one tag instead of a new
taxonomy. It plugs into the existing confidence-calibration text: `evidence_env: lab`
caps how high confidence can honestly go for a production claim.

### 2.2 Entry/exit criteria gating investigation → fix → publish

**Recommendation: define three named gates (mirroring TRR/CDR/FRR) with written
entry+exit criteria, in the SKILL "Loop until clean" section.** This formalizes
transitions that are currently implicit. The discipline NASA adds: *you may not hold
the gate until entry criteria exist, and may not pass until exit criteria are met.*

**Gate 1 — RCR (Root-Cause Review): investigation → fix.** Analogue of CDR (you've
understood the system enough to start building).
- *Entry:* every hypothesis in the ledger has a verdict (CONFIRMED/FALSIFIED/
  INCONCLUSIVE); every INCONCLUSIVE names its missing probe.
- *Exit:* root cause CONFIRMED with an evidence reference and a control/but-for case;
  confidence derived (not picked); convenient/reversed hypotheses explicitly ruled out
  with evidence. **You may not write a fix until the cause passes RCR** — no fixing a
  story.

**Gate 2 — FVR (Fix Verification Review): fix → ready-to-publish.** Analogue of TRR
(the test rig is ready) + the fix itself.
- *Entry:* fix implemented; a Reproduce block exists that regenerates the key numbers;
  baseline recorded.
- *Exit:* fix shown to move the primary metric as a **signed delta vs baseline**; **all
  named guardrail metrics checked and non-regressed**; the fix re-verified under the
  *same* `evidence_env` as the claim (test-as-you-fly); refuter wave run.

**Gate 3 — PRR (Publish Readiness Review): publish/merge/external-send.** Analogue of
FRR (the irreversible go/no-go).
- *Entry:* RCR + FVR passed; ledger persisted with provenance header (commit, machine,
  toolchain, input hashes, date); scope corrections dated.
- *Exit:* final adversarial review pass against the ledger with **no new findings**
  (dry pass); peer-review/council escalation done for high-stakes; **margin stated**
  (how far the headline number sits from the asserted limit, and the residual unknown).
  Staged rollout (dry-run/canary) where the domain allows. This is the explicit
  "before any irreversible step" gate the SKILL already gestures at — now with criteria.

Each gate is **lightweight by default** (the method-weight-scales-with-evidence-cost
rule still governs — a one-probe question gets a one-line gate check, not a ceremony).
The gates are a *checklist contract*, not a mandatory heavyweight review for trivia.

### 2.3 Encoding dissent-preservation beyond the council

The council already (a) poses a question blind to N seats and (b) routes factual cruxes
to probes and preserves minority positions. NASA adds three things our council lacks:

**(a) An independent Technical Authority chain — separate "is it correct" from "ship
it".** Today the orchestrator both runs the investigation *and* decides to publish —
this is exactly the CAIB anti-pattern (the party that owns schedule waives the
technical limit). **Adoption:** the **refuter / peer-review / meta-reviewer line is the
Technical Authority chain, and its sign-off is required and recorded separately from the
orchestrator's "done."** The orchestrator owns delivery (cost/schedule); the TA line
owns the technical baseline; publish requires *both*. Concretely: PRR (Gate 3) exit
requires a TA sign-off artifact that the orchestrator cannot self-issue.

**(b) Invert the burden of proof at the publish gate.** CAIB's core finding: the
default flipped from "prove it's safe" to "prove it's unsafe." **Adoption:** make the
PRR exit criterion *prove the claim safe to publish* — i.e., the burden is on the
finding to survive refutation, **not** on a skeptic to manufacture a reason to block.
An unrefuted-but-also-unverified claim does **not** pass. (This is already our stance —
make it the explicit gate rule and name it.)

**(c) A permanent dissent record that outlives the decision.** The council "preserves
minority positions" in-conversation, but conversation gets compacted (the same reason
we persist the ledger). **Adoption:** add a **Dissent Log** section to the persistent
ledger artifact, modeled on the SE Handbook decision record:

```
## Dissent Log
| # | Date | Dissenting position | Raised by (seat/agent) | How addressed | Resolution + rationale | Overruled? |
```

Rules: (1) any council seat, refuter, or peer reviewer whose objection was *not*
adopted gets a Dissent Log row — overruled dissent is recorded, not discarded;
(2) each row names **how the dissent was addressed** (probe run / revision applied /
documented concession) — words alone don't close it; (3) the log is part of the
provenance-pinned artifact, so a future session sees what was argued and overruled
(complementing DO-NOT-RE-ATTACK, which records what was *killed* — Dissent Log records
what was *contested but shipped anyway*). This is the durable analogue of NASA carrying
a recorded, escalated, written-resolution dissent even when the launch proceeds.

**(d) Watch the inter-layer confidence gap (Feynman).** When a council seat or refuter
disagrees with the orchestrator's confidence by a large factor, treat the *gap itself*
as a finding requiring a probe — don't average it away. A 1000× gap between "the people
touching the hardware" and the chain's number is the Appendix-F signal.

---

## One-paragraph summary for the SKILL maintainer

Keep the 4-verdict enum; add an orthogonal `evidence_env: lab|relevant|operational` tag
so "confirmed" can't masquerade as a production claim on lab-only evidence (test-as-you-
fly). Add three checklist gates with written entry+exit criteria — RCR (cause →
fix), FVR (fix → ready), PRR (ready → publish) — mirroring CDR/TRR/FRR, lightweight by
default. Make the refuter/peer-review/meta-reviewer line a Technical Authority chain
whose sign-off is required and recorded separately from the orchestrator's "done," put
the burden of proof on the claim to survive (not on a skeptic to block), and add a
persistent **Dissent Log** to the ledger so overruled objections survive compaction the
way NASA preserves recorded dissent. Underneath all of it: Feynman — the estimate comes
from the evidence and the people touching the hardware, because nature cannot be fooled.
