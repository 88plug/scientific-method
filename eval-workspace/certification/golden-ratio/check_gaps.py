"""SOUNDNESS machine-check: re-derive the anti-clustering claim for the ACTUAL params.

Claim under test: golden-ratio additive sequence delay = base + ((k*phi) mod 1)*span
gives low-discrepancy spreading that "never clusters", beating random decorrelated jitter
on the gap (clustering) statistic, for the attempt counts that matter.

We compute, for N consecutive failing requests (N = number of requests that fail and retry
in this sim), the placement of their first-retry delays over the window and the resulting
per-second load, vs random uniform jitter. The load-bearing quantity in the sim is the
MAX requests landing in any single 1-second bin (sim quantizes via offered[int(t_try)]).
"""
import math, random

PHI = 0.6180339887498949
BASE, SPAN = 31.0, 70.0

def golden_slots(n):
    return [((k+1)*PHI) % 1.0 for k in range(n)]  # policy uses ctr starting at 1

def random_slots(n, seed):
    r = random.Random(seed)
    return [r.random() for _ in range(n)]

def max_per_second_bin(slots):
    """Quantize delay = base + slot*span the way the sim does: int(t_try).
    All n requests here are assumed to fail in the SAME source second (worst case
    thundering herd: phase-aligned). We bin by int(base + slot*span)."""
    bins = {}
    for s in slots:
        sec = int(BASE + s*SPAN)
        bins[sec] = bins.get(sec, 0) + 1
    return max(bins.values()), len(bins)

def three_distance_gaps(slots):
    xs = sorted(slots)
    gaps = [xs[i+1]-xs[i] for i in range(len(xs)-1)]
    gaps.append((1.0 - xs[-1]) + xs[0])  # wrap
    return min(gaps), max(gaps), len(set(round(g,9) for g in gaps))

# In the sim: 1000 req/s fail during the 30s outage = up to 30000 requests retry.
# But the golden counter is GLOBAL and increments per first-failure across the whole run.
# Test the attempt counts that matter: the full outage backlog.
print("=== Gap / clustering statistics: golden vs random ===")
print(f"{'N':>7} | {'gold_maxbin':>11} {'gold_dgaps':>10} | {'rand_maxbin(median/worst over 50 seeds)':>40}")
for n in [70, 100, 1000, 5000, 30000]:
    g = golden_slots(n)
    gmax, gbins = max_per_second_bin(g)
    gmin_gap, gmax_gap, n_distinct = three_distance_gaps(g)
    rmaxes = sorted(max_per_second_bin(random_slots(n, s))[0] for s in range(50))
    rmed = rmaxes[25]; rworst = rmaxes[-1]
    print(f"{n:>7} | {gmax:>11} {n_distinct:>4}dist  | rand median {rmed}, worst {rworst}")
    # Three-distance theorem: distinct gap lengths should be <=3 for golden
    assert n_distinct <= 3, f"THREE-DISTANCE VIOLATED at n={n}: {n_distinct} distinct gaps"
print("Three-distance theorem holds (<=3 distinct gap lengths) for all N tested.")

# Ideal uniform per-second bin: window is base..base+span = 31..101 => 70 one-second bins.
# n requests over 70 bins => ideal max bin = ceil(n/70).
print("\n=== vs ideal uniform max-bin (ceil(n/70)) ===")
for n in [70, 1000, 30000]:
    g = golden_slots(n)
    gmax,_ = max_per_second_bin(g)
    ideal = math.ceil(n/70)
    print(f"n={n:>5}: golden max-bin={gmax}, ideal={ideal}, excess={gmax-ideal}")
