# Peer review — LENS: SOUNDNESS

**Submission:** Deterministic golden-ratio low-discrepancy retry timing; claims provable
anti-clustering during outage recovery, beating random decorrelated jitter on amplification
and healthy-success.

SUMMARY: The policy assigns each request's first-retry delay `base + ((k·φ⁻¹ mod 1)·span)`
over `[31,101]s`, capped at 3 attempts, where `k` is a single in-process monotone counter.
On the r9s04 sim it reproduces exactly (peak 1.0 / post-p99 0 / healthy 1.0, seed-invariant),
and I confirmed the anti-clustering math: the three-distance theorem and equidistribution
hold for the actual parameters and survive integer-second quantization. But the headline
comparative claim ("beats random jitter") is not demonstrated at the submitted operating
point, and the determinism that is the invention's whole differentiator is a net liability
under the very failure pattern the title invokes (simultaneous multi-client failure).

LENS: SOUNDNESS — I re-derived and machine-checked all numbers. Scripts:
`check_gaps.py` (gap/clustering stats, three-distance), `check_phase.py` (thundering-herd
phase alignment), `check_quant.py` (counter-model + quantization), plus in-sim comparators.
All run against the byte-identical sim. Repro reproduces verbatim.

STRENGTHS:
- Anti-clustering claim is now EXHAUSTIVELY CHECKED IN SCOPE (upgrades E4 from
  measured+cited). Three-distance theorem holds (≤3 distinct gap lengths) for every N∈
  {70,100,1k,5k,30k}; golden max-per-second bin is within **+1** of the ideal `ceil(n/70)`
  at every N (e.g. n=30000: golden 430 vs ideal 429), while random jitter's worst-of-50-seeds
  bin is materially higher (496). The low-discrepancy advantage over random is REAL **as a
  gap statistic on a shared stream**.
- Quantization survives: float delays binned to int seconds give 70 bins [31,100], counts
  426–430, no boundary pileup. The equidistribution argument is not broken by `int(t_try)`.
- Reproduces exactly; deterministic; mechanism (base=31 jump-clear + width) is correctly
  identified for the amplification metric.

WEAKNESSES:
- **[BLOCKING] The comparative claim "beats random decorrelated jitter on amplification and
  healthy-success" is FALSE at the submitted operating point.** At the policy's own window
  `[31,101]`, plain `random.random()*span` jitter scores 1.0/0/1.0 on every seed I tried —
  identical to golden. Random's clustering only appears at the *narrower* `[30,90]` window
  (healthy 0.9958–0.9977 vs golden 0.9986), which is H4's window, NOT the shipped policy's.
  So at the artifact's actual parameters the golden sequence's advantage over random is nil;
  the win comes from window-width + base-31, both of which random jitter shares.
- **[BLOCKING] Determinism is a liability under the title's own scenario (thundering herd).**
  The anti-clustering guarantee is a property of consecutive values of ONE shared global
  counter. That models a single client process / coordinator. A real outage-recovery herd is
  many independent clients with no shared counter; the only index they share is the attempt
  number, and golden(attempt) phase-ALIGNS all of them into one bin (check_phase.py regime B1:
  30000 requests → a single 1-second bin, vs random's 483). When I remove the shared counter
  in-sim (per-request golden), healthy_success collapses to **0.9091** (fails ≥0.995), while
  random jitter needs no coordination to stay decorrelated. The mechanism's guarantee does
  NOT survive a simultaneous-failure trigger — the exact pattern the abstract claims to solve.
- [NON-BLOCKING] Scope is a single workload/parameter set; the VERDICT acknowledges this, but
  combined with the above the result is a fragile point solution, not the general policy the
  title asserts ("provably avoiding retry clustering").

QUESTIONS FOR AUTHORS:
1. At the SUBMITTED window `[31,101]`, show any seed where random uniform jitter fails a
   criterion the golden policy passes. (My `check_phase.py`/in-sim comparator finds none.)
2. In a distributed deployment (N independent clients, no shared in-process counter), what
   supplies the global counter `k`? If it's per-client attempt number, address regime B1
   (total phase alignment) in `check_phase.py`.
3. Re-state the "beats random jitter" claim bound to a specific window, or withdraw it.

SCORES: soundness **2/5** (authoritative), provenance 3/5, reproducibility 5/5,
significance 2/5

RECOMMENDATION: major-revision

REVIEWER CONFIDENCE: 0.85 — math and in-sim comparators are machine-checked against the
byte-identical sim; the deployment-regime argument is a modeling claim about how `k` is
sourced, which the artifacts never specify, so it is inference (strong, but not executed
against a real distributed harness).
