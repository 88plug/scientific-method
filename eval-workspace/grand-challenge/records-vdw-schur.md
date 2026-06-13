# Certificate-Verifiable Combinatorial Records (van der Waerden / Schur / Ramsey / AP-free)

State of the art as of June 2026. A record here = a coloring/partition certificate that a
small program checks in seconds. "Lower bound N" almost always means: a valid certificate
of length N-1 exists (a coloring of {1,...,N-1} with no forbidden monochromatic structure),
so the number is **> N-1**, i.e. **>= N**. Watch the off-by-one (see W(2,7) note).

Sources: Wikipedia "Van der Waerden number"; Rabung-Lotts (EJC 2010); Monroe (arXiv:1603.03301,
JCMCC 2021); Ageron-Casteras-Pellerin-Portella-Rimmel-Tomasik (arXiv:2112.03175, 2021/22);
Rowley (arXiv:2107.03560 2021; arXiv:2203.13476 2022; Zenodo 10816866, 2024); Fredricksen-Sweet
(EJC 2000); Heule (S(5)=160, J.Autom.Reason. 2018); Radziszowski "Small Ramsey Numbers" DS1.16 (2021);
OEIS A045652 (Schur), A030126 (weak Schur).

---

## 1. van der Waerden numbers W(r,k)

`W(r,k)` = least N such that every r-coloring of {1,...,N} has a monochromatic k-term AP.

### Records table (bold = the named targets)

| W(r,k)    | Status      | Value / lower bound | Holder & method |
|-----------|-------------|---------------------|-----------------|
| W(2,6)    | EXACT       | 1132                | Kouril & Paul 2008 (SAT/FPGA) |
| W(3,4)    | EXACT       | **293**             | Kouril 2012 (SAT) -- so NOT an open lower-bound target |
| W(2,7)    | lower bound | **>= 3704** (i.e. > 3703) | Rabung-Lotts cyclic-zipper / Monroe; certificate length 3703 |
| W(2,8)    | lower bound | **>= 11496** (> 11495) | Rabung-Lotts / Monroe (cyclic zipper) |
| W(4,4)    | lower bound | **>= 1049** (> 1048) | Rabung-Lotts cyclic zipper |
| W(3,5)    | lower bound | >= 2174             | Rabung-Lotts |
| W(2,9)    | lower bound | >= 41266            | Rabung-Lotts |
| W(2,10)   | lower bound | >= 103475           | Rabung-Lotts |
| W(4,5)/W(4,6).. larger r,k | lower bound | Monroe holds most (distributed, primes to 950M) | Monroe 2016-21 |

Note on W(2,7): Wikipedia/literature write ">3,703". The certificate is a 2-coloring of
{1,...,3703} with no mono 7-term AP, so W(2,7) >= 3704. Both "3703" (cert length) and "3704"
(the bound) appear in the wild -- be explicit which you mean.

### Construction families (the certificate structure)

- **Rabung primitive-root coloring** (the engine behind the cyclic records): pick prime p and
  primitive root g mod p. Color nonzero residue x by (discrete log of x base g) mod r -- i.e.
  partition residues into the r cosets of the index-r subgroup of r-th-power residues. For the
  right p this coloring of {1,...,p-1} is k-AP-free. Highly **cyclic/symmetric** by construction.
- **Cyclic zipper (Herwig-Heule; Rabung-Lotts 2010 sped up the verifier)**: take a cyclic
  AP-free coloring and "zip"/fold it to extend the AP-free interval beyond p-1. Rabung-Lotts'
  contribution was reducing the AP-check of a zipped coloring from quadratic to **linear time**,
  enabling far larger searches. Monroe 2016-21 ran this distributed over ~500 volunteers,
  scanning primes up to 950M (vs 27M before), setting most current multi-color records.
- **Older small cases** (W(2,5)=178, W(2,6)=1132, W(3,4)=293): exhaustive / SAT, not cyclic.

### Most attackable here
W(4,4) >= 1049 (cert length 1048, tiny, fully checkable; cyclic constructions on a few-hundred
prime are cheap). W(2,7)/W(2,8) certs are 3703/11495 long -- still seconds to verify but a wider
heuristic search.

---

## 2. Schur numbers S(n) and weak Schur numbers WS(n)

`S(n)` = least N s.t. every n-coloring of {1,...,N} has a mono solution of x+y=z (x,y may be equal).
`WS(n)` = same but x != y required (weakly sum-free). Certificate = an explicit n-partition of
{1,...,N-1} with no mono (weak) Schur triple. Verifier: for each part, check no x+y=z (resp. x<y, x+y=z).

