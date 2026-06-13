# Provability brief
Invent + implement `apply(state_dict, op)` for a counter-CRDT-style op set
(increments with op-ids, merges of two states) with the claims:
(C1) applying the same op twice == applying once (idempotence),
(C2) merge is commutative, (C3) merge is associative, (C4) merge is
idempotent. Upgrade each claim per invent.md §4: property tests with
generated ops/states AND exhaustive enumeration over a stated small scope.
Claim chart with per-claim rungs; provenance search (this is CRDT territory —
name it).
