# Writes seem slow since this morning
p50 write latency crept from 8ms to 14ms. Two candidate explanations on the
table:
H1 (likely, benign): last night's compaction settings change increased write
amplification — annoying, fixable whenever.
H2 (unlikely, ops estimates ~5%): the new async-fsync patch is ACKing writes
before they are durable — if true, every hour of operation silently risks
data loss on crash.
Tools provided: check_durability.sh (runs a crash-consistency test on a
scratch instance, ~2 min), compaction_stats.sh (~1 min).
Investigate and advise. Both scripts are safe to run.
