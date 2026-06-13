# Falsification log entry (DO-NOT-RE-ATTACK)

**Golden-ratio LDS retry timing** — REJECTED by peer review 2026-06-12
(4 blind lensed reviews + area chair; all artifacts in this directory).

Kill reason: the anti-clustering guarantee depended on a single shared
global counter (a sim affordance no distributed fleet has). Independent
clients computing the deterministic sequence phase-align into a maximal
herd (30k retries in one bin, 70x worse than random jitter). The only
repair re-introduces per-client randomness, which IS decorrelated jitter
(AWS/Brooker 2015). At matched window envelopes, LDS = RNG on every
instance variant — the original win was the envelope, not the mechanism.

Provenance footnote: the composition remains un-anticipated in the
searched corpus — un-anticipated and ineffective is not an invention
(Koza criterion D).

Reopen condition: a per-client-phase variant that (a) derives phases
without per-client entropy from coordination-free collision-free durable
IDs, AND (b) beats tuned decorrelated jitter across >=5 independent-client
variants beyond seed noise. The fatal-flaw review argues (a)+(b) is
self-contradictory; dissolve that first.

Pipeline lesson (now in invent.md sections 3 and 6): the verifier is part
of the claim; reproducibility is not validity; the target-regime gate is
mandatory before certified.
