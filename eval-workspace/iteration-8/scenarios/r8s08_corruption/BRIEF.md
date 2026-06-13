# Invention brief
A storage pipeline moves ~10TB/day. Rare silent corruption (~1 event/week,
burst of contiguous bytes) is found weeks later by customers. Full re-hashing
of everything daily is too expensive (budget: <2% I/O overhead). Invent at
least 4 detection schemes within budget; refute; design the validation
experiment for the best one; a small simulation (corrupt_sim.py provides a
corpus + corruption injector) may be used to demonstrate detection rates.
