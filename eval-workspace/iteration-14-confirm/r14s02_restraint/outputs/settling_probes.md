# Settling probes (none require taking prod down / bisecting)

The constraint is "cannot take prod down to bisect." Every probe below is
read-only or canary-only and respects that constraint.

## P1 — Recover a pre-May-14 baseline (kills or confirms the censoring problem)
The whole verdict hinges on whether 502s existed BEFORE May 14. Sources that may
hold pre-update signal even though the sampling tier didn't retain backend logs:
  - LB access/metrics counters: `rate(lb_5xx_total{code="502"}[1d])` in the
    metrics TSDB (Prometheus/CloudWatch) going back to May 1. Counters are cheap
    and usually retained far longer than sampled request logs.
  - CDN / upstream-of-LB edge logs (separate retention tier).
  - Ticket/alert history: was there a 502 alert before May 14?
DISCRIMINATOR: a non-zero 502 rate on May 1-13 at ~30/day => kernel FALSIFIED as
onset cause. A true step at May 14 in the counter => CONFIRMED (temporality+step).

## P2 — Read the failure signature, don't bisect
All samples are `upstream_timeout`. Pull (read-only) the LB's upstream
timeout/connect config and current p99 upstream latency from metrics. A kernel
networking regression (e.g. conntrack, TCP backlog, RSS/RPS) tends to show as
connection resets/SYN retransmits, not clean upstream read timeouts. Compare
SYN-retransmit / conn-reset counters across the May 14 boundary in the TSDB.

## P3 — Canary, not bisect
The "can't bisect" constraint forbids rolling prod back. It does NOT forbid
standing up ONE canary LB on the PRE-May-14 kernel behind a 1-5% traffic split
(or shadow traffic). Run for the ~3-4 days needed to accumulate enough samples
(502s are ~30/day fleet-wide; size the canary/duration for power). Compare 502
rate canary-vs-fleet. This is the controlled but-for test without a prod outage.

## Power note
At 0.001% (~30/day across the fleet), detecting a rate change needs days of
canary or counter history, not minutes. State n and duration before running P3.
