# Verified observations (each independently confirmed)
E1: 500s occur at all hours, NOT clustered after the 03:00 rebuild (uniform across the day)
E2: every failing request contains a quoted-phrase + wildcard combination ("..."*"); replaying any such query reproduces the 500 deterministically
E3: GC logs show pauses <80ms p99.9 throughout (no long pauses at failure times)
E4: failures hit ALL index nodes equally, incl. node-local requests (no network hop)
E5: error rate is exactly 0 for the 3 weeks BEFORE the parser deploy; first 500 is 71 minutes after it
E6: index checksum verification passes daily (all shards)
E7: retries of a failing query against a different node also fail (same query)
