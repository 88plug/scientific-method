# scientific-method skill — 5-round eval benchmark (2026-06-11)

| round | arm | runs | assertions passed | rate |
|---|---|---|---|---|
| 1 | baseline | 10 | 48/75 | 64% |
| 1 | with_skill | 10 | 72/75 | 96% |
| 2 | with_skill | 10 | 56/56 | 100% |
| 3 | with_skill | 10 | 59/59 | 100% |
| 4 | with_skill | 10 | 64/64 | 100% |
| 5 | with_skill | 10 | 62/62 | 100% |

**with_skill total: 313/316 (99.1%)** — only 3 failures, all in round 1 (s05 restraint case), fixed in the round-1 revision and never recurred across 40 subsequent scenarios.

Fixes applied between rounds:
- after R1: INCONCLUSIVE as first-class deliverable + verdict-pressure failure mode; house-number confidence warning; method-weight-scales-with-evidence-cost (mini-ledger).
- after R2: removed the 0.97 anchor from the never-1.0 example; ledger size tracks uncertainty; jointly-necessary-factors headline rule.
- after R3: residual-severity sets the gap between strong verdicts (calibration spread).
- after R4/R5: none required (0 failures).

## Rounds 6-9 (2026-06-12, v1.1.0+ anticipation/structure layers)

| round | theme | runs | assertions | rate |
|---|---|---|---|---|
| 6 | new-layer validation | 10 | 63/63 | 100% |
| 7 | known solutions / prior-art | 10 | 63/63 | 100% |
| 8 | pure invention (process) | 10 | 75/75 | 100% |
| 9 | acceptance-gated invention | 10 | 70/73 | 96% |

Rounds 6-9 total: 271/274 (98.9%). Campaign grand total (9 rounds, 90 scenarios): 584/590 (99.0%).

Round-9 note: two scenarios' acceptance criteria were proven infeasible by the
runs themselves (LRU self-warming ceiling; rho≈17 saturation) — graded as passes
on the reproducible impossibility proofs; metric-forging loopholes explicitly
rejected. Fixes after 8/9: explicit prior-art partition required for every
invention pass, including solution-mode fixes.

## Rounds 10-12 (2026-06-12, v1.3.0 provable-invention core)

| round | theme | runs | assertions | rate |
|---|---|---|---|---|
| 10 | provable inventions + live provenance | 10 | 72/73 | 99% |
| 11 | provability ladders + impossibility | 10 | 80/80 | 100% |
| 12 | open-invention capstone | 10 | 76/79 | 96% |

Rounds 10-12: 228/232 (98.3%). Twelve-round campaign: 120 scenarios.
Notable: 4 briefs falsified by the runs with reproducible proofs; 1 honest
acceptance miss reported un-fudged; the one integrity failure of the program
(r10s04 fabricated witness) caught by the ladder and fixed structurally;
portfolio verdict: golden-ratio LDS retry = the sole disclosure candidate at
rung `reproduced`.

## Round 13 + formal certification (2026-06-12, v1.4.0 -> v1.5.0)

| event | result |
|---|---|
| Golden-ratio retry peer review (4 blind lenses + area chair) | **REJECT** — cross-client phase alignment inverts the thesis; win was the envelope + a shared-counter sim affordance; kill recorded DO-NOT-RE-ATTACK |
| Round 13 (full-lever + in-round certification) | 85/86 — 6/10 author-set bars proven infeasible with re-runnable proofs; zero forged passes |
| First `certified` rung | telemetry codec — certified as engineering reduction-to-practice, explicitly NOT an invention (anticipated) |

Live invention candidates after round 13: tamper-log budget-accounting result
(size-1 impossibility + Merkle-sidecar g-choice), PenaltyBoxWFQ self-backlog-
drain release predicate, ASPRiNT (one e-process driving gate + ramp). All at
reproduced/prototype with honest scoping; none claims a new principle.

Doctrine added this round: the verifier is part of the claim (§3);
reproducibility is not validity — target-regime gate before certified (§6).
Fourteen-round campaign total: 140 scenarios.
