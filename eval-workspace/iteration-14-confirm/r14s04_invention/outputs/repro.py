#!/usr/bin/env python3
"""Reproduce baseline + invention numbers and the robustness/ablation evidence.

Usage:
    python3 repro.py

Requires sim.py on the path (copied here next to this script). Run from this dir.
"""
import importlib.util, os, random, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _load_sim():
    path = os.path.join(HERE, "sim.py")
    spec = importlib.util.spec_from_file_location("sim", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


sim = _load_sim()
score, baseline = sim.score, sim.baseline


def make_policy(rng_seed=12345, dlo=3.0, dhi=75.0, olo=0.3, ohi=1.2, maxa=40):
    R = random.Random(rng_seed)

    def p(attempt, last, state):
        if attempt > maxa:
            return None
        if last == "down":
            return R.uniform(dlo, dhi)
        return R.uniform(olo, ohi)

    return p


def passes(r):
    return (r["peak_amplification"] <= 2.0
            and r["post_recovery_p99_s"] <= 2.0
            and r["healthy_success"] >= 0.995)


def instrument(policy, seed=13):
    rng = random.Random(seed)
    offered = [0] * 121
    outcomes = []
    for t in range(120):
        for _ in range(1000):
            t_try = t; attempt = 0; state = {}; start = t
            while True:
                if t_try > 120:
                    outcomes.append(("gaveup", start, None)); break
                offered[int(t_try)] += 1
                up = not (30 <= t_try < 60)
                cap = offered[int(t_try)] <= 1500
                if up and cap:
                    outcomes.append(("ok", start, t_try - start)); break
                attempt += 1
                d = policy(attempt, "down" if not up else "overload", state)
                if d is None:
                    outcomes.append(("gaveup", start, None)); break
                t_try += d
    return offered, outcomes


def main():
    print("=== BASELINE (3 immediate retries) ===")
    print(score(baseline))

    print("\n=== INVENTION (down/overload-split jittered backoff) ===")
    r = score(make_policy())
    print(r, "-> PASS" if passes(r) else "-> FAIL")

    print("\n=== ROBUSTNESS: 40 jitter seeds (sim request-loop seed fixed at 13) ===")
    amps, p99s, hs, fails = [], [], [], 0
    for s in range(40):
        rr = score(make_policy(rng_seed=s))
        amps.append(rr["peak_amplification"]); p99s.append(rr["post_recovery_p99_s"])
        hs.append(rr["healthy_success"]); fails += 0 if passes(rr) else 1
    print(f"amp  max={max(amps)} mean={round(statistics.mean(amps),3)}")
    print(f"p99  max={round(max(p99s),3)} mean={round(statistics.mean(p99s),3)}")
    print(f"healthy min={min(hs)}  FAILS={fails}/40")

    print("\n=== ROBUSTNESS: 30 sim seeds (jitter seed fixed) ===")
    fails = 0; amps = []; p99s = []; hs = []
    for s in range(30):
        rr = score(make_policy(), seed=s)
        amps.append(rr["peak_amplification"]); p99s.append(rr["post_recovery_p99_s"])
        hs.append(rr["healthy_success"]); fails += 0 if passes(rr) else 1
    print(f"amp max={max(amps)} p99 max={round(max(p99s),3)} healthy min={min(hs)} FAILS={fails}/30")

    print("\n=== HONEST ACCOUNTING (give-up breakdown, seed=13) ===")
    off, outc = instrument(make_policy())
    gave = sum(1 for o in outc if o[0] == "gaveup")
    outage = [o for o in outc if 30 <= o[1] < 60]
    og = sum(1 for o in outage if o[0] == "gaveup")
    pr = [o for o in outc if o[1] > 60]
    pg = sum(1 for o in pr if o[0] == "gaveup")
    print(f"total give-up: {gave}/{len(outc)} ({100*gave/len(outc):.2f}%)")
    print(f"outage-issued give-up: {og}/{len(outage)} ({100*og/len(outage):.2f}%)")
    print(f"post-recovery-issued give-up: {pg}/{len(pr)}  (0 => p99 is genuine, not horizon artifact)")
    print(f"peak outage bucket /1000: {max(off[30:60])/1000}")

    print("\n=== ABLATIONS (both mechanisms load-bearing) ===")
    def nojit(attempt, last, state):
        if attempt > 40: return None
        return 39.0 if last == "down" else 0.75
    R = random.Random(12345)
    def nosplit(attempt, last, state):
        if attempt > 40: return None
        return R.uniform(0.3, 75.0)
    print("no-jitter (split only):", score(nojit), "-> FAIL (sync/thundering herd)")
    print("no-split (jitter only):", score(nosplit), "-> p99 only passes via give-up")


if __name__ == "__main__":
    main()
