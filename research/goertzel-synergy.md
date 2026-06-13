# Goertzel's frameworks → scientific-method plugin adoptions

Research for the falsification-first investigation workflow. Primary sources:
OpenCog/Hyperon wiki, arXiv abstracts (Goertzel 1703.04361; Weinbaum & Veitas
1505.06366), the PLN book (Goertzel, Iklé, Goertzel & Heljakka 2009), Wikipedia.
Distilled principles first, then concrete plugin changes. Speculative items are
flagged **[SPEC]**.

---

## Part 1 — Distilled principles

### Cognitive synergy (Goertzel, arXiv:1703.04361)
- Multiple cognitive processes cooperate over **one shared knowledge store**
  (the AtomSpace) and **rescue each other from "stuckness."** Synergy is defined
  formally around stuckness: when one process hits a combinatorial wall or local
  optimum, a *different* process — operating on the same intermediate results —
  supplies the move it couldn't find.
- The canonical division of labor in OpenCog/CogPrime:
  - **PLN** — probabilistic logical inference (deduction/induction/abduction).
  - **MOSES** — evolutionary program learning: evolves/recombines candidate
    Atomese programs; the route to *novel* structure deduction can't reach.
  - **Pattern miner** — finds structural regularities (frequent subgraphs) →
    analogical/inductive candidates.
  - **Concept blending** — combines two concepts into a new one.
  - **ECAN** (attention allocation) — rations resources so no single process
    "drowns in the search space" (the explicit combinatorial-explosion governor).
- Load-bearing idea for us: **no single reasoning mode is complete; you switch
  modes precisely when the current one is stuck**, and the switch is cheap
  because all modes read/write the same ledger.

### Patternist philosophy of mind (Goertzel, *The Hidden Pattern*, 2006)
- Mind = a system of patterns; intelligence = detecting patterns in the world
  **and in oneself** ("achieving complex goals in complex environments").
