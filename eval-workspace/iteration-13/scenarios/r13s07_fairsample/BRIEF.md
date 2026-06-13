# FULL-LEVER brief: invent.md pipeline end-to-end — quota ideation (>=6/>=3 lenses),
# refute-by-probe, build, fair gates (tuned baseline/diversity/ablation/holdout),
# provability upgrade where the claim allows, LIVE provenance, claim chart (single
# table), honest rung (witness-artifact rule), disclosure, §8 self-rank.

Problem: per-key fair trace sampling. A stream of (key, event) pairs:
keys have wildly different volumes (zipf). Sample ~1% of events such that
EVERY key's realized sampling rate is provably close to 1% — bound the
per-key deviation tighter than Bernoulli(0.01) random sampling achieves
(binomial spread makes low-volume keys wildly over/under-sampled).
Constraints: streaming, O(1) state per active key (account it), keys
join/leave. Build the sampler, prove/check the deviation bound (provability
upgrade: the bound for your mechanism should be exhaustively checkable
per-key-count), measure vs Bernoulli on a generated zipf stream (>=3
seeds), and run the anticipation + combination tests on the mechanism —
deterministic per-key low-discrepancy/counter-based sampling vs the known
art (hash-based consistent sampling, systematic sampling, stratified).
