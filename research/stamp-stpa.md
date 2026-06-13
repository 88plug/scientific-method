# Systems-theoretic accident models — STAMP/STPA, the chain-of-events models they critique, and NTSB report discipline

Research note for the `scientific-method` plugin. Companion to SKILL.md §3 (controlled
experiments, but-for test) and rigor.md §3 (the causal ladder). This is the **formal,
named version of "circular causality"** the skill already gestures at: where the loop's
causal ladder treats cause as a *chain* (correlation → temporality → dose-response →
controlled experiment), STAMP treats cause as a *control structure* — a feedback loop
that failed to enforce a constraint. Both are in the toolkit; this note says when to
reach for the control-structure lens instead of the broken-component hunt.

Primary sources consulted: Leveson & Thomas, *STPA Handbook* (MIT PSAS,
psas.scripts.mit.edu); Wikipedia on the Swiss cheese model and Heinrich's domino model;
NTSB investigation-process pages (ntsb.gov). The STAMP causality model below is drawn
from the STPA Handbook text; the Wikipedia STAMP article title 404'd, so claims here are
sourced to the handbook and to Leveson's *Engineering a Safer World* framing, not to a
Wikipedia summary.

---

## 1. The two competing accident models

### Chain-of-events (the models STAMP critiques)

- **Heinrich's dominoes (1931).** An accident is a linear sequence: social/ancestral
  factors → fault of person → unsafe act/condition → accident → injury. Remove one
  domino (classically the unsafe act) and the chain stops. Emphasis lands on the
  *individual unsafe act* — i.e., on blame.
- **Reason's Swiss cheese (1990).** Defenses are a stack of imperfect barriers, each a
  slice with shifting holes. **Active failures** (unsafe acts at the sharp end) and
  **latent conditions** (dormant organizational weaknesses — a bad design, an
  understaffed shift, two look-alike drug vials shelved together) only produce a loss
  when holes across all slices momentarily line up: a "trajectory of accident
  opportunity." Reason's advance over Heinrich was to shift blame from character to
  *system* and to surface latent conditions that sit dormant for months.
- **Shared structure, shared limit.** Both are still *linear, sequential* causation:
  failure propagates stage-to-stage toward a loss. The standard critique (Leveson;
  Eurocontrol 2006) is that this oversimplifies tightly-coupled socio-technical
  systems. Chain models cannot represent losses that emerge with **no component
  failed at all** — every part operating to spec, the *interactions* unsafe. They bias
  the investigator toward finding the one broken domino / the one unblocked hole, which
  is single-cause bias wearing safety-engineering clothes.

### STAMP (Leveson) — accidents as inadequate control

STAMP (Systems-Theoretic Accident Model and Processes) reframes safety as a **control
problem, not a reliability problem**. Core claims:

- **Safety is an emergent property** of the system as a whole, enforced (or not) by a
  **hierarchical safety control structure**. Losses happen when the structure fails to
  enforce the **safety constraints** that keep behavior inside safe bounds — not
  (only) when a component breaks.
- Every level of the control structure is a **control loop**:
  - **Controller** — human or automated; holds a **process model** (its belief about
    the current state of the process) and a **control algorithm** (how it decides what
    to command).
  - **Control actions** — commands the controller issues.
  - **Actuators** — execute the commands on the process.
  - **Controlled process** — the thing being governed.
  - **Sensors** — measure process state.
  - **Feedback** — sensor data returned to the controller, which updates the process
    model.
- **The process-model gap is the central failure mode.** Most accidents in this view
  occur not because a part failed but because the controller's process model went
  **inconsistent with the real process state** — missing, delayed, or wrong feedback —
  so the controller issued a control action it *believed* was safe and wasn't.
  (Therac-25, TCAS, pilot-vs-autopilot mode-confusion crashes all fit this shape.)
  This is the formal account of "everyone did their job correctly and it still
  failed."