### Schur S(n)

| S(n) | Status | Best lower bound | Holder / method |
|------|--------|------------------|-----------------|
| S(5) | EXACT  | 160              | Heule 2017 (massively-parallel SAT, 2 PB proof) |
| S(6) | lower  | **>= 537**       | best partition (>536 Fredricksen-Sweet 2000; OEIS notes 537) |
| S(7) | lower  | **>= 1696**      | Rowley 2021 (arXiv:2107.03560), beat Fredricksen-Sweet's 1680 |
| S(8) | lower  | >= 5286          | Rowley template (arXiv:2112.03175 Table 3) |
| S(9) | lower  | **>= 17803**     | Ageron et al. 2021 (templates) -- improved 17694 |
| S(10)| lower  | **>= 60948**     | Ageron et al. 2021 (templates) -- improved 60320 |
| S(11)| lower  | >= 203828        | Ageron et al. 2021 |
| S(12)| lower  | >= 644628        | Ageron et al. 2021 |

Previous "state of the art" row (for delta reference): 1 4 13 44 160 536 1696 5286 17694 60320 201696 637856.

### Weak Schur WS(n)

| WS(n) | Status | Best lower bound | Holder / method |
|-------|--------|------------------|-----------------|
| WS(5) | EXACT  | 196              | known |
| WS(6) | lower  | **>= 646**       | Ageron et al. 2021 (dedicated weakly-sum-free 6-partition of {1,...,646}, paper Appendix C / Table 9) |
| WS(7) | lower  | **>= 2146**      | (state-of-art row; templates) |
| WS(8) | lower  | >= 6976          | Ageron et al. (WS-template, Table 4) |
| WS(9) | lower  | **>= 22536**     | Ageron et al. 2021 -- improved 22056 |
| WS(10)| lower  | **>= 71256**     | Ageron et al. 2021 -- improved 70778 |
| WS(11)| lower  | >= 243794        | Ageron et al. 2021 |
| WS(12)| lower  | >= 815314        | Ageron et al. 2021 |

Previous weak-Schur row: 2 8 23 66 196 642 2146 6976 22056 70778 241282 806786.
(Note: Ahmed-Boza-Revuelta-Sanz 2023 give related *k-color* weak Schur numbers WS_6(2)=166,
WS_7(2)=253 -- a different family, not WS(6)/WS(7).)

### Construction family: "templates" (Rowley 2020; generalized 2021)

- An **S-template** is a partition of {1,...,p} into n classes, one a distinguished "special color",
  satisfying extra constraints so it can be **composed/multiplied**: from an S-template of width q
  with n+1 colors plus a Schur (k)-partition you build a Schur partition of width ~pq with n+k colors.
  This yields recurrences S(n+j) >= a_j*S(n) + b_j. The best ones found (lingeling SAT solver):
    - S(n+1) >= 3 S(n) + 1
    - S(n+2) >= 9 S(n) + 4
    - S(n+3) >= 33 S(n) + 6
    - S(n+4) >= 111 S(n) + 43
    - **S(n+5) >= 380 S(n) + 148**  (the workhorse; gives the large-n records)
    - S(n+6) >= 1160 S(n) + 536
- Templates are sought **symmetric** (x and p+1-x get paired classes) to shrink the SAT search.
- WS-templates are the 2021 generalization to the weakly-sum-free setting; WS(6)>=646 used a
  separate direct construction (explicit 6-partition of {1,...,646}).
- Growth rate: gamma >= 380^(1/5) ~ 3.28 (Schur). Templates also feed multicolor Ramsey R_n(3).

### Most attackable here
**WS(7) and WS(8)** -- amateurs/heuristic search (Monte-Carlo: Eliahou, Bouzy, Rafilipojaona;
templates: Rowley, Ageron et al.) have repeatedly moved these; certs are short (2146 / 6976) and
trivially verified. **S(6) >= 537** is the smallest open Schur number and its 6-partition is tiny.

---

## 3. Adjacent families with recent heuristic/amateur movement

### Multicolor Ramsey R_n(3) (n colors, avoid mono triangle)
Same template machinery (Rowley arXiv:2203.13476 2022, RowleyRamsey). Certificate = an n-coloring
of K_m edges with no mono triangle; verify by scanning all triangles. R_7(3) >= 1698 (Rowley 2021).
These move in lockstep with Schur templates and are an active amateur target.

