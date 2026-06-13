# Known-record certificates — sources & provenance

All files fetched live on 2026-06-12. Each certificate was independently
re-verified by a checker script (results noted per entry) before saving.
Formats are plain JSON.

---

## 1. Cap set in F_3^8 (FunSearch, 512 points)

- **File:** `capset_n8_512.json` — list of 512 ternary vectors (length 8, entries 0/1/2).
- **Source URL:** https://raw.githubusercontent.com/google-deepmind/funsearch/main/cap_set/n8_size512.txt
- **Repo:** google-deepmind/funsearch (DeepMind FunSearch, Romera-Paredes et al., *Nature* 2023).
- **Fetched:** 2026-06-12 via `curl`.
- **Verification:** 512 distinct points; **0** collinear triples in AG(8,3)
  (no a,b,c distinct with a+b+c ≡ 0 mod 3) → confirmed cap set.
- Note: original file stores each vector as a Python/JSON list per line; converted
  to a single JSON array of arrays.

## 2. Best-known sorting networks (Bert Dobbelaere, SorterHunter)

- **Files:** `sortnet_n13_45.json` (45 comparators), `sortnet_n11_35.json` (35),
  `sortnet_n12_39.json` (39). Each is a JSON list of `[a,b]` comparator pairs.
- **Source URLs (repo `bertdobbelaere/SorterHunter`, branch `master`):**
  - https://raw.githubusercontent.com/bertdobbelaere/SorterHunter/master/Networks/Sorters/Sort_13_45_10.json
  - https://raw.githubusercontent.com/bertdobbelaere/SorterHunter/master/Networks/Sorters/Sort_11_35_8.json
  - https://raw.githubusercontent.com/bertdobbelaere/SorterHunter/master/Networks/Sorters/Sort_12_39_9.json
  - (File naming is `Sort_<N>_<comparators>_<depth>.json`; these match the known
    optimal comparator counts: n=11→35, n=12→39, n=13→45.)
- **Fetched:** 2026-06-12 via `curl`.
- **Verification:** each network sorts all 2^N binary inputs (0/1 principle) → correct.
- Note: extracted the `nw` field from the source JSON (which also carries N/L/D/symmetric
  metadata) into a bare list of pairs per the requested format.

## 3. van der Waerden lower-bound certificates (Komkov, arXiv:1701.05603)

- **Files:** `vdw_<r>_<k>_<N>.json` — list of N colors (integers 0..r-1), one per
  integer 1..N. A valid r-coloring of {1..N} with no monochromatic k-term AP, so W(r,k) > N.
  - `vdw_7_3_343.json`  (W(7,3) > 343)
  - `vdw_8_3_515.json`  (W(8,3) > 515)
  - `vdw_10_3_892.json` (W(10,3) > 892)
  - `vdw_11_3_1187.json` (W(11,3) > 1187)
  - `vdw_17_3_3549.json` (W(17,3) > 3549)
  - `vdw_7_4_9980.json` (W(7,4) > 9980)
- **Source:** "New Lower Bounds for Van der Waerden Numbers", Alexey V. Komkov,
  arXiv:1701.05603 — https://arxiv.org/abs/1701.05603 (PDF: https://arxiv.org/pdf/1701.05603).
  Certificates are printed as digit strings in the PDF (base r, using 0-9 then A-G).
- **Fetched:** 2026-06-12; PDF downloaded via `curl`, text extracted with `pdftotext -layout`,
  digit strings parsed (truncated to N where the PDF re-prints a wrapped copy).
- **Verification:** every certificate uses exactly r colors, all in range, and contains
  **no** monochromatic k-term arithmetic progression (full scan) → valid.
- Additional certificates W(6,5) and W(5,6) are referenced by the paper at
  http://komkov.org/VanDerWaerden/ (not fetched).

## 4. Weak-Schur lower-bound partitions (Eliahou et al.)

- **Files:** `wschur_5_196.json` (WS(5) ≥ 196), `wschur_6_572.json` (WS(6) ≥ 572).
  Each is a list of part-labels (1..k) of length N: the partition of {1..N} into k
  weakly sum-free parts (no distinct x,y,z in one part with x+y=z).
- **Source:** S. Eliahou, J.M. Marín, M.P. Revuelta, M.I. Sanz,
  "Weak Schur numbers and the search for G.W. Walker's lost partitions",
  *Computers & Mathematics with Applications* (2012). Open-access PDF:
  https://idus.us.es/bitstream/handle/11441/136600/1-s2.0-S0898122111009722-main.pdf?sequence=1
  Explicit partitions printed in Proof of WS(5)≥196 (interval notation, e.g. `[5,7]`) and
  Theorem 3.1 (WS(6)≥572).