- The self-pattern-recognition half maps directly onto our self-audit lens
  (campaigns.md Pattern B: "audit our own prior verdicts for soft walls
  mislabeled as hard").

### Probabilistic Logic Networks — two-component truth values
- Every belief carries **(strength, confidence)**, both in [0,1]:
  - **strength** = the estimated probability itself (the mean — *what* you believe).
  - **confidence** = certainty *about* that strength, driven by evidence count:
    **c = N / (N + k)**. It encodes the spread of a second-order distribution
    over the true probability. c=0 → uniform (know nothing); c=1 → null spread.
- This is **imprecise probability**: a distribution *over* probabilities, not a
  point estimate. Two claims at strength 0.7 differ if one rests on N=3 and the
  other on N=10,000. IndefiniteTruthValue extends this to interval-plus-confidence
  (four floats / error bars) when naive inference washes confidence out.
- **Revision** merges two truth values weighted by their confidences (counts):
  high-confidence evidence dominates; agreeing low-confidence pieces accumulate.
- Inference rules (PLN book): **deduction** (A→B, B→C ⊢ A→C — forward chaining),
  **induction** (generalize shared premise), **abduction** (A→B, C→B ⊢ A→C —
  infer an explanatory premise from a shared consequence). Each has its own
  truth-value formula; abduction is the explicitly *explanation-generating* one.

### Open-ended intelligence (Weinbaum & Veitas 2015; Goertzel)
- Shifts from "agent solves a *pre-given* problem toward a *fixed* goal" to
  intelligence as **ongoing self-organizing individuation**: the system keeps
  generating *new* distinctions, problems, and goals; complexity and coherence
  grow through coordination, with no fixed endpoint or external success criterion.
- For us: a campaign shouldn't terminate purely at "all hypotheses have verdicts."
  A good finding **opens new questions** — the deliverable should capture what
  the result made newly askable, not just close the original ticket.

### Evolutionary / abductive hypothesis generation
- Abduction (Peirce): a *surprising* observation C triggers generation of
  candidate hypotheses A such that "if A were true, C would be a matter of
  course," then selection by simplicity / prior / explanatory power / **cheapness
  to test**, then deductive test. Analogy ("this anomaly resembles known pattern
  X") is a core candidate-*generation* mechanism.
- MOSES adds the **evolutionary/recombinative** route: when enumerated/deduced
  hypotheses are exhausted, *recombine* surviving partial explanations into new
  composite ones.

---

## Part 2 — Concrete plugin adoptions

### A. Mode-switching abduction step — "the hypothesis pool ran dry"

Add to SKILL.md step 7 ("Loop until clean") a sub-procedure for the failure mode
where a falsification pass kills every live hypothesis and **leaves no
replacement** — today the loop just declares "dry" and stops, which conflates
"exhausted the space" with "exhausted *my current way of searching* the space."
Borrow OpenCog's stuckness → mode-switch. When the pool is empty, escalate
through four generation modes (cheapest first), stopping as soon as one yields a
testable hypothesis:

> **Stuck-pool escalation.** A falsification pass that empties the hypothesis
> table is *stuckness in one reasoning mode*, not necessarily a true dry pass.
> Before declaring the campaign dry, cycle generation modes:
>
> 1. **Logical (deduction/induction)** — the default. Re-derive from confirmed
>    facts + the falsification log: what must be true given what survived?
> 2. **Analogical** — find a *solved* case (this repo's ledger, a sibling
>    system, a known failure class) that structurally resembles the open
>    anomaly; port its root cause as a candidate. (PLN abduction / pattern-miner.)
> 3. **Evolutionary / recombinative** — take the *partial* explanations and the
>    DO-NOT-RE-ATTACK kills and **recombine** them: two insufficient causes may
>    be jointly sufficient (this directly serves the "jointly-necessary factors"
>    failure mode already in SKILL.md). Mutate a killed hypothesis by relaxing
>    the one assumption that killed it. (MOSES analogue.)
> 4. **Probabilistic** — when no single crisp hypothesis survives, widen to a
>    *distribution* over causes: rank residual candidates by prior × cheapness,
>    and run the highest-information probe rather than demanding one named cause.
>
> Only after all four modes produce **no testable hypothesis** is the pass
> genuinely dry. Record which mode produced each new hypothesis (provenance) so
> the ledger shows the search wasn't single-mode.

This is a small, KISS addition: it reuses existing machinery (ledger, outcome
tables, halving ladder) and only adds a named escalation order. **[Partly SPEC]**
the four-mode ordering is our synthesis; OpenCog runs the processes concurrently
under ECAN rather than in a fixed cascade, but a cascade is the right fit for a
human-paced, single-investigator campaign.

### B. PLN-style two-component verdicts — strength vs confidence

Today the plugin reports **one calibrated number** (step 4: "Confidence
calibration … 0.55–0.75 is plausible inference"). That single number silently
fuses two things PLN keeps separate, and the conflation is a real source of
miscalibration:

- **claim strength** — how strongly the evidence points to the hypothesis being
  *true* (effect direction/magnitude). A clean control case that lands exactly as
  predicted → high strength.
- **evidence confidence** — how *much* evidence stands behind that strength,
  driven by replication count: PLN's **c = N/(N+k)**. One run, however clean, is
  low confidence even if its strength is high.

The current single number forces a lossy collapse: "0.7" can mean "moderate
effect, well-replicated" or "strong effect, seen once" — operationally very
different next actions. **Adoption:** report verdicts as **(strength,
confidence)** where the campaign has more than one live hypothesis:

> Verdict: CONFIRMED — strength 0.9 (effect landed exactly on the predicted
> outcome row), confidence 0.5 (n=1 clean run; no replication yet).
> → Next action is dictated by the *low* component: replicate to n≥3.

Rules that fall out, consistent with existing SKILL.md guidance:
- **The lower component drives the next action** — high strength + low confidence
  → replicate (don't act); low strength + high confidence → the hypothesis is
  genuinely weak (stop chasing it). This sharpens the existing "named missing
  probe" discipline.
- **Confidence comes from count, not vibes**: tie it to the "State n up front"
  rule (step 2). n=1 caps confidence low *by construction*, which formalizes the
  existing "a single run is an anecdote" line.
- **Revision rule for accumulating evidence**: when a second probe agrees, merge
  confidence-weighted (counts add) — strength barely moves, confidence rises.
  When probes *disagree*, that's not low confidence — it's an unmodeled
  interaction (already flagged in step 3); surface it, don't average it away.
- Keep the **single number for cheap/decisive cases** — the mini-ledger path
  (one probe settles it) doesn't need two components; this is for contested,
  multi-hypothesis campaigns where the strength/confidence split actually changes
  what you do next. (Matches the existing "method weight scales with evidence
  cost" stance.) **[SPEC]** on exact reporting format; the *concept* is solid and
  directly from PLN.

How it differs from our current single number, in one line: **our number answers
"how sure am I?"; PLN answers "how strong, and on how much evidence?" — and the
second question's two answers can pull in opposite directions.**

### C. Open-ended "what did this finding open?" continuation

Add to step 6 (ledger) / the reporting contract a required closing field. Today
the loop optimizes for *closure* (every hypothesis gets a verdict → dry → stop).
Open-ended intelligence says a strong result also *expands the problem space*.
Capture that instead of discarding it:

> **Opened-questions field.** Every CONFIRMED or FALSIFIED verdict ends with
> **what it made newly askable**: a new candidate hypothesis the result suggests,
> an adjacent ceiling now worth testing, or a generalization to probe next. These
> are logged as *discovery* claims (the plugin's existing tag) with their exact
> next probe — they are not part of the current campaign's done-criteria, but
> they seed the next one.

This is cheap and additive: it reuses the existing **discovery** tag and
"exact next probe" requirement. It guards against the existing **premature
closure** failure mode from the other direction — instead of "we stopped from
fatigue," it's "we noticed what the win opened and wrote it down before context
compacted." It also feeds **mode A**: the opened-questions list is the first
place the stuck-pool escalation looks for its next logical/analogical candidate.

**Boundary / [SPEC]:** keep this bounded — open-endedness is a *seeding*
mechanism, not a license to never finish. The campaign's done-criteria stay
exactly as in step 7 (dry pass, all verdicts in, INCONCLUSIVEs name their probe).
Opened questions go in a clearly separate "next campaign" section so they can't
silently reopen a DO-NOT-RE-ATTACK kill.

---

## Where each adoption lands
- **A (mode-switch)** → SKILL.md step 7 + campaigns.md (new Pattern, or extend B).
- **B (two-component verdict)** → SKILL.md step 4; artifacts.md verdict template.
- **C (opened-questions)** → SKILL.md step 6 + reporting contract in campaigns.md.
