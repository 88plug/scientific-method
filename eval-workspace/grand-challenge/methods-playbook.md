# Combinatorial Records: A Practitioner's Playbook

Documented, certificate-verifiable methods for setting **lower bounds** (good colorings/partitions) on
van der Waerden numbers, Schur / weak-Schur numbers, and related Ramsey-type problems. Every method here
is grounded in the primary source; parameter values are quoted from those sources, not guessed.

**Core asymmetry that runs through everything.** A lower bound is a *single explicit object* (a coloring /
partition). Verifying it is trivial and polynomial: enumerate the forbidden tuples (each k-AP, or each
`a+b=c`) and confirm none is monochromatic. The hard half — the matching *upper bound* / exact value —
needs a complete UNSAT proof (cube-and-conquer + DRAT/LRAT). This playbook is primarily about *building and
certifying the lower-bound object*, with the upper-bound machinery covered where it sets exact records.

Notation clash to keep straight: Rabung / Rabung–Lotts write `W(k,l)` = `W(#colors, length)`;
Herwig–Heule / Monroe write `W(r,k)` = `W(#colors, length)`. The bound formula is the same throughout:
a cyclic certificate from prime `p` gives `W ≥ (length−1)·p + 1`, doubled per zip.

---

## 1. van der Waerden lower bounds

### 1A. Rabung's power-residue / quadratic-residue cyclic construction (the workhorse)

**Source.** Rabung, *Some Progression-Free Partitions Constructed Using Folkman's Method*, Canad. Math.
Bull. 22(1):87–91, 1979, DOI 10.4153/CMB-1979-012-1. Modern restatement + Algorithm 1: Monroe,
*New Lower Bounds for van der Waerden Numbers Using Distributed Computing*, JCMCC 128, 2025
(arXiv:1603.03301), code https://github.com/hmonroe/vdw.

**Construction family — discrete-log coloring of Z_p (one dimension).**
1. Pick a prime `p` and a number of colors `r` with `p ≡ 1 (mod r)` and `p > l` (the AP length).
2. Fix a primitive root `ρ` mod `p`. Define `ν(n)` = discrete log of `n` base `ρ`.
3. **Color of `n` = `ν(n) mod r`.** This partitions `Z_p*` into the `r` cosets of the `r`-th power
   residues. Equivalently `C_i = ⋃_q (ρ^{i+qr} mod p) + 1`, `i=1..r`.
4. The full certificate over `[0,(l−1)p]` is this single Z_p pattern repeated with period `p`; color the
   multiples of `p` so the pattern isn't constant on them. Bound: `W(r,l) ≥ (l−1)·p + 1`.

**Why search collapses to a 1-D run-length scan (the multiplicative trick = the fast verifier).** The
coloring is multiplicative (`χ(nm)=χ(n)χ(m)`). Any monochromatic AP `a, a+d, …, a+(l−1)d` with `(d,p)=1`
can be multiplied by `d⁻¹ mod p`, turning it into a monochromatic **spacing-1 run** `ad⁻¹, ad⁻¹+1, …`.
So checking *all* O(n²) progressions reduces to: scan the single Z_p coloring for any monochromatic run of
`l` consecutive integers, plus a small wrap-around end condition. **Monroe's Algorithm 1 verifier**:
(a) fill `x[a]=i` by iterating `a ← a·ρ mod p, i ← i+1` (one pass = the discrete-log table); (b) set
`c_j = x[j] mod r`; (c) find the longest monochromatic run `l`; accept `W(l,r) ≥ (l−1)p+1` iff no run of
length `l` exists in `1..p−1` and Rabung's end condition holds (if `1` and `p−1` share a color then
`1..⌈(l−1)/2⌉` are not all one color, else `1..(l−1)` are not all one color). O(p) fill + O(p) scan.
A published bound is independently re-checkable from just `(p, ρ, r)`.

