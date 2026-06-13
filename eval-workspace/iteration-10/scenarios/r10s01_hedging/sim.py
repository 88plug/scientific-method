"""Tail-latency sim. Each request hits one replica; latency ~ lognormal with
a 3% slow mode (10x). You may invent a request POLICY (when/whether to send
a second 'hedge' to another replica; first response wins).
Baseline: single request. Acceptance: p99 reduced >=40% vs baseline at
<=15% extra backend load. score(policy) reports p50/p99/extra_load.
policy(elapsed_ms, state) -> 'hedge' | 'wait' called each ms until response.
"""
import random
def draw(rng):
    base=rng.lognormvariate(2.3,0.4)
    return base*10 if rng.random()<0.03 else base
def score(policy, n=20000, seed=21):
    rng=random.Random(seed); lats=[]; sent=0; hedged=0
    for _ in range(n):
        a=draw(rng); sent+=1
        state={}; fired=None
        t=0
        while True:
            if t>=a: lats.append(a if fired is None else min(a, fired+t0_h)); break
            if fired is None and policy(t,state)=='hedge':
                b=draw(rng); fired=b; t0_h=t; sent+=1; hedged+=1
                if t+b < a: lats.append(t+b); break
            t+=1
    lats.sort()
    return {"p50":round(lats[len(lats)//2],1),"p99":round(lats[int(len(lats)*0.99)],1),
            "extra_load_pct":round(100*hedged/n,1)}
def baseline(t,state): return 'wait'
if __name__=='__main__': print("baseline:",score(baseline))
