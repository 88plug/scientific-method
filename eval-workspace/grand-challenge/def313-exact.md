# Verbatim extraction: Ageron, Casteras, Pellerin, Portella, Rimmel, Tomasik

"New lower bounds for Schur and weak Schur numbers", arXiv:2112.03175.
PDF: https://arxiv.org/pdf/2112.03175 (pdftotext -layout). Rowley [8] = "New Lower
Bounds for Weak Schur Partitions", Integers 21 (2021) #A59 (separate paper, fetched
from math.colgate.edu/~integers, DOI 10.5281/zenodo.10816866).

NOTE ON TRANSCRIPTION: The pdftotext output renders the LaTeX `\neq` / `\notin` /
`\geq` ligatures as `6=` / `∈/` / `⩾`. Below, those are restored to `≠`, `∉`, `≥`.
`[[1,p]]` is the paper's notation for the integer interval {1,...,p}. `(N*)` = positive
integers. Everything else is verbatim.

================================================================================
0. BASE DEFINITIONS (Definitions 1.1, 1.2, 1.4)
================================================================================

Definition 1.1. A subset A of N is said to be **sum-free** if
        ∀(a, b) ∈ A², a + b ∉ A.

Definition 1.2. A subset B of N is said to be **weakly sum-free** if
        ∀(a, b) ∈ B², a ≠ b ⟹ a + b ∉ B.

  --> SUM-FREE forbids a+b∈A for ALL pairs INCLUDING a=b (so 2a∉A too).
  --> WEAKLY SUM-FREE only forbids a+b for DISTINCT a≠b. So a weak set MAY contain
      x and 2x (a "weak pair"); a strong/sum-free set may not. A sum-free set is
      also weakly sum-free.

Definition 1.4. There is a largest integer denoted by WS(n) such that [[1, WS(n)]]
can be partitioned into n weakly sum-free subsets. WS(n) is called the nth weak
Schur number.

================================================================================
1. THE PROJECTION π  (Definition 3.4) AND λ (Definition 3.9)
================================================================================

Definition 3.4. Let (a, b) ∈ (N*)² such that a > b. We define:

        π_{a,b} : x ↦ (Id + a·1_{[[0,b]]})(x mod a).

   If there is no confusion on the a and b to use, π_{a,b} is denoted by π. Notice
   that for all x ∈ Z, π(x) = x mod a and for all x ∈ [[b+1, a+b]],
   b+1 ≤ π(x) ≤ a+b.

  --> READ EXACTLY: compute r = (x mod a)  [standard non-negative residue in 0..a-1].
      The indicator 1_{[[0,b]]} is evaluated at that residue r.
      If r ∈ {0,1,...,b}  then π(x) = r + a.
      If r ∈ {b+1,...,a-1} then π(x) = r.
      (Your summary "(Id + a·1_{[0,b]})(x mod a), if residue in [0,b] add a else
      leave" is CORRECT. Note the indicator interval is [[0,b]] — it INCLUDES 0,
      i.e. residue 0 maps to a.)
      Codomain is [[b+1, a+b]]  (Proposition 3.5: π is identity on [[b+1,a+b]]).

Definition 3.9. Let (a, b) ∈ (N*)² such that a > b. Define
        λ_{a,b} : x ↦ 1 + floor((x - b - 1) / a).
   (denoted λ when unambiguous.)
   Prop 3.10:  x = a·λ(x) + π(x) - a.

================================================================================
2. DEFINITION 3.13 — b-WS-TEMPLATE  (VERBATIM)
================================================================================

Definition 3.13. Let (a, n, b) ∈ (N*)³ with a > b. Let (A₁, ..., Aₙ) a partition
of [[1, a+b]]. This partition is said to be a **b-weakly-sum-free template
(b-WS-template) with width a and n colors** when:

    ∀i ∈ [[1, n]], Aᵢ is weakly-sum-free,                                    (C1)

    ∀i ∈ [[1, n]], Aᵢ \ [[1, b]] is sum-free,                               (C2)

    For Aₙ (the special subset):
        ∀(x, y) ∈ Aₙ², x + y > b + 2a ⟹ x + y - 2a ∉ Aₙ,                  (C3)

    For the others subsets
        ∀i ∈ [[1, n-1]], ∀(x, y) ∈ Aᵢ², x + y > a + b ⟹ π(x + y) ∉ Aᵢ.    (C4)

    Number a is necessarily colored with color n. Note that the special color n is
    not necessarily the last color by order of appearance.

  --> COLOR INDEXING (load-bearing): classes are A₁,...,Aₙ  (1-indexed, n classes).
      The SPECIAL class is Aₙ — i.e. the LAST INDEX n, NOT A_0, NOT A_1. The partition
      is of [[1, a+b]] (width a, so domain has a+b elements). The integer `a` itself
      must lie in the special class Aₙ. The special class uses condition (C3)
      (subtract 2a), all OTHER classes use (C4) (apply π). "width a and n colors."
  --> In Theorem 3.17 the template is written (A₁,...,A_{n+1}) with n+1 colors and the
      special color is A_{n+1}.

