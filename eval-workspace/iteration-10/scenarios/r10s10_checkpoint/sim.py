"""Checkpoint pacing sim. A worker processes 1000 items/s; checkpointing
state costs a stop-the-world pause: pause_ms = 50 + items_since_last/40.
Crashes occur ~ poisson (mean every 120s, sim 1800s). On crash, all items
since the last checkpoint are reprocessed. policy(items_since, seconds_since)
-> bool (checkpoint now?). Baseline: every 60s.
Acceptance: total cost (pause time + reprocessing time at 1000 items/s)
<= 0.55x baseline's, same crash schedule (seeded).
"""
import random
def score(policy, seed=30):
    rng=random.Random(seed)
    crashes=[]; t=0
    while t<1800:
        t+=rng.expovariate(1/120); crashes.append(t)
    pause=0.0; reproc=0.0; last_cp=0.0; items=0; t=0.0; ci=0
    dt=0.1
    while t<1800:
        items+=int(1000*dt)
        if ci<len(crashes) and t>=crashes[ci]:
            reproc += items/1000.0; items=0; last_cp=t; ci+=1; continue
        if policy(items, t-last_cp):
            pause += (50+items/40)/1000.0; items=0; last_cp=t
        t+=dt
    return {"total_cost_s":round(pause+reproc,1)}
def baseline(items, secs): return secs>=60
if __name__=='__main__': print("baseline:",score(baseline))
