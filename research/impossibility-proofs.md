# Impossibility & lower-bound proofs — a toolkit for the scientific-method plugin

When an investigation keeps failing to hit a target, there are two distinct
conclusions, and the plugin must not conflate them:

- **"We failed to find a way."** Absence of a found solution. Weak. Confidence
  decays as soon as someone smarter, or with more time, tries again. A verdict
  built on this is a guess wearing a lab coat.
- **"No way exists."** A *proof* that the target lies above a ceiling that
  binds **every** policy/algorithm/input in the stated model. Strong. It quantifies
  over all candidates at once, so a cleverer competitor changes nothing.

The whole value of this toolkit is the jump from the first to the second. The
plugin already crossed it three times in eval (r9s03: Little's-law backlog floor
proving `long_p99 ≤ 400` infeasible for any work-conserving policy; r9s06: a
Belady-style clairvoyant ceiling proving a 1.25x prewarm target unreachable even
with perfect foresight; r4s04: a deterministic refutation showing a "flaky" claim
was a reproducible contamination bug). This document names the five proof shapes
that produce such verdicts and fixes the **evidence standard** for each — the bar
that turns INFEASIBLE from an opinion into a finding.

Sources (all fetched, Wikipedia primary/encyclopedic): *Comparison sort*
(decision-tree bound), *Little's law*, *Competitive analysis (online algorithm)*,
*Adversary model*, *Cache replacement policies* (Belady/MIN), *Consensus (computer
science)* (FLP, CAP). Classical results are attributed to their model, not to me.

---

## The five proof shapes (try in this order — cheapest first)

The order is deliberate: shape 1 is often a single offline script; shape 5 is a
literature reduction. Try the cheap, self-contained ones before reaching for an
adversary construction or a named theorem.

### 1. Oracle / clairvoyant ceiling

**Shape.** Build the *best physically possible* solver by handing it information no
real system can have — the future, the full input, perfect foresight — then measure
what even *it* achieves. Any real (online, causal, budgeted) policy is one of the
options available to the oracle, so the oracle's result is an **upper bound** on the
metric. If the target exceeds the oracle's ceiling, the target is unachievable by
anyone. The gap between oracle and target is the proof's headroom.

**Canonical form.** Belady's MIN cache policy evicts the item whose next use is
farthest in the future; no eviction sequence yields fewer misses on the same trace.
Run it offline on the recorded trace, read off the max hit rate — that is the
ceiling for *any* replacement policy (LRU, ARC, Hawkeye all approach but never
exceed it). Competitive analysis uses the same object: OPT, the offline optimum,
is the denominator precisely because no online algorithm can beat it.

**Plugin precedent.** r9s06 built escalating oracles — today's actual hot keys,
then perfect-foresight top-50 frequency, then an *illegal* 6x-budget cheat that
fills the whole cache — and none cleared 1.006x against a 1.25x target. The target
missed the clairvoyant ceiling by ~225x the entire effect size.

**Evidence standard (PROVEN):**
- The oracle must be **strictly more powerful** than any admissible policy on the
  exact metric — state *what unfair advantage* it has (future knowledge, larger
  budget, no causality) and argue every real policy is dominated by it.
- Run the oracle on the **real trace/instance** (or many seeds), not a model of it.
- Report the **margin**: `target − ceiling`, ideally in units of the effect size.
  A target above even a cheating oracle is decisive; a target a hair under the
  ceiling is "hard," not "impossible" — say so.
- Escalate the oracle until it stops improving (diminishing returns), so the ceiling
  is shown to be a genuine plateau, not an artifact of one weak oracle.

### 2. Conservation / arithmetic bound

**Shape.** Find a quantity that is *conserved* or that accumulates by simple
accounting, independent of any policy, and show the target violates the books.
No scheduling discipline creates capacity; it only redistributes who waits. This is
the cheapest proof when it applies — often pure arithmetic on the workload.

**Canonical form.** Queueing stability: utilization ρ = λ/μ (arrival rate over
service rate). If ρ > 1, work arrives faster than any single server can clear it,
so backlog ≥ (λ−μ)·T grows without bound regardless of order. Little's law (L = λW,
holding for *any* arrival/service distribution and *any* service order) then turns a
backlog floor into a waiting-time floor: W = L/λ. A job arriving at tick `a` on one
work-conserving worker cannot start until the `W(a) − a` ticks of already-arrived
work ahead of it drain — so `wait ≥ backlog`, for everyone, by counting alone.

**Plugin precedent.** r9s03 measured ρ ≈ 16.75 (17,135 ticks of work over a
1,023-tick arrival span on one worker), proving the backlog floor of ~16k ticks
binds every work-conserving non-preemptive policy. Reordering only moves *which*
jobs absorb the backlog; the p99 floor was tabulated across 12 seeds.

**Evidence standard (PROVEN):**
- Name the **conserved quantity** and the identity it obeys (work in ≤ work out;
  L = λW; flow conservation). State the identity's preconditions and confirm they
  hold (e.g. work-conserving, single server, stationary window).
- Derive the floor **symbolically** from the identity, then **measure** the inputs
  (λ, μ, total work, arrival span) from the real instance to plug in.
- Show the bound is **policy-independent**: it must follow from the accounting, not
  from any scheduling choice. Demonstrate across seeds that the floor holds.
- If preconditions are shaky (work *not* conserving, multiple servers, transient
  window), the bound weakens — flag it rather than overclaim.

### 3. Adversary construction

