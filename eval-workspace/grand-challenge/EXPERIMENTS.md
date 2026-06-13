# Grand-challenge invention campaign — hypothesis ledger (2026-06-12)

Goal: produce a certificate-verifiable improvement to a current world-record
lower bound (a coloring/partition/construction that, if valid, IS the result —
checkable by anyone in seconds) — the only honest route to a depth-4 claim.
Falling short of a record, the deliverable is the documented frontier campaign:
what was tried, what the measured gap to the record is, and proofs/evidence of
why, all re-runnable.

Provenance: commit <set at close> | machine wildct (24 cores, RTX 4000 Ada 20GB
+ RTX 2000E Ada 16GB, single-GPU discipline) | env python3 venv + python-sat
(CaDiCaL 1.9.5) | date 2026-06-12

## Method commitments (pre-registered, before any search)

1. **No record value from model memory is trusted.** Targets and current
   records come exclusively from the live-research agents' sourced tables
   (records-vdw-schur.md, records-networks-caps.md); every record we attack is
   re-verified against its published certificate/source before we begin.
2. **Search methods come from the literature** (methods-playbook.md): we
   replicate the documented record-setting techniques (cyclic/quadratic-residue
   constructions, SLS/tabu over partitions, SAT extension, FunSearch-style
   generator+verifier loops) before inventing variations; any variation is an
   ablation against the documented method as tuned baseline.
3. **Verifier first.** For each target, the exact certificate checker is built
   and validated against the CURRENT published record certificate (it must
   accept the known record and reject mutations of it — verify-the-verifier)
   before any search runs.
4. **The verifier is part of the claim** (invent.md §3): checkers are pure
   functions of the certificate, no envelope parameters, no shared state.
5. **Target-selection is evidence-based**: a selection matrix over (verifier
   cost, search-space structure/symmetry, record-movement recency — records
   that moved via heuristics in the last decade are attackable; SAT-closed
   numbers are not), filled only from the research agents' findings.
6. **Honesty bars**: any "new record" claim requires (a) the certificate file
   committed, (b) the independent verifier accepting it, (c) re-verification by
   a fresh agent with its own checker, (d) a live search confirming the record
   we beat is in fact current. INCONCLUSIVE/short-of-record outcomes are
   reported with the measured best-found vs record gap.

## Target selection matrix (filled ONLY from sourced research; 2026 records)

| target | current record (sourced) | verifier cost | exhausted? | my-tools fit | verdict |
|---|---|---|---|---|---|
| vdW Rabung family (W(4,4)≥1049 etc.) | locked | O(p) | **YES** — Monroe exhausted primes to 950M, r=2..10 | SAT n/a | RULED OUT (exhausted) |
| Schur S(6)≥537 | 537 | O(N²) | partial | SAT | secondary |
| **weak-Schur WS(6)≥646, WS(7)≥2146** | Ageron 2021 | O(N²) | **NO — heuristic/SAT-movable** | **SAT (CaDiCaL) = the documented record tool** | **PRIMARY** |
| sorting nets n=13–16 (45/51/56/60) | Dobbelaere | O(2ⁿ) µs | hard | weak LLM edge | deprioritized |
| Costas 32/33 | open 40y | O(n³) | heavily searched, 32! space | weak | deprioritized |
| cap set n=9 | FunSearch frontier | O(m²) | NO | **LLM-in-loop = my unique edge** | secondary (FunSearch track) |

Verify-the-verifier PASSED at record scale: all 12 published record certificates
(cap 512, sortnets 35/39/45, six vdW, WS partitions) accepted; mutations rejected.

## Hypotheses (predictions before search)

| # | Hypothesis (falsifiable) | Prediction | Probe | Verdict |
|---|---|---|---|---|
| H1 | [1,647] admits a 6-color weak-sum-free partition (⇒ WS(6)≥647, beats 646) | uncertain — Ageron searched hard; CaDiCaL settles SAT/UNSAT | ws_sat.py 6 647 | OPEN |
| H2 | [1,2147] admits a 7-color weak partition (⇒ WS(7)≥2147) | larger instance; may exceed CaDiCaL budget — measure | ws_sat.py 7 2147 | OPEN |
| H3 | an improved S-template seed (Ageron-style, SAT-found) amplifies to a new large-order WS record | the leverage play — small seed, big record | seed search | OPEN |
| H4 | a FunSearch-style LLM-generated construction reaches cap set n=9 or a weak-Schur seed | my unique apparatus; needs the island loop | funsearch track | OPEN |

**Honest prior (pre-registered):** these records were set in 2021 by a dedicated
team (lingeling SAT + template theory). Beating them in hours of local compute is
LOW-probability on raw search; the realistic edges are (a) CaDiCaL settling a
direct extension the prior team didn't publish as tight, (b) the LLM-in-loop
construction track. If no record falls, the deliverable is the re-runnable
apparatus + the measured SAT/UNSAT frontier + verified gap — which is itself the
durable plugin capability the goal names.

## Assumptions