**Search procedure & records.** Table-scan primes, computing the run-length profile per `(p,r)`. Rabung
(1979): all primes ≤ 20,117 on an IBM 370/145; set records like `W(2,5)≥149` (p=37), `W(2,6)≥696` (p=139),
`W(3,4)≥292` (p=97), `W(4,4)≥1048` (p=349). Monroe (2025): BOINC, ~500 CPU-years, **primes exhaustively to
950 million**, r=2..10, two-machine validation per prime; current records e.g. `W(2,18)>91,079,252`,
`W(2,25)>23,003,662,489`, `W(4,13)>224,764,767,431`. **Finding: for large `l`, plain Rabung's method now
overtakes cyclic zipping** — Monroe ran the zipper code to 40M and found no zipped bound beating it.

### 1B. The cyclic "zip" construction (doubles a cyclic certificate; best for small/even r)

**Source (zip invented).** Herwig, Heule, van Lambalgen, van Maaren, *A New Method to Construct Lower
Bounds for Van der Waerden Numbers* ("Cyclic Zipper Method"), Electron. J. Combin. 14 (2007) #R6,
https://www.combinatorics.org/ojs/index.php/eljc/article/download/v14i1r6/pdf. **Fast arithmetic verifier
for zipped colorings**: Rabung & Lotts, Electron. J. Combin. 19(2) (2012) #P35, DOI 10.37236/2363, code
https://github.com/mlotts/van-der-waerden-zipper.

**Construction — zip = spread → turn → shift → merge.** Given a cyclic certificate `cW(r,l,n)`, produce
`ZW(r,l,2n)`:
1. **Spread:** place the original on the *odd* positions of a length-`2n` partition (`j ↦ 2j−1`, keep class).
2. **Turn:** relabel color `i → r+1−i` (the symmetry-induced flip; determined by the class of `p−1`).
3. **Shift:** shift the turned copy left by `n` (`j ↦ j−n mod 2n`).
4. **Merge:** odd positions from the spread copy, even positions from the shifted-turned copy.

Seed the cyclic certificate with the §1A power-residue coloring; zip up to twice (more never helps); repeat
`l−1` times +1. **Only works for even `r`.** Rabung–Lotts give the arithmetic re-interpretation (spread =
multiply Z_p* by 2; shift = cyclic shift by p) and prove the zipped coloring inherits weak multiplicativity,
so verification again collapses to checking ≤ `2p−l−1` spacing-1 runs (odd `d`: multiply by `d⁻¹ mod 2p`;
even `d`: reduce mod `p`) — linear, not quadratic. Double-zip has no shortcut verifier (exhaustive check).

**Records.** 2007 improved seven even-`r` bounds: `W(2,8)>11,495` (p=821, 1 zip), `W(2,9)>41,265` (p=2579),
`W(4,7)>393,469` (p=32,789, 1 zip), `W(6,6)>633,981` (p=31,699, 2 zips). Reproduces all known even-`r`
bounds except `W(2,3)`. Rabung–Lotts (2012), primes < 10⁷: `W(2,12)≥638,727` (p=29,033), `W(5,8)≥2,388,317`
(p=85,297, the one double-zip).

### 1C. Stochastic local search (when residue structure fails, e.g. odd r, W(2;3,t))

