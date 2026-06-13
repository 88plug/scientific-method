import statistics
from simx import score
from baselines import GoldenFactory, JitterFactory

JITTER_SEEDS = list(range(20))  # spread for the RNG baseline


def down_window(lo, hi):
    return lambda t: lo <= t < hi


def down_flap(segments):
    # segments: list of (lo,hi) down intervals
    return lambda t: any(lo <= t < hi for lo, hi in segments)


def run_one(name, down, cap, load, horizon, outage_secs, recovery_end):
    g = score(GoldenFactory(), down, cap, load, horizon, outage_secs, recovery_end)
    # jitter: distribution over many seeds
    jr = [score(JitterFactory(), down, cap, load, horizon, outage_secs, recovery_end, seed=s)
          for s in JITTER_SEEDS]
    def agg(key):
        vals = [r[key] for r in jr]
        return (round(min(vals), 4), round(statistics.mean(vals), 4), round(max(vals), 4))
    print(f"\n=== {name} ===  (cap={cap} load={load} horizon={horizon})")
    print(f"  GOLDEN : peak={g['peak_amplification']}  p99={g['post_recovery_p99_s']}  "
          f"healthy={g['healthy_success']}  maxPostOffered={g['max_post_offered']}  gaveup={g['gaveup_frac']}")
    pk, p9, hl = agg('peak_amplification'), agg('post_recovery_p99_s'), agg('healthy_success')
    print(f"  JITTER : peak(min/mean/max)={pk}  p99={p9}  healthy={hl}  (n={len(JITTER_SEEDS)} seeds)")
    # acceptance per the original three criteria
    def ok(r): return r['peak_amplification'] <= 2.0 and r['post_recovery_p99_s'] <= 2 and r['healthy_success'] >= 0.995
    j_pass = sum(1 for r in jr if ok(r))
    print(f"  ACCEPT : golden={'PASS' if ok(g) else 'FAIL'}  jitter={j_pass}/{len(jr)} seeds pass")
    return g, jr


# --- V0: original params, sanity that simx == sim ---
run_one("V0 original (30s outage, cap1500)", down_window(30, 60), 1500, 1000, 120,
        range(30, 60), 60)

# --- V1: short 5s outage ---
run_one("V1 short outage 5s (t=30..35)", down_window(30, 35), 1500, 1000, 120,
        range(30, 35), 35)

# --- V2: long 120s outage, longer horizon so recovery is observable ---
run_one("V2 long outage 120s (t=30..150)", down_window(30, 150), 1500, 1000, 240,
        range(30, 150), 150)

# --- V3: tighter capacity ratio (cap 1100 vs load 1000 -> only 100 headroom) ---
run_one("V3 tight capacity (cap=1100)", down_window(30, 60), 1100, 1000, 120,
        range(30, 60), 60)

# --- V3b: looser capacity (cap 3000) ---
run_one("V3b loose capacity (cap=3000)", down_window(30, 60), 3000, 1000, 120,
        range(30, 60), 60)

# --- V4: flapping outage down-up-down ---
run_one("V4 flapping (down 30..45, up, down 55..70)",
        down_flap([(30, 45), (55, 70)]), 1500, 1000, 140,
        list(range(30, 45)) + list(range(55, 70)), 70)

# --- V5: thundering herd: huge batch fails at the same instant ---
# Model as a very short outage (1s) at t=30 with a tight cap so a large fraction
# of one second's load is forced to retry simultaneously; capacity tight so the
# synchronized retry wave is what stresses the system.
run_one("V5 thundering-herd (1s blackout t=30, cap=1100)",
        down_window(30, 31), 1100, 1000, 120, range(30, 31), 31)
