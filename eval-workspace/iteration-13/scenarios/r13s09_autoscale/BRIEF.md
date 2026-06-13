# FULL-LEVER brief: invent.md pipeline end-to-end — quota ideation (>=6/>=3 lenses),
# refute-by-probe, build, fair gates (tuned baseline/diversity/ablation/holdout),
# provability upgrade where the claim allows, LIVE provenance, claim chart (single
# table), honest rung (witness-artifact rule), disclosure, §8 self-rank.

Problem: beat the reactive autoscaler under 45s boot lag (sim.py): dropped
requests <=0.4x reactive AND pod-seconds <=1.15x reactive, 5 seeds. The boot
lag makes pure reaction structurally late for spikes — what mechanism
(headroom? derivative? short-horizon prediction? spike insurance?) wins the
tradeoff? Known art exists (predictive autoscaling, Kubernetes HPA behavior,
queueing headroom rules) — find/label, scope the delta.
