# Weak-Schur record seeds & templates — exact extraction

Sources (verbatim, no paraphrase of numbers):
- Rowley, "New Lower Bounds for Weak Schur Partitions", INTEGERS 21 (2021) #A59 — http://math.colgate.edu/~integers/v59/v59.pdf
- Ageron, Casteras, Pellerin, Portella, Rimmel, Tomasik, "New lower bounds for Schur and weak Schur numbers", arXiv:2112.03175 (v?, dated April 4 2022) — https://arxiv.org/abs/2112.03175

**IMPORTANT correction to the brief:** WS(7)≥2146, WS(8)≥6976, WS(9)≥21848, WS(10)≥70778 are **Rowley's** values, not Ageron's. Ageron's *improved* records are WS(6)≥646, WS(9)≥22536, WS(10)≥71256. Ageron did NOT beat Rowley on WS(7) or WS(8) (their best for those, 6786/6976, only ties/loses). Current per-n records (max of both papers): WS(6)=646, WS(7)=2146, WS(8)=6976, WS(9)=22536, WS(10)=71256.

---

## (1) Exact recurrence / theorem statements with all constants

### Rowley (INTEGERS A59), Theorem 1 (Construction Theorem)
"If there is a strong Schur partition of the integers [1, m] into r subsets, then there is a weak Schur partition of [1, **4m+2**] into **r+1** subsets; and a weak Schur partition of [1, **13m+8**] into **r+2** subsets."
- These are the inequalities WS(r+1) ≥ 4·S(r)+2 and WS(r+2) ≥ 13·S(r)+8.

### Ageron (arXiv:2112.03175) — WS-template inequalities (Section 3.4)
- (8)  WS(n+1) ≥ **4 S(n) + 2**      [Rowley]
- (9)  WS(n+2) ≥ **13 S(n) + 8**     [Rowley]
- (10) WS(n+3) ≥ **42 S(n) + 24**    [NEW — SAT solver; "cannot be improved with this definition of WS-template"]
- (11) WS(n+4) ≥ **132 S(n) + 26**   [NEW — S-template width 33 ∘ WS-template width 4; best *pure* WS-template search only gave 127 S(n)+68]

WS-template construction core (Thm 3.17): a sum-free k-partition of [1,p] plus a b-WS-template of width a and n+1 colors → a weak partition of [1, **p·a + b**] into k+n colors. The b-WS-template definition (Def 3.13) on a partition of [1, a+b]: every Aᵢ weakly sum-free; every Aᵢ\[1,b] sum-free; special color Aₙ: x+y>b+2a ⇒ x+y−2a∉Aₙ; others: x+y>a+b ⇒ π(x+y)∉Aᵢ, where π(x)=(Id+a·1_{[0,b]})(x mod a).

Record values come from plugging the best strong Schur numbers S(n) (Heule's S(5)=160, Rowley's S(6)=536, S(7)=1696, S(8)=5286…) into (10)/(9):
- WS(9) ≥ 42·S(6)+24 = 42·536+24 = **22536**
- WS(10) ≥ 42·S(7)+24 = 42·1696+24 = **71256**
- WS(8) ≥ 13·S(6)+8 = 13·536+8 = **6976** (record held by (9), not (10))
- WS(7) ≥ 13·S(5)+8 = 13·160+8 = **2088** via (9); Rowley's 2146 is the actual record (= 13·S(5)+... no — Rowley's 2146 comes from his 13m+8 with a better strong seed / direct construction; (8) gives 4·S(6)+2=2146 = **4·536+2**, i.e. WS(7) ≥ 4 S(6)+2 = 2146).

So per record: WS(6)=646 (special, see §3), WS(7)=4·S(6)+2=**2146**, WS(8)=13·S(6)+8=**6976**, WS(9)=42·S(6)+24=**22536**, WS(10)=42·S(7)+24=**71256**.

---

## (2) Literal seed partitions (integer sets, verbatim)

### Rowley 4m+2 seed (the (8)/WS(n+1) construction) — weak Schur 2-partition of [1,6]:
- S1 = {1, 2, 6},  S2 = [3,5] = {3,4,5}
- Then U_{r+1} = {1,2} ∪ {4i+2 | i∈[1,m]};  T_i = [4i−1, 4i+1] for i∈[1,m].

### Rowley 13m+8 seed (the (9)/WS(n+2) construction) — weak Schur 3-partition of [1,21] (CONFIRMED, exact):
- S1 = {1, 2, 4, 8, 21}
- S2 = {3, 5, 6, 7, 18, 19, 20}
- S3 = [9,17] = {9,10,11,12,13,14,15,16,17}
- Then U_{r+1} = {1,2,4,8} ∪ {13i+8 | i∈[1,m]};  U_{r+2} = {3,5,6,7} ∪ {13i+j | i∈[1,m], j∈{5,6,7}};  T_i = [13i−4, 13i+4] for i∈[1,m].