Definition 3.14 / 3.15:
   WS⁺_b(n) = max{a ∈ N* / there is a b-WS-template with width a and n colors}
              (0 if none).
   WS⁺(n) = max_{b∈N*} WS⁺_b(n).

Proposition 3.16. Let n ∈ [[2, +∞]]. Then:
   (3/2)·WS(n-1) + 1 ≤ WS⁺(n) ≤ WS(n).

================================================================================
3. THEOREM 3.17 — CONSTRUCTION  (VERBATIM)
================================================================================

Theorem 3.17. Let (a, n, b) ∈ (N*)³ with a > b and (p, k) ∈ (N*)². If there are a
sum-free k-partition of [[1, p]] and a b-WS-template (A₁, ..., A_{n+1}) with width a
and n+1 colors, then there is a partition of [[1, pa + b]] into k + n weakly
sum-free subsets.

  --> So a valid b-WS-template with width a and (n+1) colors, combined with a
      SUM-FREE (= strong Schur) k-partition of [[1,p]], proves
      WS(k+n) ≥ p·a + b   when p = S(k) (the largest strong Schur k-partition).

Proof colorings (verbatim setup): f : [[1, a+b]] → [[1, n+1]] is the template coloring,
g : [[1, p]] → [[1, k]] the sum-free coloring (assumed ordered). The constraints the
template must satisfy (as encoded predicates in the proof; "the conditions x+y ≤ p
and x+y ≤ a+b are omitted"):

  sum-free:   ∀(x,y) ∈ [[b+1, a+b]]², f(x)=f(y) ⟹ f(x+y) ≠ f(x).
  weakly s-f: ∀(x,y) ∈ [[1, a+b]]², (f(x)=f(y) ∧ x≠y) ⟹ f(x+y) ≠ f(x).
  WS-extra-1: ∀(x,y) ∈ [[1, a+b]]², (f(x)=f(y) ≤ n ∧ x+y > a+b) ⟹ f(π(x+y)) ≠ f(x).
  WS-extra-2: ∀(x,y) ∈ [[1, a+b]]², (f(x)=f(y) = n+1 ∧ x+y > 2a+b) ⟹ f(x+y-2a) ≠ f(x).

The constructed coloring h of [[1, pa+b]] uses T=[[1,b]], C=π⁻¹(f⁻¹([[1,n]])),
R=π⁻¹(f⁻¹({n+1})):
   h(x) = f(x)         if x ∈ T,
   h(x) = f(π(x))      if x ∈ C,
   h(x) = n + g(λ(x))  if x ∈ R.

Theorem 3.1 (the special case, verbatim): Let (p,k),(q,n) ∈ (N*)². If there are a
weakly sum-free n-partition of [[1, q]] and a sum-free k-partition of [[1, p]] then
there is a partition of [[1, p(q + ⌈q/2⌉ + 1) + q]] into n+k weakly sum-free subsets.
(NOTE: pdftotext mangled the ⌈q/2⌉ term; the proof of Thm 3.1 sets b = q and
a = q + ⌈q/2⌉ + 1.)

================================================================================
4. THE KNOWN SMALL WS-TEMPLATES (verbatim integer sets)
================================================================================

IMPORTANT PROVENANCE: arXiv:2112.03175 does NOT print the a=4 or a=13 templates.
It states (verbatim): "Inequalities (8) and (9) were found by Rowley, they are
detailed in [8]." The sets below are taken VERBATIM from Rowley [8] = Integers 21
(2021) #A59, which gives the prototype weak Schur partitions that ARE the b-WS-
templates (their orders are exactly a+b: order 6 = 4+2, order 21 = 13+8).

--- (8) WS(n+1) ≥ 4·S(n) + 2   [a=4, b=2, 2 colors, partition of [[1,6]] ] ---
Rowley §2, "weak Schur 2-partition of order 6":
        S1 = {1, 2, 6},   S2 = [3, 5] = {3, 4, 5}.
  In the Ageron et al. b-WS-template language (a=4,b=2,n=2): the special class is
  A₂, and `a=4` must be in the special class. Rowley's translate set is
  Ti = [4i-1, 4i+1] (derived from S2), and U_{r+1} = {1,2} ∪ {4i+2 | i∈[1,m]}.
  --> Map to template colors so that 4 ∈ special class A₂. {3,4,5}=S2 contains 4,
      and S2 is the translated (Ti) family ⟹ S2 is the special class A₂={3,4,5},
      A₁={1,2,6}. (4∈A₂ as required; the single weak pair (1,2) sits in A₁.)

--- (9) WS(n+2) ≥ 13·S(n) + 8  [a=13, b=8, 3 colors, partition of [[1,21]] ] ---
Rowley §2, "weak Schur 3-partition of [1,21]":
        S1 = {1, 2, 4, 8, 21},
        S2 = {3, 5, 6, 7, 18, 19, 20},
        S3 = [9, 17] = {9, 10, 11, 12, 13, 14, 15, 16, 17}.
  Here U_{r+1} = {1,2,4,8} ∪ {13i+8 | i∈[1,m]},
       U_{r+2} = {3,5,6,7} ∪ {13i+j | i∈[1,m], j∈{5,6,7}},
       Ti = [13i-4, 13i+4]  (translates of S3).
  --> S3 = [9,17] is the translated family; 13 ∈ S3 ⟹ S3 is the special class
      (color n = A₃). Weak pairs (1,2),(2,4),(4,8) live in S1; (3,6) in S2.

--- 5-color template (this paper, §3.4) ---
arXiv:2112.03175 does NOT print a 5-color template's explicit sets. It only states
(verbatim): "The best template we could find with a computer search gives the
inequality WS(n+4) ≥ 127 S(n) + 68. It was also found with the SAT solver. In order
to reduce the search space, we only looked for WS-templates with five colors which
start with a near-optimal WS(4) partition and we assumed that the special color was
the last by order of appearance."  ⟹ a=127, b=68, 5 colors (width 127, on [[1,195]]),
sets NOT given in the paper. The PUBLISHED inequality (11) WS(n+4) ≥ 132 S(n) + 26
was instead obtained by COMBINING an S-template of width 33 with a WS-template of
width 4 (Theorem 3.21), not from a pure 5-color search.

--- The ONE WS-template actually printed in the appendix (Table 8) ---
"Table 8: 23-WS-template with width 42 and 4 colors"  [a=42, b=23, n=4, on [[1,65]]];
gives inequality (10) WS(n+3) ≥ 42 S(n) + 24:
  1: 1, 2, 4, 8, 11, 22, 25, 48, 53, (N+1)
  2: 3, 5, 6, 7, 19, 21, 23, 36, 50, 51, 52, 63, 64, 65
  3: 9, 10, 12, 13, 14, 15, 16, 17, 18, 20, 54, 55, 56, 57, 58, 59, 60, 61, 62
  4: 24, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37, 38, 39, 40, 41, 42, 43, 44,
     45, 46, 47, 49
  ("This template provides the inequality WS(n+3) ≥ 42 S(n) + 24 by placing one
   last number, here represented by (N+1), in the first subset (see Prop 3.20)."
   The `(N+1)` is the extra element added by the Prop-3.20 fine-tuning; the special
   color here is color 4, which contains a=42.)

================================================================================
5. INEQUALITIES (verbatim) AND OPTIMALITY CLAIMS
================================================================================

        WS(n+1) ≥ 4 S(n) + 2                                              (8)
        WS(n+2) ≥ 13 S(n) + 8                                             (9)
   "Inequalities (8) and (9) were found by Rowley, they are detailed in [8]."

        WS(n+3) ≥ 42 S(n) + 24                                           (10)
        WS(n+4) ≥ 132 S(n) + 26                                          (11)
   "Inequality (10), found with a SAT solver [13], cannot be improved (with this
   definition of WS-template). It uses the first sophistication explained in
   Subsection 3.3 in order to add the last number in the first color. As for
   inequality (11), it was obtained by combining an S-template with width 33 with a
   WS-template with width 4. The best template we could find with a computer search
   gives the inequality WS(n+4) ≥ 127 S(n) + 68."

OPTIMALITY / "PROVEN IMPOSSIBLE" STATUS:
  - (10) [a=42, 3-extension]: EXPLICITLY stated "cannot be improved (with this
    definition of WS-template)". The SAT search EXHAUSTED the space ⟹ a>42 for a
    1-number-added 4-color template is PROVEN IMPOSSIBLE (under this definition).
  - (8) [a=4, 1-extension, 2-color] and (9) [a=13, 2-extension, 3-color]: the paper
    makes NO optimality claim. They are simply "found by Rowley, detailed in [8]".
    NO statement that a>4 (resp. a>13) is impossible. By Def 3.15 the relevant
    optimum is WS⁺_b(2) / WS⁺_b(3); the paper does not assert these equal 4 / 13.
    ⟹ For (8) and (9): a>4 / a>13 are NOT proven impossible in this paper — OPEN
      (not claimed, not exhaustively searched in the text). Only (10)'s a=42 is
      claimed optimal-by-exhaustion. (11)'s 5-color search a=127 used restricting
      ASSUMPTIONS — "We expect that better WS-templates with n ≥ 5 colors can be
      found but one would have not to use the above assumptions." ⟹ explicitly NOT
      optimal / open for n≥5.
