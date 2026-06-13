# Sporadic 500s on /search (3 weeks)
Four candidate causes circulating; settle it with the evidence below.
H1: search-index nightly rebuild leaves a corrupt shard
H2: JVM GC pauses under memory pressure
H3: the new query-parser (deployed 3 weeks ago) chokes on rare syntax
H4: network flakiness to the index nodes