**Source.** Ahmed, Kullmann, Snevily, *On the van der Waerden numbers w(2;3,t)*, Discrete Appl. Math. 174
(2014) 27–51 (arXiv:1102.5433), using **UBCSAT** (https://github.com/dtompkins/ubcsat). Modern SOTA:
Chowdhury, Codel, Heule, *TaSSAT/PaSSAT*, TACAS 2024, https://par.nsf.gov/servlets/purl/10538898.

**Algorithm + parameters (which SLS wins on these structured instances).** Encode "no mono 3-AP up to t"
as SAT; run UBCSAT, **seeding each `n` incrementally from the solution at `n−1`** (walk up, don't cold-restart).
Best variant by regime: **GSAT-TABU** for easy/palindromic `t≤23`; **RoTS** (robust tabu) for the hard
middle `24≤t≤33`; **Adaptive G2WSAT** / **DDFW** for `t>33`. Noise: WalkSAT/Novelty static `p≈0.5`,
Novelty+ forced-walk `wp=0.01`; SAPS defaults `α=1.3, ρ=0.8, P_smooth=0.05`; Adaptive Novelty+ self-tunes
its novelty noise. Cutoffs (`-cutoff` = MAX-FLIPS): `5·10⁶` reaches `w(2;3,28)≥826`; `10⁸` with restarts
reaches `w(2;3,30)≥903`. Records: exact `w(2;3,19)=349` (+ a complete `tawSolver` for exact values);
PaSSAT (DDFW/LiWeT, params `(initpct,basepct,currpct)=(1,0.175,0.075)`, 10% random satisfied-clause pick,
48 h timeout on 128-core EPYC) **improved nine bounds for 31≤t≤39**.

### 1D. Streamlining + SAT for maximal cyclic certificates

Encode the `r×n` grid `x_{i,j}` with exactly-one-color + no-k-AP clauses; add **streamlining** constraints
forcing cyclic/point/reflection symmetry (e.g. `x_{i,⌈n/2⌉−j+1} ↔ x_{r+1−i,⌈n/2⌉+j}`). Solve with a
lookahead solver (**march_dl/march_eq**). Measured effect: `CPW(4,3,75)` (the maximal certificate, since
`W(4,3)=76`) found in **0.2 s** vs thousands of seconds unstreamlined. Caveat: streamlined UNSAT only
excludes *structured* colorings — it gives lower bounds, never upper bounds.

---

## 2. Schur and weak-Schur lower bounds

### 2A. Template / periodic copy-translate constructions (the high-yield family for large n)

**Sources.** Rowley, *New Lower Bounds for Weak Schur Partitions*, INTEGERS 21 (2021) #A59,
https://math.colgate.edu/~integers/v59/v59.pdf. Ageron, Casteras, Pellerin, Portella, Rimmel, Tomasik,
*New lower bounds for Schur and weak Schur numbers*, arXiv:2112.03175 / hal-04377719,
https://hal.science/hal-04377719v1/document. Eliahou, Marín, Revuelta, Sanz, Comput. Math. Appl. 63 (2012)
175–182 (recovers `WS(5)≥196`, `WS(6)≥572`). Recurrence form: Boza–Revuelta–Sanz,
`WS_k(n+1) ≥ k·WS_k(n) + (k−1)·p(k)`, `p(k)=½(k²+5k−2)`.

**Construction recipe (Rowley's `4m+2`, `r+1` theorem).** Given a *strong* Schur `r`-partition
`Q_1..Q_r` of `[1,m]`, build a *weak* Schur `(r+1)`-partition of `[1,4m+2]`:
1. **Guard class** `U_{r+1} = {1,2} ∪ {4i+2 : i∈[1,m]}` — all pairwise differences `≡0,1 (mod 4)` and `>3`,
   so it stays weakly sum-free.
2. **Translate** the seed block `S_2=[3,5]` into copies `T_i = [4i−1, 4i+1]`, `i∈[1,m]`.
3. **Glue using the strong partition:** `U_k = ⋃_{i∈Q_k} T_i`. Two blocks in the same class are safe
   *exactly because* `Q` was sum-free. Yields `r+1` weakly-sum-free classes over `[1,4m+2]`.
   (A `13m+8`/`r+2` variant uses a weak 3-partition seed `{1,2,4,8,21}/{3,5,6,7,18,19,20}/[9,17]`.)
   Records: `WS(6..10) ≥ 642 / 2146 / 6976 / 21848 / 70778`, asymptotic growth rate `> 3.27`.

**Ageron S-template generalization.** An *S-template* is a sum-free `n`-partition of `[1,p]` where every
class except a "special" `A_n` is sum-free **under wrap-around** (`x,y∈A_i, x+y>p ⇒ x+y−p ∉ A_i`), so it
tiles. Extend by Abbott–Hanson amalgamation: `WS(n+k) ≥ S(k)·(WS(n)+⌈WS(n)/2⌉+1) + WS(n)`. The small
irregular **template seed is found by a SAT solver (lingeling)**; the unbounded extension is deterministic.
Best Schur growth `S(n+5) ≥ 380·S(n)+148` (rate `⁵√380 ≈ 3.28`); new `S(9)≥17,803`, `S(12)≥644,628`.

**Verifier.** Trivial `O(m²)` triple-check on the explicit partition (printed in the papers' appendices).

### 2B. Local search over partitions (finds the small/medium records and the template seeds)

**The objective function that actually works (Exoo).** Exoo, *A Lower Bound for Schur Numbers...*, Electron.
J. Combin. 1 (1994) #R8 — source of `S(5)≥160` (later proved exact). The key finding: **do NOT minimize the
naive count of monochromatic sums.** Maximize a *prefix-length* objective:
`f1(P) = max{t : P restricted to [1,t] is sum-free}` (length of valid prefix), plus a small
top-discounted penalty `f2`, combined `f = c1·f1 + c2·f2` with **`c1/c2` randomly varied in `[2¹², 2¹⁸]`**.
Neighborhood move: **move a single integer to a different class** (good partitions are one move apart).
Found via SA/genetic search; report symmetric partitions compactly (`i` and `n+1−i` same class).

**Tabu / MCTS variants for weak Schur.** Robilliard et al. (EA 2011): multilevel **tabu search** over words
`w∈{1..k}^n`, with backtracking on stall; tabu tenure + schedule **auto-tuned by irace** → `WS(6)≥574`.
Eliahou et al. (NMC/NRPA Monte-Carlo): **level-3 Nested Monte-Carlo, 30 runs, ~624,600 samples/run**,
reward = valid-prefix length, **most-constrained-integer variable ordering**, plus streamliners (fix first
23 integers to optimal `WS(4)` prefix; ban small integers from high classes; **90% bias** to place an
integer in its neighbor's class — classes are unions of runs) → `WS(6)≥582`.

### 2C. SAT for exact Schur values — Schur Number Five (the cube-and-conquer template)

**Source.** Heule, *Schur Number Five*, AAAI 2018, arXiv:1711.08076; data https://www.cs.utexas.edu/~marijn/Schur/.

**Lower bound (easy half):** `S(5)≥160` is a single palindromic 5-coloring of `[1,160]`, found by CDCL in
**< 1 minute** after forcing small integers off the last color. (Heule then enumerated **all 2,447,113,088**
extremal colorings via sharpSAT + 1616 backdoors.)
**Upper bound (hard half) = the record:** prove `F⁵₁₆₁` UNSAT.
- **Encoding:** vars `v^i_j` (color i, number j); positive clauses (every number colored), negative length-3
  clauses `(v̄^i_a ∨ v̄^i_b ∨ v̄^i_c)` for each `a+b=c`.
- **Symmetry breaking:** full color-SBP → re-encoded formula `R⁵`, whose correctness is itself certified by a
  35 MB DRAT proof.
- **Decision heuristic (the novelty):** favor reduced *positive* clauses (not the dominant negative ones);
  `w(F,C)=(Σ_{l∈C} occ(F,l))/(2^{|C|}·|C|)`, split on max `H(F,v)=Σw(F'∖F)·Σw(F''∖F)`.
- **Cube split:** **march_cu** lookahead → **10,330,615 first-level cubes** (only **961 SAT**), `δ`-cutoff with
  final `(e,f)=(0.3,0.02)`, a cheap hardness predictor balancing ~10⁴ cubes/subproblem.
- **Conquer:** iGlucose (glucose 3.0, `-certified -var-decay=0.95`), **2400 parallel solvers** on TACC
  Lonestar 5, **~14 CPU-years, < 3 days wall-clock**.
- **Verifier:** DRAT → LRAT (drat-trim) → **formally verified ACL2 LRAT checker**. Proof **> 2 PB**
  (0.88 PB DRAT / 2.18 PB LRAT); checking ~36 CPU-years. Alt verified checker: **cake_lpr** (CakeML, verified
  to machine code; supports parallel interval checking).

### 2D. What S(5) implies for S(6)

Best known lower bound `S(6) ≥ 536` (Fredricksen–Sweet 2000, symmetric/palindromic search) up to ~544;
template machinery (§2A) gives the constructive improvements. **A full S(6) certificate (matching UNSAT) is
likely infeasible:** `m` jumps ~160→~540 while colors 5→6 (symmetry factor 6!=720), negative-clause count is
`O(k·m²)`, so the conquer proof scales orders of magnitude beyond 2 PB (exabyte-scale). Worse, the
compression lever that made S(5) tractable — `S(5)=S_mod(5)=S_pd(5)=160`, an unbroken palindromic certificate
symmetry — is **unknown for S(6)**; if the extremal S(6) certificate is non-palindromic, the symmetry-break
doesn't apply. Heule names `WS(5)` (conj. 196), not S(6), as the next realistic SAT target — and even that is
harder because the weak constraint `a<b` drops the length-2-reducible binary clauses that drive lookahead.
**For lower bounds specifically:** Ageron's `WS(6)≥646` was set by relaxing the `WS(n+1)≥4S(n)+2` construction
(fixing forced integers only for `i≤50`), encoding as SAT, and **reusing Heule's 1616 S(5,160) backdoors** —
backdoor #911 yielded a length-643 partition extending to 646.

---

## 3. Local search for coloring certificates, generally (cross-cutting)

- **Cyclic symmetry → 1-D search.** Restricting to cyclic colorings makes a certificate a single length-`n`
  string repeated with period; this is *the* lever behind every vdW record (§1A/§1B) and is added as a
  streamlining constraint in SAT (§1D). Cuts the variable count from `r·n` to `n`.
- **SLS tooling & noise.** UBCSAT catalog (27+ algorithms). Winners on structured instances: tabu families
  (GSAT-TABU, RoTS) and adaptive/weighting families (Adaptive G2WSAT, DDFW → LiWeT). Forced random-walk
  `wp=0.01` for PAC escape; incremental seeding (`n` from `n−1`) is essential.
- **Cube-and-conquer (for upper bounds / exact values).** Source: Heule, Kullmann, Wieringa, Biere, *Cube and
  Conquer*, HVC 2011, https://www.cs.utexas.edu/~marijn/publications/cube.pdf — *born from vdW work*.
  Lookahead (march family) splits into a DNF of cubes by maximizing `H(x)·H(x̄)` (new binary clauses); cutoff
  when a node hits a structural target (e.g. ~3000–3700 binary clauses, or a difficulty metric vs threshold
  `t_cc` scaled ×0.7 per refuted cube). Cubes are embarrassingly parallel (iCNF). **Boolean Pythagorean
  Triples**: `{1..7825}`, 10⁶ first-level cubes, 200 TB DRAT proof, ~4 CPU-years.
- **Verifiers.** Lower bound: scan forbidden tuples, poly-time, no solver trust. Upper bound: DRAT → LRAT
  (drat-trim) → formally verified checker (**ACL2 acl2-lrat** or **cake_lpr**, https://github.com/tanyongkiam/cake_lpr).

---

## 4. FunSearch — exact published loop parameters

**Sources.** Romera-Paredes et al., *Mathematical discoveries from program search with large language models*,
Nature 625 (2023) 468–475, https://pmc.ncbi.nlm.nih.gov/articles/PMC10794145/. Code + default config:
https://github.com/google-deepmind/funsearch (`implementation/config.py`).

**What it is.** Evolve *programs* (a `priority` function inside a fixed greedy skeleton), not the
combinatorial object directly. The LLM mutates programs; an automated evaluator scores them by *running* the
skeleton; best programs feed the next prompt. This is what beat plain search: the LLM proposes structured,
generalizable constructions rather than per-element local moves.

**Islands model (exact defaults from `config.py`).**
- `num_islands = 10` (paper: `m` separate subpopulations; "typically" tuned per problem).
- `functions_per_prompt = 2` — **best-shot prompting**: sample 1 island, then `k=2` programs from it, sort by
  score, label `priority_v0` (lowest) … `priority_v1`, append header `priority_v2` for the LLM to complete.
  (k=2 strictly beats k=1; diminishing returns beyond.)
- `reset_period = 4 h` — every 4 hours, **discard all programs from the `m/2` lowest-scoring islands**; reseed
  each from a single copy of the best program of a surviving island (ties → older). This is the migration /
  exploration mechanism.
- **Within-island sampling:** programs are clustered by *signature* (tuple of scores on each input). Sample a
  cluster by softmax on score `P_i = exp(s_i/T_cluster) / Σ exp(s_{i'}/T_cluster)`, with
  `T_cluster = T0·(1 − (n mod N)/N)`, `T0 = 0.1` (`cluster_sampling_temperature_init`),
  `N = 30,000` (`cluster_sampling_temperature_period`), `n` = #programs in island. Then sample a program
  within the cluster favoring **shorter** programs (softmax on negative length / `T_program`).

**LLM & distributed budget.**
- LLM = **Codey** (PaLM-2 code model), via API, **no fine-tuning**. (StarCoder works comparably.)
- Distributed async system: **15 samplers** (`num_samplers`, on accelerators) + **~140–150 CPU evaluators**
  (`num_evaluators`; paper says 150 = five 32-way CPU servers), communicating through the programs database.
- `samples_per_prompt = 4` (batch several continuations per prompt for throughput).
- **Evaluator budget:** sandboxed execution of the skeleton on user inputs; evaluation "can take minutes" per
  program → many cheap CPU evaluators run in parallel (the explicit reason for the CPU/accelerator split).

**Records & success rates (the honest yield).**
- **Cap set, n=8:** size-**512** cap set in Z_3^8 — beat the 20-year-old record. Found in **only 4 of 140
  experiments**. New capacity lower bound **C ≥ 2.2202** (from an n=12 admissible-set program giving
  I(12,7), size 237,984).
- **Admissible sets I(12,7):** **60% of experiments** found a full-size set.
- **Online bin packing:** discovered heuristics beating best-fit / first-fit on Weibull benchmarks.

---

## Highest-yield documented method per target family (≤10 lines)

1. **vdW W(r,l), large l / general r:** Rabung power-residue coloring of Z_p — color `n` = `ν(n) mod r`
   (`ν`=discrete log, `p≡1 mod r`); verify by O(p) run-length scan; table-scan primes (Monroe: to 950M).
2. **vdW W(r,l), small even r:** seed §1 with a cyclic power-residue certificate, then **cyclic-zip** ×1–2
   (spread→turn→shift→merge); Rabung–Lotts linear `l`-string verifier.
3. **vdW W(2;3,t) / odd-r where residues fail:** UBCSAT SLS (RoTS mid-range, Adaptive-G2WSAT/DDFW high),
   incremental seeding `n←n−1`, cutoff 10⁶–10⁸ flips.
4. **Weak-Schur WS(n), large n:** Rowley / Ageron **template = guard-class + translated seed blocks glued by
   a strong Schur partition** (`WS(r+1)≥4m+2`); seeds found by SAT (lingeling); growth rate ~3.27–3.28.
5. **Weak-Schur WS(n), medium n:** Exoo prefix-length objective `f1` (NOT naive sum-count) under SA/tabu/NMC;
   move = one integer; streamliners (fix prefix, 90% neighbor-class bias).
6. **Schur S(n) exact / upper bound:** SAT + symmetry-break + **cube-and-conquer** (march_cu → ~10⁷ cubes →
   iGlucose), verified by DRAT→LRAT→ACL2/cake_lpr. (Lower bound is a 1-minute CDCL model.)
7. **Open-problem constructions (cap set, admissible sets):** **FunSearch** — evolve `priority` programs;
   10 islands, k=2 best-shot, 4 h resets, cluster softmax `T0=0.1/N=30k`, 15 samplers + ~150 CPU evaluators.
