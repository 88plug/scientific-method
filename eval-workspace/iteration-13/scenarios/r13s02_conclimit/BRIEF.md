# FULL-LEVER brief: invent.md pipeline end-to-end — quota ideation (>=6/>=3 lenses),
# refute-by-probe, build, fair gates (tuned baseline/diversity/ablation/holdout),
# provability upgrade where the claim allows, LIVE provenance, claim chart (single
# table), honest rung (witness-artifact rule), disclosure, §8 self-rank.

Problem: adaptive concurrency limiting under a capacity shift (sim.py).
Beat every fixed limit on whole-trace goodput (>=1.25x the best fixed) while
holding windowed p99 <=250ms. Adapt from observed latencies only. Known art
exists (gradient/Vegas-style limiters) — find it live and scope your delta.
