# FULL-LEVER brief: invent.md pipeline end-to-end — quota ideation (>=6/>=3 lenses),
# refute-by-probe, build, fair gates (tuned baseline/diversity/ablation/holdout),
# provability upgrade where the claim allows, LIVE provenance, claim chart (single
# table), honest rung (witness-artifact rule), disclosure, §8 self-rank.

Problem: extend the prior hedging result (iteration-10/r10s01 artifacts =
tuned baseline) with a HARD hedge budget: total extra load must never
exceed 5% in ANY 10-second window (the prior policy averaged 4% but
burst-violates windows during latency storms — measure that first!), while
keeping >=80% of its p99 improvement. Build on the same sim
(iteration-10/scenarios/r10s01_hedging/sim.py). This is a guardrailed
invention: the budget enforcement mechanism is yours; ablate it;
provenance the composition (hedging + token-budget known? adaptive
hedging art?). Full lever set.
