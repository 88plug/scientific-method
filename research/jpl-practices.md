# JPL engineering & investigation practices — distilled for the scientific-method plugin

Research basis: Holzmann's *Power of Ten* (IEEE Computer, June 2006; spinroot.com/p10),
JPL fault-protection papers (Morgan, NTRS 20060044316 / 20100002848; Methodology NTRS
20100021298; arXiv 2305.11902), Mars Climate Orbiter Phase I & II boards
(llis.nasa.gov, larc.nasa.gov MCO Phase II), Mars Polar Lander failure board, Test-Like-You-Fly
(Aerospace Corp GSAW 2014; NASA NTRS 20260000215; JPL Design Principles cmap), and the
JPL ISA / Problem Reporting System (PRS) anomaly-reporting practice.

The throughline: **JPL engineers a system that must be right when nobody can intervene,
and they treat verifiability, not cleverness, as the property that earns trust.** That is
the same stance this plugin takes toward numbers and root causes. Every adoption below maps
a JPL practice onto an existing plugin discipline.

---

## 1. The Power of Ten — verifiability over expressiveness

Holzmann's ten rules for safety-critical C deliberately **trade expressive power for
analyzability**. The recurring justification across the rules: if a static checker cannot
*mechanically prove* a property, the code is not acceptable — restricting the language is the
price of making correctness checkable by tools rather than merely plausible to a human reader.

The ten rules (paraphrased, with rationale):

1. **Simple control flow** — no `goto`, `setjmp`/`longjmp`, recursion. Cyclic call graphs make
   stack bounds and termination unprovable.
2. **Fixed upper bound on every loop** — a tool must be able to prove statically the loop can't
   exceed a preset bound. Guarantees termination is *mechanically checkable*.
3. **No dynamic allocation after init** — removes allocator failures, leaks, fragmentation, and
   unpredictable runtime memory behavior.
4. **Functions fit on one page (~60 lines)** — each function stays a reviewable unit.
5. **≥2 assertions per function on average** — side-effect-free Boolean tests for "conditions
   that should never happen", each with an explicit recovery action; an assertion a checker can
   prove always-true/false *violates* the rule (no `assert(true)` padding). Assertions are not a
   test aid — they catch misbehaving code at runtime "at the earliest possible moment" and must
   never be compiled out.
6. **Smallest possible scope for data** — limits where a value can be corrupted; narrows diagnosis.
7. **Check every return value and every parameter at boundaries** — defensive interfaces stop
   silent error propagation across the call boundary.
8. **Restrict the preprocessor** — only includes + simple macros; conditional compilation
   multiplies the variants that must be verified.
9. **Restrict pointers** — ≤1 dereference level, no function pointers; indirection defeats static
   analysis of data and control flow.
10. **Zero warnings at the most pedantic setting from day one, plus daily static analysis** —
    tooling is a *continuous gate*, not an afterthought.

Rules 2, 5, 10 state the philosophy outright (properties must be *tool-provable*); rules 1, 3,
8, 9 remove the features that break provability. Absorbed into the JPL Institutional Coding
Standard; NASA's review of Toyota throttle firmware found 243+ violations of these rules.

**Distilled principle:** prefer the form a checker can verify over the form that is clever or
terse. Constrain your own expressiveness so the correctness of a probe/finding is *mechanically
re-checkable*, not a matter of trusting the author.

## 2. JPL Design Principles / Flight Project Practices

From the JPL design-principles corpus and the Young report after the 1999 losses:

- **Test as you fly / fly as you test** is the *named system-verification philosophy*: use
  flight sequences, flight-like operating conditions, and the same software functionality. Where
  testing is impossible, verification is by *independent analysis*, never by assumption.
- Verification plans must cover **nominal AND off-nominal end-to-end** paths, plus environmental,
  fault-protection, flight-sequence, and cross-system verification.
- **Stress / margin testing beyond design level** to find capability boundaries — explicitly
  including "single faults that cause multiple-fault symptoms" and "subsequent faults in an
  already-faulted state."
- **Keep-it-simple** is a stated design principle: complexity must be *justified*, because
  simplicity is what makes verification and operations tractable (echoes KISS).
- **Single-point-of-failure policy, redundancy, and margins** are first-class requirements, not
  optimizations: the system must continue operating through a fault, not just detect it.
- **Heritage is a trap, not a credential.** MCO's nav team assumed Mars Global Surveyor heritage
  and therefore under-learned the actual spacecraft — they didn't know it transmitted the very
  velocity-change data that would have exposed the units bug. "It worked before / it's the same
  as X" is an assumption to be verified, not a reason to skip verification.