**STPA** (System-Theoretic Process Analysis) is the proactive hazard-analysis method
built on STAMP; **CAST** (Causal Analysis based on STAMP) is its retrospective,
accident-investigation twin. STPA's four steps:

1. **Define the purpose of the analysis** — name the losses to prevent, the
   system-level hazards, the system-level constraints, and the system boundary.
2. **Model the control structure** — the hierarchy of controllers, control actions,
   feedback, actuators, sensors.
3. **Identify Unsafe Control Actions (UCAs)** — apply the taxonomy below to every
   control action; each UCA yields a controller constraint.
4. **Identify loss scenarios** — the causal factors that explain *why* a UCA would
   occur (flawed process model, bad feedback, wrong algorithm) and why a safe action
   might be executed badly. These drive the requirements/mitigations.

### The Unsafe Control Action taxonomy (the hypothesis generator)

For each control action, four ways it can be unsafe:

1. **Not provided** when safety required it.
2. **Provided** when it caused a hazard (provided unsafely / when it shouldn't have
   been).
3. **Wrong timing or order** — too early, too late, out of sequence.
4. **Wrong duration** (for continuous actions) — stopped too soon, or applied too long.

The power for our purposes: this is a **finite, exhaustive checklist that generates
hypotheses mechanically** from a control loop, the same way the cheapest-falsifier
sweep generates them from assertions. You don't brainstorm what went wrong; you walk
the four cells for each control action and each one is a candidate hazard.

---

## 2. NTSB methodology — the report discipline worth stealing

The NTSB's value here is not its accident model (its reports are still largely
chain-of-events "sequence of events" narratives) but its **process discipline**, two
pieces of which map cleanly onto the plugin:

- **Factual record vs. analysis are separated by construction.** Fact-gathering is a
  distinct phase producing factual reports and a **public docket** — the raw evidence,
  released *before and apart from* any conclusions. Only afterward do specialists
  analyze the assembled facts to determine what happened. The investigator who gathers
  facts is institutionally prevented from smuggling a pet theory into the factual
  record.
- **The party system with a blinding rule.** Parties (manufacturer, operator, labor)
  supply technical expertise the Board lacks — but **lawyers and insurers are barred
  by law** from party teams, and parties work under NTSB supervision. The interested
  parties contribute facts; they don't get to write the verdict. (Even this has known
  failure modes: Boeing withholding the TWA 800 fuel-tank study; Rand 2000 flagged
  party conflicts of interest.)
- **"Probable cause" is deliberately calibrated language.** The Board issues a formal
  **determination of probable cause** — not "the cause," not "proven." It is the
  Board's best-supported finding, voted on at a public Board meeting, explicitly
  probabilistic in name. Findings, probable cause, and **safety recommendations** are
  distinct report sections; recommendations are the NTSB's primary tool, and it has
  **no enforcement power** — it separates "what we found" from "what should change."

---

## 3. Concrete plugin adoptions

### A. A trigger for the control-structure lens (vs. the broken-component hunt)

Add to SKILL.md §1 (convert assertions into hypotheses) a branch test. The default loop
hunts for a broken component / false ceiling. **Switch to the STAMP lens when the
broken-component hunt keeps coming up empty** — specifically when any of these hold:

- The post-incident review finds **every component operating to spec** and the failure
  still happened (the chain model has nothing to point at).
- The system has **multiple controllers acting on shared state** (human + automation,
  two services, a cache and its invalidator, a deployer and a health-checker).
- The leading story is **"X failed"** but X is a coordination/timing/feedback issue,
  not a part — races, stale reads, retry storms, autoscaler oscillation, mode
  confusion, a playbook that ran against a wrong picture of the fleet.

When triggered, the agent **models the incident as a control loop before naming a
culprit**: draw controller → actuator → controlled process → sensor → feedback, and
locate the **process-model gap** (what did the controller believe vs. what was true?).
"Hunt for the broken component" and "find the inadequate control" are different search
strategies; the second finds losses the first is blind to.

### B. The UCA taxonomy as a hypothesis generator

