# S(6) Lower Bound — Discrepancy Resolution (strong Schur number)

**Verdict:** The 536-vs-537 conflict is NOT a real disagreement. Both notes are right; they
quote two OEIS sequences that use opposite conventions differing by exactly 1 (A045652(n) = A030126(n) − 1).
The current strong-Schur S(6) record is **one fact: [1,536] is partitionable into 6 sum-free sets; 537 is not (yet) shown to be).**

---

## 1. OEIS A045652 — "Schur's numbers (version 2)" = *largest* N partitionable

Source: https://oeis.org/A045652/internal (revision #56, dated **Feb 16 2025**).

- DATA: `1, 4, 13, 44, 160` (these are S(1..5); S(5)=160 proven, "a(5) from Marijn Heule, Nov 26 2017").
- NAME: *"Largest number such that there is an n-coloring of the integers 1, ..., a(n) such that each color is sum-free."* — Charles R Greathouse IV, Jun 11 2013.
- LOWER-BOUND COMMENT (verbatim):
  > "The best known lower bounds for the next terms are due to Fredricksen and Sweet (see links): **a(6) >= 536** and a(7) >= 1680." — *Dmitry Kamenetsky, Oct 23 2019*
  > "A partition showing that **a(7) >= 1696** was demonstrated in 2021, along with some recurrence relationships for lower bounds on a(n)." — *Fred Rowley, Mar 01 2023* (Rowley, arXiv:2107.03560)

So in version-2 (largest-partitionable) convention: **S(6) ≥ 536**, and this is a **lower bound, NOT proven exact** (keyword `more,hard`; only S(1..5) are exact, S(5)=160 by Heule 2017).

## 2. OEIS A030126 — "Schur's numbers (version 1)" = *smallest* N NOT partitionable

Source: https://oeis.org/A030126/internal (revision #70, dated **Dec 01 2025**).

- DATA: `2, 5, 14, 45, 161`. NAME: *"Smallest number such that for any n-coloring of 1..a(n) no color is sum-free."*
- LOWER-BOUND COMMENT (verbatim):
  > "**a(6) >= 537**, a(7) >= 1681 (see Ahmed et al. at p. 2)." — *Stefano Spezia, Aug 25 2023*
- Formula (A045652): `a(n) = A030126(n) - 1`.

**→ 537 = 536 + 1. The "537" note is the version-1 (smallest-not-partitionable) value; the "536" note is the
version-2 (largest-partitionable) value. They are the SAME record. Neither is proven exact — both are lower bounds.**

## 3. Convention disambiguation (so S(6) is unambiguous)

Wikipedia "Schur number" uses **version 1** (A030126): S(n) = 2, 5, 14, 45, 161; defines S(c) as the *smallest* N
where every c-partition has a monochromatic x+y=z. Under that convention the record statement is "**[1,537] is the threshold; [1,536] IS 6-partitionable sum-free.**"
Ageron et al. (arXiv:2112.03175) use **version 2**: "the greatest p ... is the nth Schur number," so they write **S(6) = 536**.

**The record to beat for a NEW strong sum-free 6-partition certificate: a sum-free partition of [1, N] with N ≥ 537** (i.e., beat the current 536-length partition; equivalently push A030126(6) past 537).
Current best 536-partition: Fredricksen & Sweet (2000), Electron. J. Combin. 7, doi:10.37236/1510.

## 4. Certificate availability

The S(5)=160 certificate (Exoo/Heule) is printed in full in both OEIS entries (sets A–E). For **S(6) ≥ 536** the
explicit 6-partition is in **Fredricksen & Sweet, "Symmetric Sum-Free Partitions and Lower Bounds for Schur Numbers,"
Electron. J. Combin. 7 (2000)** — https://doi.org/10.37236/1510 (open access; partition tabulated in the paper).
No 536-partition is inlined in the OEIS DATA/COMMENTS; the EJC paper is the downloadable source.

## 5. Recurrence chain — CONFIRMED as a THEOREM (not heuristic)

Source: Ageron, Casteras, Pellerin, Portella, Rimmel, Tomasik, *"New lower bounds for Schur and weak Schur
numbers,"* arXiv:2112.03175 (Apr 4 2022) / HAL hal-04377719. Uses version-2 convention (S(6)=536, S(7)=1696).

Three template inequalities (all proven by explicit construction; verbatim §3.4 / Table 4):
```
WS(n+1) ≥  4·S(n) +  2   (8)  [Rowley]
WS(n+2) ≥ 13·S(n) +  8   (9)  [Rowley]
WS(n+3) ≥ 42·S(n) + 24  (10)  [Ageron et al.; "found with a SAT solver, cannot be improved (...)"]
```

Plugging current strong-Schur records into inequality (10):
- **WS(9) ≥ 42·S(6)+24 = 42·536+24 = 22536.** ✓ Matches the published WS(9) record exactly; it IS the highlighted best in Table 4 (beats 21146 and 22056).
- **WS(10) ≥ 42·S(7)+24 = 42·1696+24 = 71256.** ✓ Matches the published WS(10) record exactly (beats 71214 and 68726). Uses S(7) ≥ 1696 (Rowley 2021), not the older 1680.

These are **theorems** (each inequality is a construction: a template that builds the weakly-sum-free partition;
inequality (10) is the 6-color WS-template in Appendix B placing one extra element in the first subset, Prop. 3.20).
**Therefore the cascade is provable, not heuristic:** if S(6) improves from 536 → 537, then
WS(9) ≥ 42·537+24 = **22578** — a guaranteed +42 increase. Likewise any +1 in S(7) lifts WS(10) by 42.

---

## Bottom line (≤8 lines)
- Current strong-Schur record: **S(6) ≥ 536** (version-2 = largest partitionable) ≡ **537 is the version-1 threshold** — same fact, the "536 vs 537" conflict is a convention difference (A045652 = A030126 − 1).
- Status: **LOWER BOUND, not proven exact.** Source: Fredricksen & Sweet 2000 (EJC, doi:10.37236/1510). Only S(1..5) are exact (S(5)=160, Heule 2017).
- **A new strong certificate must exhibit a sum-free 6-partition of [1, N] with N ≥ 537** (beat the 536-length partition).
- Cascade is a **THEOREM**: WS(9) ≥ 42·S(6)+24 = 22536 and WS(10) ≥ 42·S(7)+24 (S(7)=1696) = 71256, both verbatim in Ageron et al. arXiv:2112.03175 ineq (10), Table 4.
- ⇒ Improving S(6) by 1 provably raises WS(9) by exactly 42 (→ 22578). The recurrence is constructive (SAT-verified template), not heuristic.