## 3. Fault protection as a discipline

JPL fault protection exists because **the urgency of a response often precludes interaction with
ground control** — light-time delay means the spacecraft must protect itself with no human in the
loop for hours. Core constructs (Morgan; Deep Impact FP methodology):

- **Monitor/response pairs**: a monitor detects the symptom of a fault or off-nominal condition;
  a paired response acts autonomously. Monitors graduate RawOpinion → Opinion
  (no-opinion / acceptable / unacceptable) → Symptom → Alarm(Fault) → Response.
- **Tiered responses**: early tiers attempt a *localized*, step-by-step fix; only unresolved
  faults escalate to system-level response. Recovery is gated by urgency, MaxRetry, hardware
  availability, hazardous-vs-ordinary classification.
- **Fault Containment Regions (FCRs)**: the architecture scopes mitigation/recovery per FCR so a
  fault can't propagate past its boundary. Credibility is proven both top-down (fault-tree) and
  bottom-up (functional FMEA).
- **Safe Mode**: a general-purpose response that drops the craft into a *lower-power, safe,
  predictable* state so human experts can diagnose complex faults at leisure. The autonomous
  layer's job is to *survive and preserve diagnosability*, not to solve everything.
- An emerging hazard (arXiv 2305.11902): autonomous executors and fault-protection responses
  issuing *competing command streams* — contention between two autonomous agents acting on the
  same system. Directly relevant to multi-agent campaigns.

## 4. Anomaly handling — ISA culture & the Lessons Learned system

JPL's structured anomaly channel is the **Incident, Surprise, Anomaly (ISA)** report, inside the
Problem Reporting System (PRS). The defining cultural property: **every surprise gets a record —
including benign ones.** Studies catalogued 1160 ISAs for Mars Global Surveyor and 536 for Mars
Odyssey; anomalies are counted *with no preference for criticality*, ground and flight grouped
together, each individually reviewed and characterized by source and corrective action. A common,
fully-legitimate corrective action is **"Use As Is" — take no action** — the record still exists.
The point is the *ledger of surprises*, plotted over time (peaks cluster at mission start and at
key milestones), not a filter that only logs the scary ones. Each ISA carries: problem described
→ verification → corrective action → review/approval → closure.