| assumption | status | note |
|---|---|---|
| research agents return current records with sources | pending | gate: re-verify published certificates locally |
| local compute (24 cores, hours-scale) is in the regime where past records moved | pending | check against methods-playbook compute reports |

## SELECTED TARGET (evidence-locked 2026-06-12)

**Strong Schur S(6).** Record: sum-free 6-partition of **[1,536]** (Fredricksen &
Sweet 2000, EJC #R32 — unmoved 25 years; lower bound, not proven exact, OEIS
A045652/A030126 dated comments). A sum-free 6-partition of **[1,537]** is a NEW
record AND, by theorem (Ageron Prop 3.20, WS(n+3)≥42·S(n)+24), provably lifts
WS(9): 42·536+24=22536 → 42·537+24=22578. One certificate, two records.

Why this over alternatives: cleanest verifier (O(N²), self-certifying), the
cascade is a *theorem* not heuristic, and the SAT asymmetry favors us — if [1,537]
is satisfiable, CaDiCaL finds it fast; if tight, we time-box and report the
frontier. Direct weak-Schur WS(6)=647 deprioritized (head-on vs Ageron's
exhaustive SAT). vdW Rabung family RULED OUT (exhausted to primes<950M).

Capability gates PASSED: S(4)[1,44] SAT 0.12s / [1,45] UNSAT 11.3s (encoder +
boundary-UNSAT both correct). S(5)[1,160] find-gate: in progress (the SAT
direction of Heule 2017 — must reproduce before trusting the S(6) attempt).

Attack: (a) if the Fredricksen-Sweet 536-partition is fetchable → incremental
seed + extend to 537 (documented method, tractable); (b) else cold 24-core
prefix-split CaDiCaL portfolio on [1,537], time-boxed.

