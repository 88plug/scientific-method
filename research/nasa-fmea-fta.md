# NASA's failure-anticipation canon: FMEA/FMECA, Fault Tree Analysis, mishap taxonomy

Distilled from primary/authoritative sources for adoption into the scientific-method plugin.
The plugin today is *backward-looking* (falsify a claim, root-cause an incident that already
happened). NASA's canon adds the *forward-looking* half — anticipate failure modes before a
risky change ships — plus a structured combination-of-causes model the plugin's flat H1..Hn
list cannot represent, and a causal vocabulary (proximate / root / contributing) that sharpens
verdicts.

Sources: Wikipedia FMEA/FMECA, Fault Tree Analysis, Root Cause Analysis, Bow-tie diagram;
NASA OSMA mishap-investigation page (NPR 8621.1, Event & Causal Factor Trees, NCAT).

---

## Part 1 — Distilled principles

1. **Two complementary directions of analysis, and you need both.** FMEA is *inductive /
   bottom-up*: start at a component, ask "if this fails, what happens?", catalog every
   single-point failure. FTA is *deductive / top-down*: start at one undesired outcome (the
   "top event") and work backward through logic gates to the fault combinations that produce
   it. FMEA exhaustively finds *initiating* faults but is weak at multi-failure and
   system-level effects; FTA models combinations and redundancy but cannot enumerate all
   initiators. The plugin's `H1..Hn` list is FMEA-shaped (a flat catalog of candidate
   causes); it has no FTA-shaped tool at all.

2. **Anticipation belongs *before* the change, not after the incident.** "FMECA should be a
   living document during development... performed after hardware is built it would be of
   little use." The plugin only activates reactively (a number to verify, an incident to
   root-cause). A lightweight pre-mortem FMEA is the missing proactive entry point.

3. **Failure mode ≠ failure cause ≠ failure effect — keep the three distinct.** *Mode* = the
   way it fails (contact stuck open, beam fractured). *Cause/mechanism* = the underlying defect
   (fatigue, fretting corrosion, bad requirement). *Effect* = the consequence, tiered by
   indenture level: local → next-higher → system end effect. Always rate the **worst-case end
   effect**, and remember one mode can have several causes.

4. **Score risk on three axes, not one: Severity × Occurrence × Detectability.** The third
   axis — *detectability* — is the one engineers forget and the one most relevant to software:
   a high-severity, low-probability bug that is *also invisible until users hit it* (no test,
   no alert, silent) is far more dangerous than the severity alone suggests. RPN = S×O×D
   surfaces exactly this.

5. **RPN is a *triage sort*, not a measurement — its ordinal math is broken.** S, O, D are
   ordinal ranks; "multiplication is not defined for ordinal numbers," so RPN suffers rank
   reversals (a less serious mode scoring higher). Use RPN/Action-Priority to *rank what to
   probe first*, never as a real probability. This is the same trap the plugin already warns
   about with derived numbers — RPN is a derived number.

6. **One top event per fault tree; severity gates the depth of analysis.** Each tree examines
   exactly one undesired state. The most severe failure conditions get the most extensive
   trees; trivial ones get a stub. Don't build a tree per hypothesis — build one per *outcome
   you're trying to prevent or explain*.

7. **AND gates are where safety lives; OR gates are where fragility lives.** An OR gate fires
   if *any* input does — these multiply failure probability (P_A + P_B). An AND gate fires only
   if *all* inputs do — these are your redundancy/defenses, and they multiply *reliability*
   (P_A · P_B). A system with no AND gates between an initiating fault and catastrophe has no
   defense in depth. Reading a tree = finding the OR-chains with no AND guarding them.

8. **Minimal cut sets are the payload of a fault tree.** A *cut set* = a combination of events
   that together cause the top event; *minimal* = remove any one and it no longer fires. A
   single-element minimal cut set is a **single point of failure** — the highest-value finding.
   Cut-set size is a structural reliability metric: all size-1 cut sets are SPOFs to eliminate;
   small cut sets are fragile paths.

9. **Common-cause failures defeat redundancy and break the independence math.** When one root
   event feeds multiple branches (shared library, shared config, shared power, shared
   on-call human), an apparent AND gate (two "independent" defenses) is secretly an OR gate.
   This is *the* classic reason "we had redundancy and it still failed." The plugin's
   independence assumption in any AND-style reasoning must be explicitly checked.

10. **Proximate cause ≠ root cause ≠ contributing factor — and the root is defined by
    removal.** *Proximate/direct cause* = the immediate surface symptom (blown fuse, the line
    of code that threw). *Root cause* = "a factor [whose] removing it prevents the problem from
    recurring." *Contributing factor* = "affects the outcome but is not the root cause" —
    removing it improves things but "does not prevent recurrence with certainty." NASA's own
    rule: a contributing factor can itself have a root cause, and it "should be listed as
    such."

