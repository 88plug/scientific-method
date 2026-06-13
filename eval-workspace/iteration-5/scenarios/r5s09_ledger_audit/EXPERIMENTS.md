# cache-layer campaign ledger (2026-06-01)

| # | Hypothesis | Probe | Verdict |
|---|---|---|---|
| H1 | LRU beats LFU on our trace | bench_lru.sh, trace-2026-05, n=10, commit 4f2a91c, median 412us vs 538us (±6us) | CONFIRMED (0.95) |
| H2 | 64MB cache is past the knee | "ran it, looked flat" | CONFIRMED (0.9) |
| H3 | TTL jitter removes the stampede | herd_sim.py commit 4f2a91c n=20: p99 conn spikes 1410->220 (±30) | CONFIRMED (0.93) |
| H4 | write-through costs <5% | bench from Marco's laptop before he left, no command recorded | CONFIRMED (0.92) |

## Reproduce
```bash
./bench_lru.sh trace-2026-05   # H1
python3 herd_sim.py --jitter   # H3
```
