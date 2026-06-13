# Certificate-Verifiable Construction Problems — Current Frontiers (2026)

Scope: combinatorial construction problems where an *improved object is instantly checkable*
(a cheap, deterministic verifier confirms validity in poly time, so search and verification
decouple). Compiled June 2026. Each section gives: current record, verifier spec, search-method
history, and attackability notes.

---

## 1. Sorting networks (minimize SIZE = comparator count)

### Records (best-known size; "optimal" = proven minimal)
Source: Bert Dobbelaere's living table (https://bertdobbelaere.github.io/sorting_networks.html),
OEIS A003075 (size) / A067782 (depth), Codish–Cruz-Filipe–Frank–Schneider-Kamp.

| n  | best-known size | proven optimal? | depth at that size |
|----|-----------------|-----------------|--------------------|
| 9  | 25  | YES — optimal size [CCFS16, arXiv:1405.5754] | 7 |
| 10 | 29  | YES — optimal size [CCFS16] (Waksman 1969 network) | 8 |
| 11 | **35** | YES — optimal size proven [Harder 2019, "sortnetopt"] | 8 |
| 12 | **39** | YES — optimal size proven [Harder 2019] | 9 |
| 13 | **45** | OPEN — lower bound 44…45 (END alg improved 46→45) | 10 |
| 14 | **51** | OPEN — lb 48…51 | 10 |
| 15 | **56** | OPEN — lb 53…56 | 10 |
| 16 | **60** | OPEN — lb 57…60 (Green's 1969 construction; still unbeaten) | 10 |
| 17 | 71  | OPEN — lb 63…71 | depth 10 proven optimal [CCEMS16] |

Key status facts:
- Optimal SIZE is proven only for n ≤ 12. The smallest open size case is **n = 13** (gap 44…45).
- Depth optimality is much further along: proven for all n ≤ 17 [Bundala–Závodný 2014; CCEMS16];
  tn ≥ 9 for all n ≥ 17.
- The size upper bounds for 13 ≤ n ≤ 16 are essentially 40–50 years old (Knuth/Green era);
  only n=13 was nudged (46→45) by the END evolutionary algorithm. **n=14,15,16 upper bounds
  have not moved in decades.**
- n=11/12 optimality (Harder 2019): the optimal networks were known for 50 years; what was new
  was the *proof of optimality* via a new search-space-reduction theorem ("An Answer to the
  Bose–Nelson Sorting Problem for 11 and 12 Channels"), with a machine-checked formal proof
  (sortnetopt repo). So 35/39 were always the records; 2019 just certified them minimal.
- van Voorhis bound: s(n) ≥ s(n−1) + ⌈log2 n⌉ — propagates lower bounds upward.

### Verifier spec (cheap — this is what makes it attackable)
**Zero-one principle** (Knuth): a comparator network sorts all inputs iff it sorts all 2^n
binary inputs. So to verify a candidate network of c comparators on n channels:
- Enumerate all 2^n 0/1 vectors, push each through the network (each comparator = min to lower
  channel, max to higher), check output is monotone nondecreasing.
- Cost: O(2^n · c). For n=16: 2^16 = 65536 vectors × ~60 comparators ≈ 4M ops — microseconds.
- An improved network (fewer comparators that still sorts) is therefore **instantly checkable**.
  Finding it is the hard part; certifying it is trivial.
- Proving a *lower bound* (no network with c−1 comparators exists) is the genuinely hard,
  non-certificate side (exhaustive/SAT over comparator-network space).

### Search-method history
- Hand construction (Knuth, Green 1969, Batcher odd–even merge / bitonic).
- Hillis 1990: co-evolution w/ "parasites" → 61-comparator n=16 (missed Green's 60).
- END algorithm (evolutionary, Juillé): improved n=13 upper bound 46→45.
- SAT-based optimality proofs: Bundala–Závodný 2014 (depth ≤16), Codish et al. 2016 (size 9,10;
  depth 17), Harder 2019 (size 11,12 with formal Coq/Isabelle-style proof).
- **SorterHunter** (Dobbelaere) — current SOTA *upper-bound* engine for n ≥ 17 (metaheuristic).
- Wang 2025 — recent depth upper bounds for n=27,28.
- AlphaEvolve / FunSearch line has NOT (publicly) targeted sorting-network size — open lane.

---

## 2. Cap sets / progression-free sets in F_3^n

A cap set = subset of F_3^n with no 3 points on a line (no x,y,z distinct with x+y+z=0).
a(n) = max cap size. Central open question: c = lim a(n)^{1/n}.
Bounds on c: **2.2202 ≤ c ≤ 2.756** (lower: Tyrrell 2023 / FunSearch refinement; upper:
Ellenberg–Gijswijt 2017 polynomial method).

### Records (exact for n ≤ 6; lower bounds beyond)
Sources: FunSearch (Nature 625, 2024, Romera-Paredes/Balog et al.), Tyrrell 2023,
arXiv:2502.06005 ("greedy capsets"), arXiv:2602.05254 ("Algebraic capsets", 2026).

| n | a(n) | status |
|---|------|--------|
| 4 | 20   | exact |
| 5 | 45   | exact |
| 6 | 112  | exact (last exact value known) |
| 7 | 236+ | lower bound (best-known cap; exact value OPEN) |
| 8 | **≥ 512** | FunSearch 2024 (beat previous 496). NOT improved since as of 2026. |
| 9 | ≥ 1082+ | lower bound (product/recursive constructions) |

Key facts:
- The headline FunSearch result: a **512-cap in n=8**, up from 496. Verified, reproduced; the
  google-deepmind/funsearch repo ships `cap_set.ipynb` with the explicit priority function and
  an assertion `cap_set_n8.shape == (512, 8)`.
- As of 2026 the 512 record for n=8 **stands** — multiple follow-ups (arXiv:2503.11061 FunSearch
  re-benchmark; 2502.06005 greedy "remove points" approach) did NOT beat it. The greedy-removal
  approach provably only yields 2^n caps (Theorem 3.2 there) — a dead end, documented.
- n=8 exact value remains OPEN (512 is only a lower bound; true a(8) unknown).
- Related "admissible sets" lower-bounded c: FunSearch raised it 2.2180 → 2.2184, then Ellenberg
  spotted a symmetry in FunSearch output → 2.2202 (the current record lower bound on c).
- 2602.05254 (2026) constructs smallest *complete* capsets O(√(3^n)) — different metric (minimal
  maximal caps), not the max-cap record, but a fresh adjacent target.

### Verifier spec (cheap)
A candidate set S ⊂ F_3^n of size m is a cap iff no 3 collinear points. Equivalent checkable form:
- For all unordered pairs (x,y), the third collinear point z = −x−y (mod 3) must NOT be in S.
- Cost: O(m^2) membership tests (hash set). For n=8, m=512 → ~131k pair checks — milliseconds.
- Alternatively O(m^3) "no three sum to zero" check; the O(m^2)+hashset form is standard.
- An improved (larger) cap is **instantly checkable**. The hard side (upper bounds on a(n)) is
  the polynomial method, not a certificate.

### Search-method history
- Algebraic/Hill caps, product constructions (a(m+n) ≥ a(m)·a(n) style lower bounds).
- Edel 2004 (496 in n=8 via tensor/product methods) — the record FunSearch beat.
- FunSearch 2024: LLM evolves a `priority(element, n)` heuristic feeding a greedy add-point
  builder; best programs run to produce the 512-cap.
- Post-2024: re-benchmarks across models (2503.11061) — note caveat that the 512 program may now
  be in LLM training data, contaminating benchmarks.

---

## 3. Golomb rulers, Costas arrays, covering codes, kissing numbers

### 3a. Optimal Golomb Rulers (OGR)
- **OGR-27 proven** (2014), **OGR-28 proven optimal Nov 2022** by distributed.net after 8.5 yr
  exhaustive search. Optimal 28-mark ruler (length 585):
  `0 3 15 41 66 95 97 106 142 152 220 221 225 242 295 330 338 354 382 388 402 415 486 504 523 546 553 585`
- **OGR-29, OGR-30+ : NOT being actively searched** — distributed.net has no plans (projected
  duration prohibitive). Best-known rulers for 29+ marks are tabulated (Shearer's list to 150
  marks) but NOT proven optimal. So OGR-29 optimality is OPEN; a better-than-known 29-mark ruler
  would be a record (none expected — known ones believed optimal but unproven).
- Verifier: a candidate set of m marks is a Golomb ruler iff all C(m,2) pairwise differences are
  distinct — O(m^2) into a hashset. Optimality (no shorter ruler) is the hard exhaustive side.
- NOTE: Golomb-ruler search is NOT really a good FunSearch-style target — the record (shortest
  *known* ruler) for each m is already conjectured optimal; the open work is *proving* optimality
  (exhaustive search / lower bounds), which a constructive search engine can't certify.

### 3b. Costas arrays
- Costas array = n×n permutation matrix, all C(n,2) displacement vectors between pairs distinct.
- All orders enumerated exhaustively up to **n=29**. Arrays known by construction (Welch,
  Lempel–Golomb) + sporadic for many n.
- **Smallest OPEN orders: n=32 and n=33** — no Costas array of these orders is currently known,
  open since 1984. Existence is the question (C(32) > 0?). Order 31 has ≥8 known.
- Exhaustive settling of n=32 estimated ~45,000 CPU-years (2011) — out of reach.
- Verifier (cheap): given a candidate permutation of order n, check the Costas property in
  **O(n^3)** (or O(n^2 log n)): all displacement vectors distinct. So "is this a Costas array?"
  is in NP with a tiny certificate. A *single found array* of order 32 or 33 would instantly
  settle a 40-year-old open existence question — **maximally attackable certificate target.**
- Search history: exhaustive backtracking (distributed, to n=29), algebraic constructions,
  recursive enumeration (efficient new approaches proposed but 32/33 unsettled). Stochastic
  search for orders 30–33 explicitly listed as Drakakis open Problem 13 — i.e. a *call for
  exactly the FunSearch/AlphaEvolve style of attack*, not yet publicly answered.

### 3c. Covering codes K_q(n,R) (football-pool problem K_3(n,1))
- K_q(n,R) = min size of a q-ary length-n code with covering radius R.
- Tables: Kéri (https://old.sztaki.hu/~keri/codes/), OEIS A004044 (football pool K_3(n,1)).
- Many upper bounds are explicit-code constructions (instantly verifiable); many open gaps remain
  between best-known lower and upper bounds.
  - K_3(n,1) ("football pool"): exact only for small n; a(6)∈[71,73], a(7)∈[156,186],
    a(8)∈[402,486] still have gaps; van Laarhoven 1989 codes are the best-known upper bounds for
    n=6,7,8 — unbeaten ~35 years.
- 2025 activity: arXiv:2504.01932 — new SDP (Lasserre/symmetry) *lower* bounds across many q,n,R.
  June 2026: arXiv:2606.09600 — Lean 4 proof-carrying certificates for K_q(n,R) upper/lower
  bounds (machine-checkable cert framework — directly relevant to "instantly checkable").
- Verifier (cheap, upper bound side): given a candidate code C ⊂ {0..q−1}^n with |C|=k, verify it
  covers iff every one of q^n words is within Hamming distance R of some codeword. Cost
  O(q^n · k · n) — exponential in n but trivial for the small n where gaps live (n ≤ ~13). A
  smaller covering code than best-known is **instantly checkable** by this sweep.
- Attack lane: the open football-pool gaps (n=6,7,8 and the K_3(n,1) frontier) are explicit
  small-code construction targets — a found code beating van Laarhoven's upper bound is a clean,
  cheaply verified record. Genetic/tabu/simulated-annealing already used; no public FunSearch hit.

### 3d. Kissing numbers / packings (certificate-checkable in small dims)
- **AlphaEvolve 2025: kissing number in dimension 11 improved 592 → 593** (new lower bound). This
  is the flagship geometric construction result.
- Verifier: a kissing config is N unit vectors (centers of outer spheres) on a sphere of radius 2
  such that pairwise angular distance ≥ 60° (i.e. all pairwise dot products ≤ 1/2 after scaling).
  Check: O(N^2) pairwise inner products. **Instantly checkable** (modulo exact-arithmetic care for
  rational/algebraic coordinates). A larger valid config = new record, cheaply verified.
- Caveat: many kissing/packing records use real coordinates; rigorous certification needs exact
  (rational or algebraic) coordinates or interval arithmetic to be a true certificate. AlphaEvolve's
  results ship with verification code (google-deepmind/alphaevolve_results notebook).
- Adjacent open dims (12, 13, 14): lower bounds still gappy vs. upper bounds → attackable.

---

## 4. FunSearch / AlphaEvolve line (2024–2026): what they actually improved

### FunSearch (Nature 625, Dec 2024; Romera-Paredes, Balog, Ellenberg, et al.)
- Cap set n=8: **496 → 512** (the canonical result). Verified, reproduced. Stands in 2026.
- Admissible sets → raised lower bound on c: 2.2180 → 2.2184; human (Ellenberg) used the
  discovered symmetry → **2.2202** (current best lower bound on cap-set growth constant).
- Online bin packing: improved heuristics (not a certificate-construction problem).

### AlphaEvolve (arXiv:2506.13131, May 2025; results repo google-deepmind/alphaevolve_results,
###   problem repo alphaevolve_repository_of_problems — 67 problems with verifiers)
Applied to 50+ open problems: matched SOTA on ~75%, **beat SOTA on ~20%**. SOTA-breaking
constructions (all ship with verification code in the Colab):
- **Kissing number, dim 11: 592 → 593** (new lower bound). [Flagship.]
- **4×4 complex matrix multiplication: 49 → 48 scalar multiplications** — first improvement over
  Strassen 1969 in this setting; improved 14 matrix-mult targets total. (Verifier: tensor
  decomposition checks out — cheap.)
- **Erdős minimum overlap problem**: new upper bound (slightly beat prior record).
- **Sum-and-difference sets**: AlphaEvolve θ=1.1584 → then HUMANS beat it: Gerbicz θ=1.173050
  (arXiv:2505.16105), then arXiv:2506.01896 θ=1.173077. (Example of AlphaEvolve result being
  rapidly leapfrogged — frontier is live.)
- **Autocorrelation inequalities**, **uncertainty principles** (Fourier): improved bounds.
- **Packing problems**: point-packing min/max distance ratio, polygon-in-polygon packings,
  **Heilbronn-triangle variants** (point sets avoiding small-area triangles).
- Problems were suggested by Terence Tao and Javier Gómez-Serrano.

### Adjacent open targets with cheap verifiers NOT yet (publicly) cracked by FunSearch/AlphaEvolve
1. **Costas arrays order 32/33** — existence open since 1984, O(n^3) verifier, explicit open call
   for stochastic search (Drakakis Problem 13). Highest-value cheap-cert target.
2. **Sorting-network size n=13–16** — upper bounds decades-old, zero-one O(2^n·c) verifier, no
   public AI attack on the SIZE objective.
3. **Cap set n=9 and exact a(7), a(8)** — O(m^2) verifier; 512 (n=8) stands but n=9 lower bound
   and the c-growth-constant lower bound remain a live, AI-tractable lane.
4. **Football-pool / covering-code gaps K_3(n,1)** for n=6,7,8 — van Laarhoven upper bounds
   unbeaten ~35 yr; small q^n sweep verifier; Lean cert framework now exists (2606.09600).
5. **Kissing number dims 12–14** — same O(N^2) verifier as dim 11 where AlphaEvolve already won.

---

## Verifier-cost summary (why these are "attackable")

| problem | improved object | verifier | cost |
|---------|-----------------|----------|------|
| sorting network | network with fewer comparators | zero-one principle, all 2^n binary inputs | O(2^n · c) |
| cap set | larger cap in F_3^n | no 3 collinear: z=−x−y ∉ S for all pairs | O(m^2) |
| Golomb ruler | shorter ruler, m marks | all pairwise diffs distinct | O(m^2) |
| Costas array | array of open order 32/33 | all displacement vectors distinct | O(n^3) |
| covering code | smaller covering set | every q^n word within R of a codeword | O(q^n·k·n) |
| kissing / packing | larger config | all pairwise dot products ≤ 1/2 (exact arith) | O(N^2) |

In every case: **finding** the object is the hard, parallelizable, search/AI-amenable side;
**verifying** it is a tiny deterministic check. That asymmetry is the defining property of this
problem class and what makes them targets for evolutionary / LLM-guided program search.
