# FULL-LEVER brief: invent.md pipeline end-to-end — quota ideation (>=6/>=3 lenses),
# refute-by-probe, build, fair gates (tuned baseline/diversity/ablation/holdout),
# provability upgrade where the claim allows, LIVE provenance, claim chart (single
# table), honest rung (witness-artifact rule), disclosure, §8 self-rank.

Problem: an append-only audit log of 1,000,000 entries must support
(a) O(1)-amortized append cost (accounted), and (b) a verifier with a
budget of <=1,000 entry-reads per audit that catches ANY single
contiguous tampering (modify/delete/insert of up to 1,000 entries) with
>=99% probability per audit, and locates it within +-2,000 entries.
Design the structure + verifier, implement, and measure detection over
>=300 random tamper trials (vary position+size). Account append overhead.
Rich known art (Merkle/CT logs, skip-lists, sampling auditors) — the
composition and the budget math are yours to get right and to
provenance-search.