Bolt the four UCA cells onto §1's assertion sweep as a second generator. For each
control action in the modeled loop, mechanically enumerate:

| UCA type | Hypothesis it generates |
|---|---|
| Not provided | "The invalidation/ack/throttle/rollback was never issued → hazard" |
| Provided unsafely | "The action fired when state made it unsafe → hazard" |
| Wrong timing/order | "Fired too early/late or out of order relative to another controller → hazard" |
| Wrong duration | "Held too long / stopped too soon (retry, lock, backpressure) → hazard" |

Each non-empty cell becomes a numbered, falsifiable hypothesis with an H0, recorded in
the ledger exactly like an assertion-derived one — and then gets the cheapest-falsifier
treatment. This makes hypothesis generation **exhaustive over the control surface**
rather than dependent on the investigator imagining the right failure.

### C. The process-model gap as the but-for control case

§3 already mandates control cases for causal claims (the but-for test). STAMP sharpens
*what to control for* in coordination failures: the controlled experiment becomes
**"reconcile the controller's process model with ground truth at decision time."** The
negative control is "show a case where feedback was correct and the same control
algorithm produced a safe action" — which directly tests whether the *gap*, not the
*algorithm*, was the cause. This is the control-loop instantiation of rigor.md §3's
"necessary ≠ sufficient": a flawed process model is often necessary, the trigger
feedback delay sufficient, and the headline must say both.

### D. NTSB factual/analysis separation as ledger discipline

Two report-discipline rules for the ledger (SKILL.md §6) and the verdict step (§4):

1. **Factual record before analysis, structurally.** The ledger's evidence references
   (the commands, log lines, timestamps) are the **public docket** — recorded as raw
   fact, dated, *before* any verdict is attached. A verdict may never introduce a new
   "fact" that isn't already in the evidence section. This is the existing
   "evidence reference per verdict" rule, hardened: facts and conclusions live in
   separate sections, and the conclusion section may only cite, never add.
2. **"Probable cause," not "the cause."** Adopt NTSB's calibrated language as the house
   style for causal verdicts. CONFIRMED at <1.0 confidence is a **determination of
   probable cause** — best-supported, voted (council/peer-review), explicitly
   probabilistic — never "the proven cause." This already aligns with the skill's
   "never report 1.0 while a named unknown remains"; NTSB gives it a name and a
   precedent. Keep **findings / probable cause / recommendations** as distinct ledger
   sections, mirroring the skill's verified-vs-discovery tagging and the "next probe"
   discipline.

### E. The bridge to "circular causality," made explicit

The skill mentions circular causality as a reason to include the *reversed* hypothesis
("assume it's our fault and prove it / assume it's theirs"). STAMP is the formal
machinery underneath that instinct: in a control loop, cause **is** circular —
controller acts on process, process feeds back to controller, and a loss is a property
of the *loop*, not of either end. The reversed-hypothesis trick is the cheap version;
modeling the actual control loop (who controls whom, which feedback closed the circle)
is the rigorous version. When the reversed hypothesis feels forced because "both sides
were doing their job," that is exactly the signal to stop hunting a culprit and model
the loop — the loss lives in the coupling.

---

## 4. One-paragraph summary for a skill reference

> When the broken-component hunt comes up empty — every part to spec, multiple
> controllers on shared state, a coordination/timing/feedback failure — stop looking for
> a culprit and model the incident as a control loop (controller, actuator, controlled
> process, sensor, feedback). Find the **process-model gap**: what the controller
> believed vs. what was true. Generate hypotheses mechanically by walking the four
> Unsafe Control Action cells (not provided / provided unsafely / wrong timing-or-order
> / wrong duration) over each control action. Control for the gap, not just the
> algorithm. Record facts before conclusions (NTSB docket discipline), and write
> verdicts as **determinations of probable cause** — best-supported and probabilistic,
> never "the proven cause." This is the formal version of circular causality: in a
> feedback loop, the loss lives in the coupling, not in either end.
