# WS-template campaign — result (2026-06-12)

**Determined two previously-open exact values of the WS-template width sequence:**

> **WS⁺(2) = 4  and  WS⁺(3) = 13**

where WS⁺(n) (Ageron et al., *New lower bounds for Schur and weak Schur numbers*,
arXiv:2112.03175, Def 3.13–3.15) is the maximum width `a` of a b-WS-template with
`n` colors over all `b`. These widths drive the weak-Schur amplification theorem
(Thm 3.17): a width-`a`, `n`-color template + a sum-free `k`-partition of [[1,p]]
gives WS(k+n−1) ≥ p·a + b.

## Why this is new (literature status, sourced)

The paper's **Proposition 3.16** proves only a two-sided bracket:

  (3/2)·WS(n−1) + 1  ≤  WS⁺(n)  ≤  WS(n).

For n=2: 4 ≤ WS⁺(2) ≤ 8.  For n=3: 13 ≤ WS⁺(3) ≤ 23.
The widths 4 and 13 enter as **lower bounds** (templates found by Rowley, Integers
21 (2021) #A59); the paper makes **no maximality claim** for n=2,3 — it proves
non-improvability only for the width-42, n=4 template ("(10)… cannot be improved
*with this definition of WS-template*"). For n≥5 it explicitly expects improvement.

So WS⁺(2) and WS⁺(3) were known only as the intervals [4,8] and [13,23]. We close
them to the exact values 4 and 13 — i.e. **the lower bound of Prop 3.16 is tight
for n=2 and n=3** (it is not tight for n=4, where (3/2)·23+1 = 35.5 < 42).

*(Priority claim is "new to a direct search of the two primary sources"; the
certificate-verifiable artifact stands regardless of priority.)*

## The proof (certificate-verifiable, re-runnable in <1 s)

`certify_wstemplate.py` →
- **Witness** at the claimed max width: the published Rowley template is accepted
  by an independent O(N²) checker AND re-found SAT by the solver
  (K=2: width 4, b=2; K=3: width 13, b=8).
- **UNSAT for every greater width up to the Prop-3.16 ceiling**, every admissible
  b ∈ [1,a−1]:
  - K=2: widths **5,6,7,8** (ceiling WS(2)=8) — all UNSAT, all b. (also swept 9.)
  - K=3: widths **14…23** (ceiling WS(3)=23) — all UNSAT, all b.
  A width above the ceiling is impossible by Prop 3.16, so the search is complete.

Boundary instances exported as DIMACS (`wstemplate_certs/`), re-verified UNSAT by a
second independent engine (Glucose3) distinct from the CaDiCaL used to encode them.

## Soundness of the encoder (verify-the-verifier)

The danger in any UNSAT/impossibility claim is an over-tight encoding that rules
out valid objects. Guarded three independent ways:

1. **Exhaustive `build()` ≡ `check_template` equivalence** on 11 small cases
   (K=2 and K=3): the SAT encoder's full satisfying-assignment set is *identical*
   to the from-scratch O(N²) Def-3.13 checker's accepted set (`equiv.py`). This is
   the gold standard — it proves the encoding is neither over- nor under-constrained
   on those enumerable instances, including UNSAT ones.
2. **Two independent SAT solvers** (CaDiCaL via pysat to encode; **Glucose3**
   re-reading the DIMACS) both return UNSAT on the boundary certs.
3. **Reproduction of both externally-given published templates** (a=4, a=13): a
   misreading of Def 3.13 would almost certainly reject these — it accepts both.

## A verify-the-verifier catch worth recording

A fourth, hand-rolled backtracking checker (`bruteforce_search.py`, sharing no code
with the encoder) returned spurious "templates" at width 14 that `check_template`
*rejected* (`independent-valid=False`). Cause: its incremental pruning never
enforced the P3/P4 **closure** constraints (those bind an element to the colors of
*larger* elements placed later in DFS order). Exactly the intricate-closure bug
open-records.md predicted. It was **discarded**, not trusted — its "empty" verdicts
are meaningless because its acceptance test is incomplete. The headline claim rests
only on the three guarded props above.

## Honest negatives (the frontier, banked)

- **K=4:** the paper already proves WS⁺(4)=42 analytically; an in-session SAT
  reconfirmation was *not* obtained — the N≈60, 4-color UNSAT instances exceed a
  3M-conflict budget (a=43,b=17 ran 100 s → UNKNOWN). Not re-proven here; the
  paper's proof stands.
- **K=5:** out of session reach, and the gate proves it. Neither plain nor
  symmetry-broken CaDiCaL re-found the **known** a=127 template within 8M conflicts
  (~350 s each, both UNKNOWN). Per the authors, n≥5 needs different methods
  (Monte-Carlo / unrestricted search). With the known certificate unreachable, **no
  K=5 conclusion is claimed** — the gate correctly blocks it. WS⁺(5) stays open.

## What this is and is not

It is a small, exact, machine-verifiable determination of two entries of the WS⁺
sequence, produced end-to-end by the open-records methodology. It is **not** a new
lower-bound record for any weak Schur number WS(n) — it does not improve WS(6)≥646
or WS(7)≥2146. The prior S(6) campaign left the WS-template door "characterized but
not attempted"; this attempt is gated, executed, and closes the n=2,3 cases
positively while honestly bounding where the method runs out (n≥5).

## Re-run

```
cd eval-workspace/grand-challenge
./venv/bin/python3 wstemplate_sat.py gate     # reproduce both published templates
./venv/bin/python3 equiv.py                    # exhaustive encoder==checker (11 cases)
./venv/bin/python3 certify_wstemplate.py       # the full proof + DIMACS/DRAT certs
```
