# pipeline perf campaign — hypothesis ledger (2026-05-20)

## Falsification log (DO-NOT-RE-ATTACK)
- **W3 "mmap read path":** assumed mmap would beat buffered reads for the
  scan stage — **Disproved** (probe: bench_w3.sh): mmap 4.1s vs buffered 1.9s.
  DO-NOT-RE-ATTACK.
