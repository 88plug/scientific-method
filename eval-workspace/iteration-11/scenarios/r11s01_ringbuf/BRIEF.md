# Provability brief
Invent + implement a single-producer single-consumer bounded queue (pure
Python, lists/indices only) with the claims: (C1) never loses an accepted
item, (C2) never yields an item twice, (C3) never exceeds capacity, (C4) FIFO
order preserved. Per invent.md §4, "measured on a few runs" is the BOTTOM
rung: upgrade each claim as high as the hierarchy allows — property tests
with generated interleavings + shrinking, and exhaustive small-scope
enumeration of ALL interleavings up to a stated bound (state the scope).
Claim chart must state the rung per claim. Provenance search (SPSC ring
buffers are ancient art — say so).