### Small two-color Ramsey R(k,l) lower bounds (cyclic/circulant graphs)
Certificate = a 2-coloring of K_n edges (a graph G on n vertices) with no K_k and complement no K_l;
verify by clique check. Per Radziszowski DS1.16 note (d): essentially **all** Table IIa/b lower
bounds, and the relevant R(3,k)/R(4,6) bounds, come from **circulant (cyclic) graphs** -- you
specify a connection set S subset of Z_n and color edge {i,j} by whether (i-j) mod n is in S.

| R(k,l) | Lower | Upper | Notes |
|--------|-------|-------|-------|
| R(5,5) | 43    | 48    | conj. = 43; lower from cyclic 42-vertex graph (Exoo) |
| R(4,6) | 36    | 41    | lower cyclic; upper 41 (since pre-2020) |
| R(3,10)| 40    | 42    | lower 40 (a claimed cyclic 41 was shown incorrect) |
| R(3,11)| 47    | 50    | cyclic |
| R(3,9) | 36    | 36    | EXACT |
| R(4,5) | 25    | 25    | EXACT (McKay-Radziszowski) |

Cyclic-graph lower bounds: most best ones up to order 102 are tabulated/compiled (HaKr1).
Steven Van Overberghe's circulant-Ramsey search code: https://github.com/Steven-VO/circulant-Ramsey
Geoffrey Exoo hosts constructions + verifiers: https://cs.indstate.edu/ge/RAMSEY/
RL-based Ramsey construction search is a 2024-26 active thread (arXiv).

### Green-Tao / AP-free (Behrend-type) density sets for small n
Largest subset of {1,...,n} with no 3-term AP (cap-set / r_3(n)) -- certs are explicit sets,
verified by checking no x+z=2y. Small-n records tracked at OEIS A065825 / A003002 and on
sequence pages; Behrend / Elkin constructions give the asymptotic density floor. Less "open record"
churn than vdW/Schur but verifier is one line.

---

## Verifier definitions (all checkable in seconds)

```
# van der Waerden: coloring is a list c[1..N]; reject if any mono k-term AP.
vdw_ok(c, k):
  N = len(c)
  for a in 1..N:
    for d in 1..(N-a)//(k-1):
      if all c[a + i*d] == c[a] for i in 0..k-1: return False
  return True   # c certifies W(r,k) > N  (so >= N+1)

# Schur: partition = color map c[1..N]; reject if mono x+y=z.
schur_ok(c):
  for x in 1..N: for y in x..N:
    z = x+y
    if z<=N and c[x]==c[y]==c[z]: return False
  return True   # certifies S(n) > N

# weak Schur: same but require x != y.
weak_schur_ok(c):  # as above but skip x==y
  ... if x!=y and z<=N and c[x]==c[y]==c[z]: return False

# Ramsey: edge-coloring of K_n (circulant: color(i,j)=f((i-j) mod n)); reject if mono K_k / K_l.
ramsey_ok: enumerate k-subsets, reject if monochromatic clique of forbidden size.
```

---

## Where records are reported / verified

- **OEIS**: A045652 (Schur), A030126 (weak Schur), A005346 etc. -- comments carry dated record claims
  (e.g. Rowley's S(7)>=1696, Mar 2023). First-stop for "is this still the record".
- **arXiv math.CO**: where new constructions land (Rowley, Ageron et al., Monroe).
- **Radziszowski "Small Ramsey Numbers" dynamic survey (DS1)**, Electronic Journal of Combinatorics
  -- the authoritative living Ramsey record (current rev DS1.16, 2021).
- **Wikipedia "Van der Waerden number"** -- maintained table, good for the diagonal.
- **GitHub**: marijnheule/vdWaerden, hmonroe/vdw, mlotts/van-der-waerden-zipper,
  Steven-VO/circulant-Ramsey, Exoo's RAMSEY page -- code + certificates for re-verification.
- **Zenodo**: Rowley deposits weak-Schur partition data (record 10816866, 2024).

---

## The 3 most attackable records (short certificates, recent heuristic movement)

1. **S(6) >= 537** -- smallest open Schur number; certificate is a 6-partition of {1,...,536}; one-line verifier.
2. **WS(7) >= 2146** (and WS(8) >= 6976) -- amateurs have repeatedly moved weak-Schur bounds with Monte-Carlo / templates; short certs.
3. **W(4,4) >= 1049** -- shortest open vdW certificate (length 1048); cyclic primitive-root + zipper search over small primes is cheap.
