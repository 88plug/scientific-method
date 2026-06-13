# Sharded time-series store (16 shards)
shard key = timestamp rounded to hour ("so range queries are fast")
write load now: shard handling the CURRENT hour: 14,000 w/s (saturated, 95%
of writes); other 15 shards: ~50 w/s each, idle.
Reads: 90% are "last 24h for device X".
Proposal: "add 16 more shards." Evaluate and recommend.
