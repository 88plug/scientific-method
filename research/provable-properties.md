# Making Systems Claims Provable, Not Just Measured

A claim "measured on N seeds" reports outcomes for the inputs you happened to draw.
A *provable* claim says something about the whole input space. The job is to pick the
cheapest technique that upgrades your evidence as far up the hierarchy as the claim allows.

## The honest hierarchy

```
measured  <  property-tested  <  exhaustively-checked-in-scope  <  proven
(N seeds,    (N generated cases  (every case up to a bound,        (all cases,
 a sample)    + shrinking,         conclusive within that bound)     unbounded)
              still a sample)
```

- **measured** — ran it on some hand-picked or random inputs; tells you about those inputs only.
- **property-tested** — stated an invariant over *all* inputs, let a generator (QuickCheck / Hypothesis) draw N cases (default ~100). A failure is definitive; a pass is **absence of counterexample among the samples, not proof**. Shrinking turns any failure into a *minimal* reproducer.
- **exhaustively-checked-in-scope** — enumerated *every* case up to a small bound (Alloy / a model checker / brute-force over a finite domain). Within the bound, "no counterexample" is conclusive. Rests on the **small-scope hypothesis**: a high proportion of bugs have a small counterexample, so a small bound catches most of them — but says nothing beyond the bound.
- **proven** — a deductive argument (analytic proof, or model-checking a *finite-state* design that covers the real state space) covers all cases, unbounded.

Key honesty rule: report which rung you are on, and never let a green property-test suite be written up as "proven." It is property-tested.

## Decision guide by claim type

For each claim, the question is: what upgrades "measured on N seeds" to a statement over the space?

### 1. Correctness (function/transform does the right thing)
- **Technique:** property test against an *invariant* or *oracle* (round-trip `decode(encode(x))==x`; postcondition `sorted(out) && perm(out,in)`; agreement with a reference). Generate N cases + shrinking.
- **Upgrade:** measured → property-tested. The invariant holds *by construction over all generated inputs*, and any violation shrinks to a minimal case.
- **Go further:** if the input domain is small/finite (e.g. all 8-bit inputs, all states of a small protocol), **enumerate exhaustively** → checked-in-scope. If there's a clean algebraic argument, **prove** it.
- **Provenance:** QuickCheck (Claessen & Hughes) and Hypothesis both frame a pass as "no counterexample found," explicitly *not* a proof.

### 2. Never-violates-bound (latency ceiling, memory cap, no-overflow, no-data-loss invariant)
- **Technique:** express the bound as a *safety invariant* ("∀ reachable state: x ≤ B") and **model-check the design** (TLA+/TLC, Alloy) — exhaustive over all reachable states / all states up to scope.
- **Upgrade:** measured → checked-in-scope (often effectively proven, when the model's state space is finite and fully covered). This is the sweet spot for model checking: bounds and "bad thing never happens" are exactly safety properties.
- **Amazon/TLA+ evidence:** TLC found a data-loss bug in DynamoDB whose shortest error trace was **35 high-level steps** — a deep interleaving that "passed unnoticed through extensive design reviews, code reviews, and testing." Engineers got useful results in 2–3 weeks; specs were a few hundred lines. Caveat they state plainly: this proves the *design*, not that the code matches it ("we do not know").
- **When NOT worth it:** if the bound is over a huge/continuous state space with no finite abstraction, model checking blows up — fall back to property testing the worst-case generators plus an analytic argument for the tail.

### 3. Equivalence (refactor matches original; two impls agree; optimization preserves behavior)
- **Technique:** **differential testing** — run both on the same generated inputs and assert equal outputs; the other implementation *is* the oracle. Add shrinking. For finite input domains, **enumerate exhaustively** (decisive). For two *designs*, assert equivalence as an Alloy/TLA+ check.
- **Upgrade:** measured → property-tested → (if domain finite) checked-in-scope. Differential testing is the strongest cheap oracle because you don't need to know the right answer, only that two things must agree.
- **Use it for:** "aggressive performance optimization is safe" — Amazon reported teams made optimizations they "otherwise wouldn't have dared" precisely because they could check the optimized design against the verified one.

### 4. Termination (no infinite loop / always makes progress / no deadlock)
- **Technique:** for finite-state designs, **model-check** for deadlock and for a *ranking/variant* that strictly decreases (TLC checks deadlock directly; absence of cycles in the reachable graph). For algorithms, an **analytic proof** via a well-founded ranking function is usually the right tool — termination rarely reduces to a random-sampling claim.
- **Upgrade:** measured → checked-in-scope (model check) or → proven (ranking-function argument).
- **Note:** property testing can only *fail* to terminate (timeout = found a non-terminating case); it cannot establish termination, since "ran for a while" is just measured.

### 5. Fairness / liveness (every request eventually served; no starvation; progress under scheduling)
- **Technique:** **model-check liveness properties under fairness assumptions** (TLA+ temporal `[]<>` / `<>[]`, weak/strong fairness). This is the one class where naive testing is weakest: liveness violations are infinite behaviors, invisible to any finite run.
- **Upgrade:** measured → checked-in-scope (proven for the modeled state space). You *must* state the fairness assumptions explicitly — a liveness claim is meaningless without them.
- **Caveat:** liveness checking is more expensive than safety and was de-emphasized even in Amazon's safety-first practice; budget for it deliberately, and prefer reducing a fairness claim to a safety invariant ("a served counter is monotetc.") when you can.

## Picking the technique (cheat sheet)

| Claim | First reach | Upgrade if cheap | Ceiling |
|---|---|---|---|
| Correctness | property test + oracle/invariant + shrink | exhaustive (finite domain) | analytic proof |
| Never-violates-bound | safety invariant, model-check design | — | proven if state space finite |
| Equivalence | differential test (other impl = oracle) | exhaustive enumeration | design-equivalence proof |
| Termination | analytic ranking function | model-check deadlock/cycles | proven |
| Fairness/liveness | model-check under explicit fairness | reduce to safety invariant | proven for modeled space |

**Operating rules for the plugin:**
1. Always write the claim as a *universally quantified property over a named input space*, then ask "what's the cheapest rung above `measured` I can reach?"
2. A passing property suite is **property-tested**, never "proven." State the rung.
3. Exhaustive-in-scope beats property-tested when the domain is small enough to enumerate — and it is *conclusive within the bound*, so prefer it whenever the bound is reachable.
4. Use a *differential oracle* whenever a second implementation/reference exists — it sidesteps needing to know the right answer.
5. Bounds, "bad thing never happens," and fairness are model-checking's home turf; correctness/equivalence over finite domains are exhaustive-enumeration's; algebraic claims and termination want proofs.

## Sources
- Newcombe et al., *How Amazon Web Services Uses Formal Methods* (CACM 2015) / Lamport's TLA+ excerpt — 35-step DynamoDB bug missed by review/testing; safety-property focus; design-not-code caveat; 2–3 week learning cost.
- Claessen & Hughes, *QuickCheck* — properties as universally-quantified executables; random generation; shrinking to minimal counterexamples; pass ≠ proof.
- Hypothesis docs — property-based testing, strategies, default ~100 cases, falsification framing.
- Jackson, *Alloy* / small-scope hypothesis — bounded exhaustive SAT-based checking; conclusive within scope, silent beyond it.
