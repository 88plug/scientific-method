# Attacking open records: certificate-verifiable discovery

The deepest invention claim — a new world record on an open problem — is only
honestly reachable where the claim **certifies itself**: a witness object that,
if valid, *is* the result, checkable by anyone in seconds with no judgment and
no harness to fool. This is why every machine-discovery success (FunSearch's cap
sets, AlphaDev's sorting routines, GP "human-competitive" results) attacked
problems with an exact, cheap verifier. Pick that ground and the falsification
gate becomes the world itself.

This reference is the campaign playbook, validated end to end against the real
frontier (van der Waerden, Schur, weak-Schur, cap sets, sorting networks,
Costas arrays). It composes with invent.md — it is invent.md aimed at a record.

## 1. Is the target certificate-verifiable?

The entry test: **can a candidate answer be checked far more cheaply than it can
be found, by a pure function of the candidate alone?** A coloring with no
monochromatic progression, a permutation with distinct displacement vectors, a
point set with no collinear triple, a network sorting all 2ⁿ binary inputs.
If yes, the record is attackable on these terms; if the "answer" needs a
proof or a judgment to validate (most conjectures), this method does not apply —
say so and stop.

## 2. Target selection matrix (fill from sourced research, never memory)

Score candidates on five axes, all from live research with citations — **record
values from model memory are never trusted; training data is stale by
construction here, and these numbers move:**

| axis | the question | kill condition |
|---|---|---|
| verifier cost | seconds to check a candidate? | too expensive → not this method |
| **exhausted?** | did someone already search the whole space the method covers? | YES → ruled out (e.g. cyclic vdW records were exhausted to primes < 950M — no construction in that family can beat them) |
| amplifiable | does a small generator/seed amplify into the record via a *theorem*? | gives leverage; its absence isn't fatal |
| tool fit | does your edge (SAT, SLS, LLM-in-loop, GPU) match the documented record method? | mismatch → low odds, say so |
| record recency | did heuristic/amateur search move it recently? | recently-moved = soft, still attackable; decades-static = hard |

The honest output is often "ruled out": the cyclic/algebraic record families are
usually exhausted; the **heuristic-search families (weak Schur, template-amplified
bounds, FunSearch constructions) are where records still move** because their
spaces were never exhaustively characterized.

## 3. Verify-the-verifier — at record scale, before any search

Build the exact checker first, then **fetch the current published record
certificates and confirm your checker accepts every one and rejects mutations of
each.** A search guided by a wrong verifier finds either a false certificate or a
false impossibility — both worse than nothing. Resolve definitional ambiguities
here (weak vs strong sum-free, the "largest N" vs "the number" convention, an
off-by-one in how a bound is reported): the published cert that *accepts* defines
the operative definition. Confirm the exact value a new certificate must beat from
the primary source (OEIS dated comments, the dynamic survey, the author's repo) —
two secondary notes will disagree.

## 4. Methods are the tuned baseline — replicate before you vary

Pull the documented record-setting technique per family and run *it*, not a guess:

- **Algebraic/cyclic constructions** (vdW Rabung power-residue, the multiplicative
  trick that collapses an O(n²) check to an O(p) run-scan): cheap, often exhausted.
- **SAT** (CaDiCaL/lingeling, symmetry-breaking, cube-and-conquer for the hard
  boundary): the tool for direct extension at the SAT/UNSAT frontier. Note it gets
  exponentially harder as N approaches the true value — budget accordingly.
- **Stochastic local search** (tabu/min-conflicts/simulated-annealing over the
  certificate; the *objective function matters more than the metaheuristic* — e.g.
  prefix-length beat naive violation-count for Schur partitions). Incremental
  seeding (solve N from the solution at N−1) is near-universal.
- **Template / recurrence amplification**: a small seed certificate, glued by a
  proven inequality, becomes an arbitrarily large record. **Search the generator,
  not the giant object** — this is the FunSearch insight in classical form, and the
  single highest-leverage move. A width-a seed on a ~150-element interval can lift a
  20,000-element record by a theorem.
- **LLM-in-the-loop** (FunSearch: evolve `priority` programs, island population,
  periodic reset of low-scoring islands, a mechanical evaluator scoring every
  candidate): the one place a language model's generative reach is the lever rather
  than the bottleneck. Reserve it for construction problems where the move is "write
  a better scoring function," not "search a fixed space."

Any variation you invent is an ablation against the documented method as baseline
(invent.md §3). The acceptance verifier is the same world-checkable certificate
checker — there is no envelope to exploit here, which is exactly why this ground
is honest.

## 5. The honest outcomes (all three are real deliverables)

1. **Record broken** — a certificate file, accepted by your checker AND an
   independent from-scratch checker (witness-artifact rule), with the beaten record
   re-confirmed current and live. Then: announce on the channel the field uses
   (OEIS, the dynamic survey, arXiv), which is the true external `certified` rung —
   the one the system cannot grant itself.
2. **Frontier proven** — a provable impossibility *within a method's definition*
   ("inequality (10) cannot be improved for this template class"; "the bar sits
   above the clairvoyant ceiling") is a real result with the impossibility toolkit
   (invent.md §5), not a failure.
3. **Measured gap** — best-found vs the record, the search budget spent, the
   re-runnable apparatus. This is the durable capability: the next person with more
   compute resumes exactly where you stopped.

## Worked case study (2026-06-12 campaign, full trail in eval-workspace/grand-challenge)

A real run of this playbook, recorded because the *shape* generalizes:

- **Selection** (sourced, §2): strong Schur S(6). A sum-free 6-partition of
  [1,537] beats the 25-year-static Fredricksen-Sweet [1,536] record AND lifts
  WS(9) by theorem (Ageron WS(n+3)≥42·S(n)+24). vdW ruled out — Monroe exhausted
  the Rabung family to primes<950M. Records resolved from OEIS A045652/A030126
  dated comments (a 536-vs-537 "conflict" that was just a convention difference).
- **Verify-the-verifier** (§3): two independent checkers validated against 12
  published record certificates; all accepted, all mutations rejected.
- **The correctness gate paid for the whole apparatus.** The symmetric encoder
  returned UNSAT on the *known* [1,536] — a false negative that, untrapped, would
  have "confirmed" no record. Two bugs: a value-symmetry ladder conflicting with
  symmetry-sharing, then a genuine number-theoretic exception (537=3·179 ⇒ 179 is
  both the mirror and the sum-half of 358, so naive symmetry contradicts sum-free
  — exactly the exception Fredricksen-Sweet document). Never trust a search whose
  encoder hasn't reproduced a known certificate.
- **Outcome: measured frontier, no record** (honest outcome #3). Both documented
  methods, in-session, hit the wall at/below the boundary (CDCL: S(4)=45 UNSAT in
  11s, WS(5)=196 unresolved >10min; SLS: plateaus at 1 violation on tiny S(4)=44 —
  the documented boundary plateau Exoo solved with a prefix-length objective).
  Consistent with S(6)=536 being exact.
- **The WS-template door, then attempted (same campaign, follow-up).** The intricate
  π-closure encoding (Ageron Def 3.13) was built and **gated by reproducing both
  published templates** (width 4 and 13) — accepted by an independent O(N²) checker
  *and* re-found SAT — plus an **exhaustive `encoder ≡ checker` equivalence** on 11
  small cases (the encoder's full model set identical to the from-scratch checker's
  accepted set). That gate is what made UNSAT verdicts trustworthy. Result: two
  previously-open exact values, **WS⁺(2)=4 and WS⁺(3)=13** (the literature gave only
  the Prop-3.16 brackets [4,8] and [13,23]); each is a published-template witness
  plus UNSAT for every greater width up to the WS⁺(n)≤WS(n) ceiling, all `b`, with
  CaDiCaL and Glucose3 independently confirming the boundary DIMACS. This is an
  exact value of the auxiliary template-width sequence — **not** a new WS(n) record.
  The **5-color** door stayed shut and the gate proved it: neither plain nor
  symmetry-broken CaDiCaL re-found the *known* a=127 template in 8M conflicts, so no
  K=5 conclusion was claimed. And a fourth, hand-rolled DFS checker was caught
  emitting spurious width-14 "templates" the reference rejected — it never enforced
  the closure constraints, exactly the intricate-closure bug to fear — and was
  discarded rather than trusted. The lesson sharpens: the gate (reproduce known
  certs + exhaustive checker-equivalence) is not ceremony; here it both *enabled* a
  real positive result and *blocked* two ways to ship a false one.

The lesson that generalizes: the discipline's value here was not a trophy — it was
catching its own encoder's false negative, ruling out exhausted families before
burning compute, and refusing to ship an ungated intricate search that could
fabricate a certificate. A record campaign that ends in an honest measured frontier
with a precise next step is a success of method; a fabricated or unverified record
claim is the one unrecoverable failure.

Pre-register the prior honestly: beating a record set by a dedicated team with
optimized solvers and CPU-months is **low-probability in a single session's
compute**. The campaign is worth running anyway — the apparatus generalizes to
any certificate-verifiable target, the frontier measurement is genuine, and the
small chance is real. What is never acceptable is converting a low prior into a
forged or unverified claim; the certificate either checks against the world or it
does not exist.
