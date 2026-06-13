"""SOUNDNESS: (1) confirm the sim's counter model; (2) integer/second quantization survival.

The sim calls policy(attempt, status, state) with a FRESH state={} per request, but the
DecorrelatedSpreadPolicy instance is shared, so self.ctr is the single global counter.
Verify that the measured win is destroyed if the counter is per-request (i.e. if the
policy could NOT carry shared state -- the distributed reality)."""
import sim, random
from policy import DecorrelatedSpreadPolicy

# (1) Shared-counter dependence: a policy that resets ctr each request (=distributed,
# every request sees the same k sequence) -- drop-in, same window, same math.
PHI=0.6180339887498949
class PerRequestPolicy:
    def __init__(self, base=31.0, span=70.0, maxa=3):
        self.base=base; self.span=span; self.maxa=maxa
    def __call__(self, attempt, last, state):
        if attempt>self.maxa: return None
        # no shared counter available: index by attempt only (all first-retries -> k=1)
        return self.base + (((attempt)*PHI)%1.0)*self.span

print("shared-counter (as-submitted):", sim.score(DecorrelatedSpreadPolicy(31.0,70.0,3)))
print("per-request golden (distributed):", sim.score(PerRequestPolicy(31.0,70.0,3)))

# (2) Integer quantization survival: the policy returns FLOAT delays; sim does int(t_try)
# binning. The three-distance / equidistribution argument is over the REAL window. After
# int() quantization to 70 one-second bins, does equidistribution survive for the global
# stream? (already shown in check_gaps: max-bin within +1 of ideal). Confirm rounding
# direction doesn't pile a boundary bin.
slots=[((k+1)*PHI)%1.0 for k in range(30000)]
import collections
bins=collections.Counter(int(31.0+s*70.0) for s in slots)
lo,hi=min(bins),max(bins)
print(f"\nquantized bins span seconds [{lo},{hi}] ({len(bins)} bins), counts min={min(bins.values())} max={max(bins.values())}")
print("bin 31 (boundary, base):", bins[31], " bin 100 (last):", bins.get(100), " bin 101:", bins.get(101))
