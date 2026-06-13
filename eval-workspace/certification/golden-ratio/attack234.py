"""ATTACKS 2-4, plus the proposed repair.

(2) PHASE ADVERSARY: even with the god's-eye shared counter, an adversary
    who controls request ARRIVAL ORDER picks which clients get adjacent
    ctr values. Adjacent ctr -> slots PHI apart (0.618 of the window) =
    well separated, GOOD. But the adversary can instead make the SAME set
    of clients fail repeatedly: a client failing on attempt k uses the same
    state['u'] for all its retries (u is frozen on first failure). So an
    adversary that forces a cohort to fail in lockstep replays one slot.
    We test cohort-replay synchronization.

(3) QUANTIZATION COLLAPSE: real timers tick. Round each delay to a 1s grid
    (or coarser) and recount distinct slots. Low-discrepancy over a
    continuum collapses to pigeonhole over few buckets.

(4) STATE LOSS: client restarts reset the local counter to 0. A fleet that
    crash-loops together (common in an outage!) all restart at ctr=1 ->
    identical slot -> synchronized.

REPAIR: per-client random phase offset u0; delay = base + ((u0 + k*PHI)%1)*span.
    This is just... per-client random jitter on the phase. We test it and
    note it is exactly the prior-art it claims to beat (AWS "decorrelated
    jitter" / full jitter, Marc Brooker 2015).
"""
import random
PHI = 0.6180339887498949

def herd(slots, span=70.0):
    bins = {}
    for u in slots:
        b = int(31.0 + u*span)
        bins[b] = bins.get(b,0)+1
    return max(bins.values()), len(bins)

N = 30000

# (2) cohort replay: a cohort fails together; each uses its frozen u.
# Worst case for adversary: force clients whose ctr maps to the SAME 1s bin
# to be the ones that keep failing. With shared ctr, slots are k*PHI mod 1;
# pick the cohort sharing a bin. How big can one bin get -> see attack1 (430).
# Adversary can also defeat spread by making ALL retries reuse attempt-1 slot
# if it can force first-failures to interleave so consecutive ctr collide:
# but golden ratio's whole point is consecutive don't collide. The real
# adversarial lever is (4)+correlated-failure, tested below.

# (3) quantization
print("=== ATTACK 3: timer quantization ===")
shared_slots = [ (k*PHI)%1.0 for k in range(1, N+1) ]
for grid in [1.0, 2.0, 5.0]:
    bins={}
    for u in shared_slots:
        d = 31.0 + u*70.0
        d = round(d/grid)*grid
        bins[d]=bins.get(d,0)+1
    print(f"  grid={grid}s: distinct delay values={len(bins):3d}, peak/value={max(bins.values())}")
print("  (70s window / grid => ceiling on distinct slots; e.g. 5s grid => <=15 slots,")
print("   so >=2000 clients share each slot regardless of golden ratio.)\n")

# (4) state loss: correlated restart
print("=== ATTACK 4: correlated restart (fleet crash-loops together) ===")
restart_slots = [ (1*PHI)%1.0 for _ in range(N) ]  # everyone resets ctr->1
peak,nb = herd(restart_slots)
print(f"  all clients restart at ctr=1: peak={peak} in {nb} bin(s)  -> total synchronization\n")

# REPAIR: per-client random phase offset
print("=== REPAIR: per-client random phase offset (=== decorrelated jitter) ===")
rng=random.Random(1)
repair_slots=[ (rng.random()+1*PHI)%1.0 for _ in range(N) ]
peak,nb=herd(repair_slots)
print(f"  delay=base+((u0+k*PHI)%1)*span, u0~U(0,1): peak={peak} in {nb} bins")
print("  This restores spread -- but the entropy doing the work is u0 (random),")
print("  not the golden ratio. It IS per-client random jitter. Prior art:")
print("  AWS Architecture Blog, Marc Brooker, 'Exponential Backoff And Jitter'")
print("  (2015): full jitter / decorrelated jitter. The deterministic golden")
print("  ratio is doing nothing the random offset isn't already doing.")
