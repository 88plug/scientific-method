# Two primaries
HA pair (2 nodes, primary + standby, automatic failover on heartbeat loss).
Last night a 40s network partition between them: standby promoted itself,
old primary kept serving. 6 minutes of divergent writes to both, painful
manual merge. Team proposal: "lower the heartbeat timeout from 10s to 3s so
failover is faster." Evaluate and recommend the real fix.