11. **There can be more than one root cause, and "root" is relative to where you stop.** Causal
    graphs "have many levels"; analysis stops at what is root "in the investigator's eyes."
    NASA requires you to *attempt* to find root causes but acknowledges "No, [a root cause is]
    not [always found]." This is the plugin's INCONCLUSIVE discipline applied to causation:
    don't manufacture a single tidy root when the evidence shows several, or shows the trail
    runs off the edge of your control.

12. **Corrective action attaches to the root, not the symptom — and prefer design over
    discipline.** Fixing only the proximate cause (replace the fuse) restores operation but the
    problem recurs. NASA/RCA practice: corrective actions should target root causes *and*
    contributing factors, favor the Hierarchy of Hazard Controls / mistake-proofing
    (engineered barriers) over administrative rules or "add more training," and close with an
    *effectiveness review* — if recurrence isn't reduced, the RCA reopens. An "Extent of Cause"
    review (how widely did this cause reach?) is named as the most common reason corrective
    plans fail.

---

## Part 2 — Concrete plugin adoptions

### Adoption A — Lightweight pre-mortem FMEA before a risky change

A new proactive trigger for the skill: *before* a risky change (migration, schema change,
dependency bump, infra cutover, a "this is irreversible" step), run a 20-minute FMEA instead of
waiting for the incident. This fits the existing "before any irreversible step" gate in step 7
of the SKILL, which currently only says "adversarial review + staged rollout" — FMEA makes that
review *structured*.

The worksheet (compressed from NASA's columns to what a software agent can fill):

| # | Component / step | Failure mode (how it breaks) | Cause | End effect (worst-case) | S | O | D | RPN | Detection gap → mitigation |
|---|---|---|---|---|---|---|---|---|---|

Scoring (1-5 ordinal, keep it coarse — precision here is false):
- **S (Severity):** 1 = cosmetic → 3 = degraded function → 5 = data loss / outage / silent
  corruption.
- **O (Occurrence):** 1 = would need a freak combination → 5 = likely on first run.
- **D (Detectability):** **1 = a test/alert catches it before users do → 5 = silent until a
  user or auditor stumbles on it.** (High D = bad. This is the software-critical axis.)

Process:
1. List the components/steps the change touches (the "functions" — NASA: start from functions,
   it gives the best yield).
2. For each, one failure mode at a time, fill the row. Assume interfaces operate in-spec, then
   *re-run* treating each interface's failure as a cause (NASA's robustness-extension trick).
3. **Sort by RPN, act on the top of the list — never treat RPN as a probability.** The output
   isn't a risk score; it's an *ordered probe queue* that plugs straight into the plugin's
   "cheapest falsification first" / successive-halving ladder: the highest-RPN rows become the
   first hypotheses to falsify with a real probe before shipping.
4. Every row with **D ≥ 4 (silent failure) is a finding by itself**, regardless of RPN — it
   means "we would not know if this happened." The mitigation is "add the test/alert/assert
   that lowers D," and that mitigation ships *with* the change.