The ISA channel feeds the **NASA/JPL Lessons Learned Information System (LLIS)**: designs are
reviewed against the LLIS database and NASA/JPL Alerts early and at life-cycle checkpoints, so a
past event in a *different* program can preclude recurrence ("propulsion contamination", "boom
deployments", etc.). Lessons are reusable knowledge, not mission-local trivia.

**The MCO board's verdict makes this load-bearing:** the units error was "at the heart of the
mishap", but the *causal* failure the board named was the **breakdown of the ISA process** —
the team used e-mail instead of formal problem resolution, dissenting navigators' concerns were
dismissed for not filling out the form, and the discrepancy "slipped through the cracks." The MPL
recommendations that followed: "train the entire team on the ISA Process… encourage *any* issue to
be written up as an ISA… review all current anomalies and generate appropriate ISAs… Mission
Safety First." A surprise with no record is a defect waiting to recur.

## 5. Failure-board canon

**Mars Climate Orbiter (1999):** Lockheed's ground software output thruster impulse in
pound-force-seconds; NASA's nav software consumed it expecting newton-seconds — values wrong by
4.45×, corrupting the trajectory through cruise. Lost at Mars insertion. Board's framing
(Weiler): *"The problem here was not the error; it was the failure of NASA's systems engineering,
and the checks and balances in our processes, to detect the error."* NASA explicitly did **not**
blame the contractor — it owned the missing verification. The unit mismatch was a *contract
violation on a software-to-software interface that nobody checked against ground truth.* Process
changes: verify interface *conformance* (a correct spec is useless unmonitored), independent
end-to-end validation of nav data, lower the barrier to raising concerns, restore mission
assurance during operations.

**Mars Polar Lander (1999):** the three landing legs carry Hall-effect touchdown sensors; leg
deployment (still on the parachute) produces a **transient false touchdown signal**. The flight
software accepted a touchdown valid if it persisted two readings — and most transients qualified.
The logic was *supposed* to ignore indications before the sensing logic enabled, but that
masking "was not properly implemented"; the spurious bit was retained, so when sensing enabled at
~40 m the software immediately cut the engines. Free-fall from 40 m → unsurvivable impact. The
transient behavior *was visible in deployment tests* but the software requirements never accounted
for it — **an untested sensor/software interaction that ground testing didn't exercise under
flight-like conditions.** This is the canonical "test like you fly" failure.

**"Faster, Better, Cheaper" retrospective (Young report):** the program was under-funded by ≥30%;
the twin losses showed that cutting cost while *also* cutting systems-engineering rigor —
cross-checks, end-to-end test coverage, channels for raising concerns — invites mission-ending
errors that a single cheap verification step would have caught. The lesson is not "spend more"; it
is **never cut the verification, the controls, or the surprise-reporting channel to go faster.**

---

# Concrete plugin adoptions (highest-leverage first)

### A. ISA discipline — every surprise gets a ledger record, even when benign
*Extends §6 (Persist the ledger) and §4 (record verdicts).* Today the ledger captures
hypotheses and verdicts. Add a **surprise log**: any observation that violated expectation —
even one that turns out benign, even one whose corrective action is "use as is / no action" —
gets a one-line record (what surprised you → checked → disposition). JPL's MCO loss was caused
not by the units bug but by a surprise that went to e-mail instead of the ISA system and slipped
through. The cheapest probe (§0) only helps if the surprise that *triggers* it is recorded. The
benign ones matter: the discipline is the habit of recording, and surprises cluster at milestones
(insertion, publish, merge) exactly where the plugin's irreversible-step gate (§7) lives.
**Implementation:** a "Surprises" subsection in the ledger template (artifacts.md), one row per
anomaly — `| # | Surprise (expected vs observed) | Probe | Disposition |` — with "no action /
expected after all" as a first-class, fully-acceptable disposition.

### B. Verifiability over cleverness — a probe-design rule
*Extends §3 (Design controlled experiments).* Holzmann's whole standard is: prefer the form a
tool can *mechanically check* over the form that is clever. Adopt as an explicit probe-design
constraint: **a probe whose correctness can't be independently re-checked is worth less than a
plainer probe that can be.** Concretely — bounded/terminating probes (no open-ended loops),
return-value and input checks at the boundary (Rule 7 → validate that the probe actually
measured what you think, e.g. allocation-sanity / A-A checks already in §3), and a probe a second
agent can re-run from the Reproduce block (§6) and get the same number. Cleverness that isn't
re-checkable is a liability, not a flex.

### C. Fault-containment thinking for autonomous agents
*Extends "Scaling up: multi-agent campaigns" and the design/execute split.* JPL agents act when
nobody can intervene for hours — so they use **monitor/response pairs, tiered (localized-first)
recovery, fault-containment regions, and a safe mode that preserves diagnosability.** Map onto
agent campaigns: (1) give each fanned-out agent a *containment region* — it writes probes and
findings but cannot mutate shared state or the ledger, so a bad agent can't propagate corruption
(the design/execute split is already an FCR; name it as one). (2) Define a **safe mode** for
agents: on contradiction or low confidence, halt into INCONCLUSIVE + named-missing-probe rather
than improvising — the autonomous layer's job is survive-and-preserve-diagnosability, not force a
verdict. (3) Heed the arXiv FPE hazard: **two autonomous agents issuing competing command streams**
is a real failure mode — the parent must own execution serially (already the rule; the JPL
contention case is the institutional validation).

### D. The MCO units lesson validates ground-truth-units checking
*Extends §3 "Measure against ground truth, not metadata."* The plugin already says read the
silicon, build claimed-vs-observed matrices, let the empirical column win. MCO is the canonical
institutional proof: a 4.45× error survived all the way to Mars because **the units on a
cross-component interface were a documented spec that nobody verified against ground truth.**
Adopt a named **units/interface ground-truth check**: whenever a number crosses a boundary
(tool→tool, agent→agent, log→report), assert its units/scale explicitly and confirm both sides
agree against an observed value, not against the spec that says they should. Weiler's line is the
banner: *"The problem was not the error; it was the failure of the checks and balances to detect
it."* A finding's units are part of its evidence reference (§4), not a footnote.

### E. "Test like you fly" → test the probe under finding-like conditions
*Extends §5 (Adversarial verification) and the §7 irreversible-step gate.* MPL died from a
sensor transient that *appeared in test data* but was never exercised under flight-like
deployment conditions. The plugin analogue: a probe validated under clean/idealized conditions
can hide the very interaction that breaks the finding in production. Before a CONFIRMED verdict
on anything irreversible, ask **"was this measured under the conditions the conclusion will be
used in?"** — same load, same concurrency, same transients, end-to-end not component-only (the
"per-component win must also be an end-to-end win" check in §5 is exactly this). Where a
flight-like probe is impossible, fall back to *independent analysis* (JPL's own escape hatch) and
say so — never to assumption. Add off-nominal / stress conditions (faults-on-top-of-faults) to
the probe matrix, mirroring JPL's mandated stress testing.
