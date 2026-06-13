"""Overload admission sim. Server capacity 100 rps; arrivals oscillate
60-180 rps in waves. Each request has a 'value' (1-100, pareto-ish).
admit(value, observed_state) -> bool. Dropping is free; admitting beyond
capacity queues (latency grows). Baseline: admit-all.
Acceptance: total admitted VALUE >= 1.55x baseline's value-delivered-
within-SLO (SLO: served within 2s), while p99 queue wait <= 2s.
score(admit) reports both. State: anything O(1)-ish you maintain from
the values you've seen (no peeking at the future).
"""
import random, math
def score(admit, seed=28, seconds=600):
    rng=random.Random(seed)
    q=[]; served_value_in_slo=0; t=0.0; admitted=0; waits=[]
    for s in range(seconds):
        rate=120+60*math.sin(s/30)
        for _ in range(int(rate)):
            v=min(100,int(rng.paretovariate(1.2)))
            if admit(v, None):
                q.append((s,v)); admitted+=1
        # serve up to 100/s
        for _ in range(100):
            if not q: break
            ts,v=q.pop(0); w=s-ts; waits.append(w)
            if w<=2: served_value_in_slo+=v
    waits.sort()
    p99=waits[int(len(waits)*0.99)] if waits else 0
    return {"value_in_slo":served_value_in_slo,"p99_wait_s":p99}
def baseline(v,_): return True
if __name__=='__main__': print("baseline:",score(baseline))
