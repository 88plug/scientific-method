"""ATTACK 1 — Cross-client correlation / synchronized waves.

The submission's policy spreads retries via a GLOBAL monotonic counter
`self.ctr`, incremented once per request across the whole sim. In sim.py
there is exactly ONE module-level `_policy` instance shared by all 120k
requests, so every request draws a DISTINCT slot ctr*PHI mod 1 -> perfect
low-discrepancy spread. That shared counter is the load-bearing trick.

The CLAIM, though, is "a CLIENT retry policy" that clients run to avoid
clustering during outage recovery, beating per-client random jitter. Real
distributed clients do NOT share a global counter. The realistic question:
when many independent clients each compute a deterministic delay, what
phase does each one use, and do they synchronize?

We model the realistic deployment: N independent clients, each running the
SAME deterministic policy with its OWN local attempt counter (starting
from its own request). We test three plausible per-client phasing schemes
that an engineer would actually ship:

  (A) PHASE-BY-ATTEMPT: delay = base + ((attempt*PHI)%1)*span
      Pure "deterministic by attempt number" — the literal reading of
      "compute the same deterministic delay sequence by attempt number"
      from the attack brief. No per-client entropy at all.

  (B) PHASE-BY-LOCAL-COUNTER: each client has its own ctr starting at 0,
      ++ per request. Independent clients that started cleanly all walk
      the SAME ctr sequence 1,2,3,... -> identical slots.

  (C) The sim's own god's-eye shared global counter (the submission), for
      reference — not realizable across independent clients.

Metric: peak retry arrivals in any 1s bin during recovery, vs per-client
random jitter over the same window. If deterministic >> random, the
mechanism CAUSES the herd it claims to prevent.
"""
import random, math

PHI = 0.6180339887498949

def run(N_clients, scheme, span=70.0, base=31.0, seed=0):
    """All N clients fail simultaneously at t=0 (outage instant) and each
    schedules its first retry. Return histogram of retry arrival times in
    1s bins; report the peak bin (the herd)."""
    rng = random.Random(seed)
    bins = {}
    global_ctr = 0
    for c in range(N_clients):
        if scheme == "A_attempt":
            attempt = 1
            u = (attempt * PHI) % 1.0
            delay = base + u * span
        elif scheme == "B_localctr":
            # each independent client's own counter, all start at 1
            ctr = 1
            u = (ctr * PHI) % 1.0
            delay = base + u * span
        elif scheme == "C_shared":
            global_ctr += 1
            u = (global_ctr * PHI) % 1.0
            delay = base + u * span
        elif scheme == "random":
            delay = base + rng.random() * span
        b = int(delay)
        bins[b] = bins.get(b, 0) + 1
    peak = max(bins.values())
    return peak, len(bins), bins

N = 30000  # ~the outage backlog the VERDICT cites
print(f"=== ATTACK 1: {N} clients all fail at the same instant, schedule retry ===")
print(f"(perfect spread = ~{N/70:.0f}/bin over a 70s window; herd = one giant bin)\n")
for scheme, label in [
    ("A_attempt",  "Deterministic by ATTEMPT number (literal claim)"),
    ("B_localctr", "Deterministic per-client local counter (clean clients)"),
    ("C_shared",   "Submission's SHARED global counter (god's-eye, sim-only)"),
    ("random",     "Per-client random jitter (the baseline it 'beats')"),
]:
    peak, nbins, _ = run(N, scheme)
    print(f"  {label}")
    print(f"      peak retries in one 1s bin: {peak:6d}   bins used: {nbins:3d}")
print()
print("Interpretation: if A/B peaks ~= N (all in one bin) while random peaks")
print("near N/70, the deterministic policy SYNCHRONIZES independent clients")
print("into the exact wave the mechanism claims to prevent.")
