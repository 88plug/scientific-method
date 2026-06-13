"""SOUNDNESS probe: does the anti-clustering guarantee survive a thundering-herd
trigger where many requests fail at the SAME instant?

The mechanism's spreading comes ENTIRELY from a single GLOBAL monotone counter `ctr`
shared across all requests (policy.py: self.ctr += 1 on each first-failure). The
low-discrepancy property is a property of consecutive counter VALUES, NOT of time.

So the real question for soundness: in deployment, what plays the role of `ctr`?
Two regimes:
 (A) ONE shared in-process counter (the sim): every failing request, regardless of
     when it failed, gets the NEXT counter value -> perfect golden interleave. This
     is what the sim measures.
 (B) DISTRIBUTED clients: each client process has its OWN counter starting at 0,
     OR each request independently computes phi*k with its own k. If many clients
     fail simultaneously and each starts its sequence at the same k (e.g. k=1 on
     first retry), they ALL pick the SAME slot -> total phase alignment -> a single
     1-second bin gets ALL of them. Determinism becomes a LIABILITY.

We test regime B: N clients each independently fail at the same instant, each using
attempt-number as its sequence index (the only per-request state available without a
shared counter)."""
import random
PHI = 0.6180339887498949
BASE, SPAN = 31.0, 70.0

def bin_of(slot):
    return int(BASE + slot*SPAN)

def maxbin(slots):
    b={}
    for s in slots: b[bin_of(s)]=b.get(bin_of(s),0)+1
    return max(b.values())

N = 30000  # outage backlog all failing in the same instant

# Regime A: shared global counter (what the sim implements)
shared = [((k+1)*PHI)%1.0 for k in range(N)]
print(f"Regime A (shared global counter, = the sim): max 1s bin = {maxbin(shared)}")

# Regime B1: every client independently on its FIRST retry -> all use k=1 -> same slot
indep_same_k = [((1)*PHI)%1.0 for _ in range(N)]
print(f"Regime B1 (distributed, all on attempt=1, no shared state): max 1s bin = {maxbin(indep_same_k)}  <-- ALL collide")

# Regime B2: distributed clients seed k from a per-client id (e.g. hash). If ids are
# 0..N-1 contiguous it's fine; if ids collide mod something, partial alignment.
indep_id = [((cid+1)*PHI)%1.0 for cid in range(N)]
print(f"Regime B2 (distributed, k=client_id 0..N-1 contiguous): max 1s bin = {maxbin(indep_id)}")

# Regime B3 (realistic): random RNG decorrelated jitter, distributed, no coordination
r=random.Random(0)
rand_dist=[r.random() for _ in range(N)]
print(f"Regime B3 (distributed random jitter, the standard baseline): max 1s bin = {maxbin(rand_dist)}")

print()
print("INTERPRETATION:")
print("- The sim's win depends ENTIRELY on a single shared in-process counter ordering")
print("  the global stream of failures. That models ONE client process (or one LB).")
print("- A real outage-recovery thundering herd is MANY independent clients. Without a")
print("  shared counter they cannot reconstruct the golden interleave; the deterministic")
print("  sequence index they DO share (attempt number) phase-ALIGNS them (B1) -- strictly")
print("  WORSE than random jitter (B3), which needs no coordination to decorrelate.")