Weight rule (consistent with the SKILL's "method weight scales with evidence cost"): a
one-line config change gets a 3-row mental FMEA, not a worksheet. A schema migration on a
production table gets the full table written to the ledger. Theater is as corrosive here as
anywhere.

### Adoption B — When to build a fault tree instead of a flat H1..Hn list

The plugin's hypothesis list is flat: H1, H2, ... Hn, each independently CONFIRMED / FALSIFIED.
That representation is correct when causes are **mutually exclusive or independent** — exactly
one of them did it, and falsifying one doesn't change the others. **Build a fault tree instead
when causes *combine*.** Concrete decision rule:

**Use a tree (not a flat list) when any of these hold:**
- The incident required **two or more conditions to be true simultaneously** ("the retry storm
  *and* the cache being cold *and* the rate-limiter mis-tuned"). A flat list forces you to crown
  one of N jointly-necessary factors as "the cause" — the exact single-cause bias the SKILL's
  failure-modes section already warns against ("crowning one of two jointly-necessary factors
  the root cause"). The tree represents the AND explicitly.
- You suspect a **common-cause failure** — one event that knocked out supposedly independent
  defenses. The tree shows the same basic event feeding multiple branches; a flat list hides
  the shared dependency.
- You need to reason about **redundancy / defense-in-depth** ("we had a fallback, why did it
  still fail?"). AND gates *are* the defenses; the tree shows which were defeated together.

**Stay with the flat H1..Hn list when:**
- Causes are competing single explanations (it was the bad deploy *or* the vendor *or* the
  config — find which). This is FMEA-shaped and the existing machinery is ideal.

How an agent builds the tree (text form — no special tooling needed):

```
TOP: checkout latency spike >2s (the one undesired event)
└─ OR
   ├─ AND  (both needed — this whole branch is a finding)
   │   ├─ BASIC: connection-pool exhausted   [evidence: pool metric pinned at max 14:02]
   │   └─ BASIC: retry-on-timeout enabled      [evidence: config flag, deployed 13:55]
   └─ BASIC: DB failover in progress           [FALSIFIED: no failover in window]   ← ruled_out
```

- Each leaf is a **basic event** carrying an **evidence reference** — same standard as a plugin
  hypothesis verdict. A leaf with no probe behind it is "undeveloped," not "true."
- **Minimal cut sets are the deliverable.** Solve the tree by hand: the cut set above is
  `{pool exhausted, retry enabled}` — a **size-2 cut set**, both elements necessary, neither
  sufficient. The verdict headline must name *both* (this is the SKILL's "necessary ≠
  sufficient" rule made structural). A **size-1 cut set = single point of failure** = the
  highest-priority fix.
- **Falsifying a leaf prunes the tree:** mark it `ruled_out` with the killing evidence (the
  plugin already maintains a `ruled_out` list — leaves map onto it directly). If pruning a leaf
  empties a cut set, that whole failure path is eliminated — a stronger, more satisfying
  closure than crossing one item off a flat list.
- **Bow-tie extension** for incidents where the question is also "why did the blast radius get
  so big?": keep the fault tree on the left (causes → event), add an event tree on the right
  (event → consequences, each consequence gated by a mitigation barrier that did or didn't
  hold). Use it as a *rapid scoping* tool to decide which branch deserves a full probe — it is
  explicitly "less rigorous than full fault/event tree analysis."

### Adoption C — Proximate / root / contributing taxonomy in verdicts

Today a plugin verdict says CONFIRMED/FALSIFIED/INCONCLUSIVE with confidence. For *causal*
verdicts (incident root-causing), add a **three-tier causal label** so the report can't collapse
a chain into one misleading line:

- **Proximate cause** — the immediate trigger / surface symptom. State it, then explicitly mark
  it as proximate so no one mistakes it for the fix target. ("Proximate: the null-deref at
  `handler.go:212`.")
- **Root cause(s)** — defined operationally by the SKILL's existing but-for test, which is
  *exactly* RCA's removal test: a factor is root iff removing it prevents recurrence. Plural
  allowed and expected. ("Root: the deploy pipeline skips schema-compat checks — removing that
  gap prevents recurrence.")
- **Contributing factors** — present and load-bearing but not sufficient for prevention.
  ("Contributing: alert threshold set too high, so detection lagged 40 min.") Per NASA, each
  contributing factor *may itself have a root cause* — recurse one level where it pays.

Verdict-discipline upgrades this gives the plugin:

- **Kills "blame the proximate cause."** The SKILL warns against premature closure and
  convenient blame; the taxonomy makes the failure visible — a verdict that names only a
  proximate cause is structurally incomplete, like a FALSIFIED with no evidence reference.
- **Confidence binds per tier.** You can be 0.95 on the proximate cause (you can see the stack
  trace) and 0.6 on the root cause (the but-for control case is missing) — these are *different
  claims* and the SKILL already forbids one house number for all of them. The 0.90+ bar still
  applies to the root: it needs temporality **plus a control case** (the but-for ladder), not
  just "it's upstream of the symptom."
- **INCONCLUSIVE has a natural home.** When the trail runs off the edge of your control (vendor
  internals, a rotated log, a one-time transient), the honest output is "proximate cause
  CONFIRMED; root cause INCONCLUSIVE — the deciding probe is X." NASA's own answer to "is a root
  cause always found?" is *"No, but they need to attempt to determine if any exist."* This is
  the SKILL's anti-manufactured-closure stance stated in mishap-investigation language.
- **Corrective actions attach to root + contributing, prefer engineered over administrative,
  and get an effectiveness review.** A fix that patches only the proximate cause is flagged as
  recurrence-prone. Prefer a mistake-proofing barrier (a CI gate, an assertion, a type that
  makes the bad state unrepresentable) over "we'll be more careful / add a runbook step." Close
  with the SKILL's existing loop: re-probe after the fix; if the symptom can recur, the verdict
  reopens — RCA's effectiveness review and the plugin's "loop until clean" are the same gate.