- **Fetched:** 2026-06-12; PDF via `curl`, text via `pdftotext -layout`, interval tokens expanded.
- **Verification:** both partitions cover {1..N} exactly once and each part is
  weakly sum-free (brute-force checked all x+y within each part) → valid.

## 5. Costas array, order 27 (James K. Beard)

- **File:** `costas_27.json` — permutation of 1..27.
- **Permutation:** `11,10,4,24,7,23,3,18,21,9,26,16,5,1,15,27,2,25,17,22,19,6,8,12,20,13,14`
- **Source:** James K. Beard, "Costas Arrays" page —
  http://jameskbeard.com/Costas_Arrays.html ("The new Costas array of order 27").
  Context: order-27 enumeration, Drakakis et al., *IEEE Trans. Inf. Theory*, Oct 2008.
- **Fetched:** 2026-06-12 via WebFetch of the page.
- **Verification:** is a permutation of 1..27 and all difference vectors (for every row
  shift h=1..26) are distinct → confirmed Costas array.

## 6. Schur S(6) ≥ 536 partition (Fredricksen & Sweet 2000)

- **File:** `schur_6_536.json` — list of 536 integers in `0..5`; index `n-1` holds
  the color (sum-free set) of integer `n` for n=1..536. 6 colors ⇒ S(6) ≥ 536
  (equivalently R_6(3) ≥ 538).
- **Source:** Harold Fredricksen & Melvin M. Sweet, "Symmetric Sum-Free Partitions
  and Lower Bounds for Schur Numbers", *Electron. J. Combin.* **7** (2000), #R32,
  doi:10.37236/1510. PDF fetched from
  https://www.combinatorics.org/ojs/index.php/eljc/article/download/v7i1r32/pdf/
  (saved `fs2000.pdf`; extracted with `pdftotext -layout` → `fs2000.txt`).
  The partition is under "Constructions" → "Partition of 536 into 6 symmetric
  sumfree sets" (p.6), Set 1..Set 6, depth D(P)=161.
- **Literal vs reconstructed:** RECONSTRUCTED from the paper's symmetric generating
  rule. The paper states it lists *"only the smallest of a symmetric pair"*, so the
  full partition is built via `color(i) = color(537 − i)` (n=536 ⇒ pair i ↔ 537−i).
  **Documented special case:** 537 = 3·179, so the elements 179 = (n+1)/3 and
  358 = 2(n+1)/3 may lie in different sets; the paper lists both explicitly (358 in
  Set 1, 179 in Set 4), so they are NOT mirror-linked. `build_536.py` does the
  reconstruction and self-verification.
- **Verification (all PASS):** all 536 integers covered exactly once with no
  listing/mirror conflict; symmetric (modulo the documented 179/358 exception);
  brute-force sum-free check over every color class found **0** monochromatic
  `x ≤ y, x+y=z` triples. Set sizes (color 0..5): [129, 86, 110, 77, 64, 70].
- The same PDF also contains the symmetric 7-set partition of [1,1680] (S(7) ≥ 1680).

---

## Failed / unreachable lookups (absence documentation)

- **http://datafin.com/costas/costas.html** — HTTP 404 (no longer hosted). Costas data
  obtained instead from jameskbeard.com (entry 5).
- **https://www.cs.cmu.edu/~mheule/vdW/** — HTTP 404. Heule's older vdW certificate index
  page was not reachable at this path; vdW certificates obtained instead from
  arXiv:1701.05603 (entry 3).
- **https://core.ac.uk/download/pdf/82165425.pdf** (Eliahou WS mirror) — returned an empty
  (0-byte) body; used the idus.us.es mirror successfully instead (entry 4).
- **https://www.combinatorics.org/.../v14i1r6/pdf/** (Herwig–Heule–van Lambalgen–van Maaren,
  EJC) — PDF retrieved but text is Flate-compressed; not parsed. Not needed: the Komkov
  arXiv paper supplied verifiable vdW certificates.
- **GitHub search for a vdW-certificate repo** — no relevant repository surfaced via
  DuckDuckGo HTML search; arXiv:1701.05603 used instead.
- A direct published Costas array for orders other than 27 was not separately fetched
  (order 27 is < 31 and satisfies the "order ≤ 31" requirement); only `costas_27.json` saved.
