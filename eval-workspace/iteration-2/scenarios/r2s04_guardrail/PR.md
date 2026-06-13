# PR #88: faster aggregation
Rewrote the aggregator — **~35% faster** on the standard 8M-line input
(gen.py). Output unchanged. Requesting sign-off for the ingest fleet, where
these workers are memory-capped at 512MB per cgroup.