NOTE on the brief's "r=5,6,7 seeds": Rowley's paper uses ONE fixed seed per construction (the [1,6] and [1,21] partitions above). The r-dependence comes entirely from which strong S(r)-partition is plugged in via Q_k; there is no separate stored seed per r. The full per-r values are Rowley Table 1: WS = [2,8,23,66,196,642,2146,6976,21848,70778] for r=1..10; strong S = [1,4,13,44,160,536,1680,5286,17694,60320].

### Ageron (10) seed — 23-WS-template, width 42, 4 colors (Table 8), gives WS(n+3) ≥ 42 S(n)+24:
- A1 = {1, 2, 4, 8, 11, 22, 25, 48, 53, (N+1)}   ← (N+1) = the one extra number added in first subset via Prop 3.20
- A2 = {3, 5, 6, 7, 19, 21, 23, 36, 50, 51, 52, 63, 64, 65}
- A3 = {9, 10, 12, 13, 14, 15, 16, 17, 18, 20, 54, 55, 56, 57, 58, 59, 60, 61, 62}
- A4 = {24, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 49}
- (b=23, a=42, so partition of [1, a+b]=[1,65].)

### Supporting S-templates (Ageron Appendix A): width-33/4col (Table 5), width-111/5col (Table 6), width-380/6col (Table 7) — these feed the Schur side. Width-33 example:
- 1: {1,6,9,13,16,20,24,27,31}  2: {2,5,14,15,25,26}  3: {3,4,10,11,12,28,29,30}  4: {7,8,17,18,19,21,22,23,32,33}

---

## (3) What an "improved seed" must satisfy + smallest SAT instance per record

A new WS-template improving inequality (k) is a b-WS-template of width a, n+1 colors, partitioning [1, a+b], satisfying Def 3.13, whose induced inequality WS(n+k) ≥ a·S(n) + b beats the current (a,b) lexicographically. Concretely:

- **Beat WS(9)=22536 and WS(10)=71256 (both from (10), 42 S(n)+24):** Inequality (10) is PROVEN OPTIMAL for the WS-template definition ("cannot be improved with this definition of WS-template"). To beat it you must improve the n+3 relation — i.e. find a 3-extension construction with multiplier a>42, OR a better S(6)/S(7) strong seed. Smallest SAT seed-search: a b-WS-template with **4 colors** (n+1=4, k=3) and width a≥43, i.e. searching partitions of an interval [1, a+b] with a≥43; the current optimum sits at a=42,b=23 (interval [1,65]). Since (10) is optimal under the current definition, the productive search is the *relaxed* WS-template (Prop 3.20-style, weaken last-row/first-row constraints) over an interval of size ≈ a+b ≈ 70–130.

- **Beat WS(8)=6976 (from (9), 13 S(n)+8):** find a 2-extension WS-template (n+1=3 colors, k=2) with a>13 on interval [1, a+b]; current seed is the [1,21] 3-partition (a=13,b=8 ⇒ interval [1,21]). Smallest instance: SAT over 3-color partitions of [1, ~22…30].

- **Beat WS(7)=2146 (from (8), 4 S(n)+2):** find a 1-extension WS-template (n+1=2 colors, k=1) with a>4 on [1,a+b]; current seed [1,6] 2-partition (a=4,b=2). This is the **smallest** seed-search instance — 2-color partitions of a tiny interval.

- **Beat WS(6)=646:** not template-derived (see §4); improving it means the special relaxed search of §4.

**Smallest seed-search instance that would set a NEW WS record:** the n+4 relation (11), WS(n+4) ≥ 132 S(n)+26, is the *weakest-understood*: the best *pure* 5-color WS-template found was only 127 S(n)+68, and the authors explicitly say "better WS-templates with n≥5 colors can be found." So a 5-color b-WS-template with width a>132 — i.e. a SAT search over **5-color** weakly-sum-free partitions of an interval [1, a+b] starting near a near-optimal WS(4)=66 partition (a≈132, b small ⇒ interval ≈ [1,150]) — would directly lift WS(n+4) and hence WS(9)=132·S(5)+...→ improves the n+4 lower bounds in Table 4. Any a≥133 here beats the current record chain.

---

## (4) Downloadable FULL certificates

- **WS(6)≥646 full 6-partition of [1,646]: YES, printed in full** in Ageron Appendix C, Table 9 (arXiv:2112.03175 PDF, page 20). The complete six integer subsets are reproduced verbatim in this file's source PDF; no external download needed — it is in the paper itself. (Built from Heule's 1616 backdoors; only the 911th backdoor yielded length 646; cannot reach 647.)
- WS(9)/WS(10) certificates are NOT printed in full — they are *implicit* via Thm 3.17 applied to the width-42 WS-template (Table 8) ∘ the strong S(6)/S(7) partitions (the latter from Rowley [11] "An improved lower bound for S(7)…" / Heule "Schur number five" [9]). No standalone certificate file linked.
- Rowley's WS records: also implicit (construction + strong seeds from arXiv:1912.01164); no certificate file.
