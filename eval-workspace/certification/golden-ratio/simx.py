"""Generalized r9s04 sim for INSTANCE-DIVERSITY review.

Faithful to the original sim.py mechanics (same per-second offered[] accounting,
same retry loop, same acceptance metric definitions) but parameterized so the
outage profile, capacity, load, and horizon can vary. Metric windows TRACK the
actual outage rather than the hardcoded 30..60 of the original.

down(t)  -> True if server is hard-down at integer second t
cap      -> per-second server capacity (requests served that second)
load     -> fresh requests issued per second
horizon  -> seconds simulated
recovery_end -> first second at/after which the server is up for good
               (defines the "post-recovery" latency window: start > recovery_end)
outage_secs -> the set/range of seconds counted for peak amplification

policy is a callable(attempt,last_status,state)->delay|None. It is re-instantiated
per run via a factory so stateful policies (golden-ratio counter, RNG) start fresh.
"""

def score(policy_factory, down, cap, load, horizon, outage_secs, recovery_end, seed=13):
    import random
    rng = random.Random(seed)          # mirrors original: available to policy via closure if it wants
    policy = policy_factory(rng)
    offered = [0] * (horizon + 1)
    outcomes = []
    for t in range(horizon):
        for _ in range(load):
            t_try = t; attempt = 0; state = {}
            start = t
            while True:
                if t_try > horizon:
                    outcomes.append(("gaveup", start, None)); break
                it = int(t_try)
                offered[it] += 1
                server_up = not down(it)
                cap_ok = offered[it] <= cap
                if server_up and cap_ok:
                    outcomes.append(("ok", start, t_try - start)); break
                attempt += 1
                d = policy(attempt, "down" if not server_up else "overload", state)
                if d is None:
                    outcomes.append(("gaveup", start, None)); break
                t_try += d
    base_rate = load
    peak = max(offered[s] for s in outage_secs) / base_rate
    post = [o[2] for o in outcomes if o[0] == "ok" and o[1] > recovery_end]
    post.sort()
    p99 = post[int(len(post) * 0.99)] if post else 999
    healthy = [o for o in outcomes
               if (o[1] < min(outage_secs)) or (o[1] > recovery_end + 1)]
    succ = (sum(1 for o in healthy if o[0] == "ok") / len(healthy)) if healthy else 1.0
    # ground-truth: max offered in any post-recovery second (cap-breach check)
    max_post_offered = max((offered[s] for s in range(recovery_end + 1, horizon)),
                           default=0)
    gaveup = sum(1 for o in outcomes if o[0] == "gaveup") / len(outcomes)
    return {
        "peak_amplification": round(peak, 2),
        "post_recovery_p99_s": p99,
        "healthy_success": round(succ, 4),
        "max_post_offered": max_post_offered,
        "cap": cap,
        "gaveup_frac": round(gaveup, 4),
    }