Honest prior: a 25-year-static record improved by plain CaDiCaL in one session is
LOW probability — most likely the true S(6)=536 (so [1,537] UNSAT, unprovable
cheaply à la Heule's 2PB S(5) proof). The shot is real and cheap to take; the
guaranteed deliverable is the re-runnable apparatus + references/open-records.md
(shipped v1.6.0) + the measured frontier.

## Surprise log (append-only — the correctness gate earned its existence)

- 2026-06-12: symmetric encoder v1 (schur_sym) gave symmetric S(6)[1,536]=UNSAT
  in 0.0s — but that partition provably exists (Fredricksen-Sweet). BUG #1: the
  value-symmetry ladder ("colours appear in order of first use") conflicts with
  symmetry rep-sharing and kills the real solution. Caught by the correctness
  gate BEFORE trusting any [1,537] UNSAT (which would have falsely "confirmed" no
  record). Disposition: dropped the ladder (schur_sym2).
- 2026-06-12: schur_sym2 (no ladder) STILL gave [1,536]=UNSAT in 0.0s. BUG #2 is
  real mathematics, not a coding slip: for N+1 divisible by 3, i=(N+1)/3 has
  mirror N+1-i = 2i = i+i, so symmetry forces colour(i)=colour(2i) while
  sum-free (i+i=2i) forbids it — instant contradiction. For 537: i=179,
  2i=358. This IS the documented Fredricksen-Sweet exception (179/358 placed in
  different sets). Fix: exempt {(N+1)/3, 2(N+1)/3} from symmetry-sharing
  (schur_sym3). The gate surfaced a subtle number-theoretic exception the
  literature handles specially — exactly what verify-the-verifier is for.
- Harness lesson (operator error, not math): early flailing with `nohup &` in
  foreground calls, broad `pkill` (self-signals the session group -> exit 144),
  and heredoc file-writes that don't commit on non-zero exit. Corrected to
  run_in_background + Write tool + absolute paths (claude-code-guide research).

## VERDICT (2026-06-12): no record this session — measured frontier reported

**Honest outcome #3 (measured gap), as pre-registered.** No certificate found;
no record broken. This is reported, not hidden — the cardinal sin would be a
fabricated or unverified claim, and there is none.

What was MEASURED (the frontier, all re-runnable):
- **CDCL (CaDiCaL 2023) hits the wall at the boundary.** S(4)[1,45] UNSAT took
  11s; WS(5)[1,196] churned >10 min unresolved; finding even the *known*
  exception-aware symmetric [1,536] did not return inside the time box. The
  S(6)[1,537] boundary is far beyond this in difficulty.
- **SLS (naive min-conflicts) plateaus at the boundary.** Seeded and from-scratch
  runs reach best=1 violation on the tiny known-SAT S(4)=44 and cannot close the
  last conflict — the documented SLS-boundary plateau (Exoo switched to a
  prefix-length objective precisely for this; a plain violation count is not the
  record-setting objective).
- Consistent with the likeliest truth that **S(6)=536 is exact** (so [1,537] is
  genuinely UNSAT, and proving it is Heule-scale, not session-scale).

Why this was the right target and the right attempt regardless: the selection was
evidence-locked (S(6) cascades to WS(9) by theorem; vdW ruled out as exhausted),
the verifiers were validated against 12 real record certificates, the correctness
gate caught two real encoder bugs (one a genuine number-theoretic exception) BEFORE
any false result could be claimed, and modern CDCL was a legitimate edge the 2000-era
record-setters lacked. The shot was real; it missed; the miss is measured.

**Durable deliverables (the goal's "do this anywhere", banked):**
- references/open-records.md (shipped v1.6.0) — the reusable certificate-verifiable
  discovery playbook.
- verifiers/ + verify_independent.py — checkers validated at record scale, two
  independent implementations, mutation-tested.
- The full method apparatus (Rabung/zip/template/SAT/SLS encoders, the methods
  playbook, the Ageron leverage analysis, the resolved exact records) — the next
  attempt, with optimized C solvers or the FunSearch-in-loop track or more compute,
  resumes exactly here. The frontier is a starting line, not a dead end.

To actually break one of these with this apparatus would need: an optimized
record-grade local-search objective (Exoo prefix-length / Rowley templates) in C,
or the LLM-in-loop FunSearch track at scale, or distributed compute (Monroe-scale)
— none session-sized. Recorded honestly.

## ADDENDUM (2026-06-12, same session): WS-template door attempted → positive result

The prior VERDICT left the 5-color WS-template as "the frontier, not attempted." It
is now attempted and gated (wstemplate_sat.py + RESULT_WSTEMPLATE.md). Outcome:

- **WS⁺(2)=4 and WS⁺(3)=13 determined exactly** (new exact values; literature gave
  only Prop-3.16 brackets [4,8] and [13,23]). Proof: published-template witness +
  UNSAT for every greater width up to the Prop-3.16 ceiling WS(n), all admissible b.
  Certificate-verifiable; encoder soundness proven by exhaustive build()≡checker
  equivalence (11 cases) + CaDiCaL/Glucose3 cross-solver UNSAT + dual published-
  template reproduction. NOT a WS(n) lower-bound record; an exact value of the
  auxiliary template-width sequence.
- **K=5 honestly blocked by the gate:** neither plain nor symmetry-broken CaDiCaL
  re-found the *known* a=127 template in 8M conflicts (~350 s) → no K=5 claim made.
  Matches the authors' note that n≥5 needs different methods.
- **Verify-the-verifier catch #3:** a hand-rolled DFS checker emitted spurious
  width-14 "templates" that the reference checker rejected (it never enforced the
  P3/P4 closure). Discarded, not trusted. The intricate-closure bug open-records.md
  predicted — caught before it could fabricate a false UNSAT confirmation.

## ADDENDUM 2 (2026-06-12): record-grade frontier SLS run — the reopening condition, tested

The falsification log's reopening condition for S(6) ("reopen only with a record-grade
SLS objective ... or distributed compute") was actually executed this session:

- **Cheap extension test:** the known Fredricksen-Sweet [1,536] partition needs >=32
  recolorings to admit 537 — every one of the 6 colors leaves 32-64 monochromatic
  x+(537-x)=537 pairs. No trivial extension exists. (Strong evidence S(6)=536 exact.)
- **frontier_sls.py:** a frontier-weighted min-conflicts SLS seeded from the 536 record.
  **Verifier gate caught a search bug:** it reported "0 conflicts" on a coloring the
  independent verifier REJECTED — a wrong incremental delta on the doubling triple
  (i,i,2i), where recoloring i changes both addends at once. On the real 537 run this
  would have been a fabricated record; caught on a known-SAT S(4)[1,44] smoke test
  instead. After the fix the engine provably solves known-SAT instances with
  verified-true output.
- **Measured plateau:** from the 536-seed (32 initial conflicts), the corrected SLS
  reached **best=27 conflicts in 60k flips (92 s)** — slow progress, far from 0. Pure
  Python is ~1.5 ms/flip at N=537 (delta is O(N) for small elements); a serious attack
  needs a C objective (as open-records.md pre-registered). So the record-grade method
  ALSO hits the wall at session scale.

Net: no S(6) record. The reopening condition was honestly tested and the wall held;
the apparatus (validated SLS engine + verifier gate that caught its own false-0) is
banked. To actually break it still needs the C-level record-grade objective or
distributed compute — not session-sized, recorded honestly.

## Falsification log (DO-NOT-RE-ATTACK)

- **"Plain CaDiCaL + naive SLS can break a static combinatorial record (S(6)/WS)
  in one session"** — FALSIFIED 2026-06-12 by measurement: both methods plateau/
  churn at or below the boundary (S(4)=45 UNSAT 11s; S(4)=44 SLS stuck at 1
  violation; [1,536] gate non-returning). The record-setting versions need
  optimized objectives/implementations/compute beyond session scale.
- **"A record-grade frontier SLS (seeded from the record) can break S(6) in one
  session"** — FALSIFIED 2026-06-12 (Addendum 2): the seeded frontier SLS plateaus
  at 27 conflicts (from 32), pure-Python ~1.5ms/flip at N=537 is too slow to probe
  the boundary; the 536 partition needs >=32 recolorings to admit 537. DO-NOT-
  RE-ATTACK in interpreted code; reopen ONLY with a C-level record-grade objective
  or distributed compute (the apparatus + measured plateau are banked to resume from).