**Shape.** Quantify over all algorithms by playing an adversary that answers the
algorithm's queries *without committing to a fixed input*, always keeping alive the
largest set of inputs still consistent with its answers. Show that until N
operations have occurred, two consistent inputs demand *different* outputs — so any
algorithm halting early can be handed a consistent input on which it is wrong. The
adversary is fair: the final input matches everything the algorithm observed.

**Canonical form.** Online lower bounds: to prove no online algorithm beats ratio X,
let the adversary issue, at each step, the request worst for the algorithm's *current*
state, then show ALG's cost ≥ X·OPT. Paging with k+1 pages: always request the page
ALG lacks → ALG faults every request, while OPT (Belady) faults ≤ once per k → no
deterministic policy beats k-competitive. Ski-rental: end the season the instant the
algorithm buys → ratio ~2 is forced.

**Evidence standard (PROVEN):**
- The argument must hold against an **arbitrary** algorithm in the model — never a
  specific one. State the model (what queries/moves are admissible) explicitly.
- Give the adversary's **response rule** and prove the consistency invariant: after
  the adversary's answers, ≥2 inputs remain that force different correct outputs.
- For ratios, exhibit the concrete sequence and compute **both** ALG's forced cost
  and OPT's cost on it; the ratio is the bound.
- In an eval, the executable form is a **stress harness** that constructs the
  worst-case sequence and demonstrates every submitted/candidate policy hits it.

### 4. Information bound

**Shape.** Count the answers the algorithm must distinguish (K), bound the
information each query yields (b outcomes → log₂ b bits), and conclude it needs
≥ log_b(K) queries. Decision-tree picture: a b-ary tree with K leaves has height
≥ log_b K. This is the "you cannot learn 40 bits by asking 10 yes/no questions"
argument.

**Canonical form.** Comparison sorting: K = n! orderings, each comparison gives
1 bit, so height ≥ log₂(n!) = Ω(n log n) — an *absolute* floor (⌈log₂ n!⌉), nearly
matched by mergesort. The averaged version uses Shannon entropy: a uniform
permutation carries log₂(n!) bits, each comparison removes ≤1, so expected
comparisons ≥ log₂(n!).

**Evidence standard (PROVEN):**
- Pin down **K** (how many distinct outcomes must be told apart) and **b** (max
  outcomes per query) for the real problem — both must be justified, not assumed.
- The bound is `q ≥ log_b K`. State it, then check tightness honestly: the
  information bound is a **floor, not always the true cost** (finding the minimum
  needs n−1 comparisons though the info bound is only log₂ n). If it is loose,
  it proves *a* lower bound but may not prove *your* target is the binding one —
  combine with an adversary argument (shape 3) to close the gap.

### 5. Reduction to a known impossibility

**Shape.** Don't re-prove anything. Show your problem, if solvable, would solve a
problem already proven impossible in the matching model — the impossibility
transfers down the reduction by contrapositive. To escape, you must *weaken a model
assumption*, not search for a cleverer algorithm.

**Canonical form.** FLP: no deterministic protocol guarantees consensus in an
asynchronous system with even one crash failure (a slow process is
indistinguishable from a dead one). If your task (totally-ordered broadcast, leader
election with agreement, state-machine replication) would implement consensus, it
inherits FLP — escape only via randomization or partial synchrony. CAP: under
network partitions a system cannot be both consistent and available; if your design
must answer during partitions while keeping replicas consistent, you've reproduced
the CAP conditions and inherit the tradeoff.

**Evidence standard (PROVEN):**
- Cite the theorem and **its exact model** (FLP: async + deterministic + ≥1 crash;
  CAP: partitions possible).
- Exhibit the **reduction**: a construction showing "solution to X ⟹ solution to
  the impossible problem," and verify your system **actually matches the model's
  assumptions** (this is where most false reductions die — e.g. claiming FLP when
  the system is partially synchronous).
- Name the **escape hatch** the model forbids, so the user knows what assumption to
  relax if they want the target after all.

---

## Verdict discipline (how this plugs into the ledger)

1. **State the target as a falsifiable proposition** ("some 50-key prewarm hits
   ≥1.25x baseline"), then attack the proposition, not the search.
2. **Pick the cheapest applicable shape.** Saturated workload → conservation
   (shape 2). Cache/hit-rate/online metric → oracle (shape 1). Query/comparison
   complexity → information (shape 4) then adversary (shape 3). Distributed
   agreement/availability → reduction (shape 5).
3. **Refuter gate.** A separate refuter must try to *break the bound*, not confirm
   it: stronger oracle, illegal over-budget cheat, more seeds, a policy the bound
   supposedly excludes. r9s06 and r9s03 both ran this pass and survived; record it.
4. **Confidence calibration.** PROVEN bounds (conservation, oracle on real trace,
   clean reduction) earn ~0.97+ and the word **INFEASIBLE / IMPOSSIBLE**. A bound
   resting on shaky preconditions, a loose information floor, or a single weak
   oracle earns lower confidence and the words **"no solution found within
   <constraints>"** — explicitly *not* an impossibility claim.
5. **Always report the escape hatch.** Every impossibility is relative to a model.
   Name the assumption that, if relaxed (more workers/lower ρ; preemption; future
   knowledge; randomization; weaker consistency), would move the target back into
   reach. This converts a dead end into an actionable redesign.

**The one-line test for every verdict:** *Does this argument rule out an entire
class of solutions, or merely report that I didn't find one?* Only the former is a
proof.
