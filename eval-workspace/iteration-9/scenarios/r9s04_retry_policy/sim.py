"""Retry-amplification sim. 1000 client req/s, server capacity 1500 rps,
server hard-down between t=30s and t=60s. Client policy decides retries.
Baseline: 3 immediate retries -> amplification ~4x during outage, recovery
delayed by retry backlog after the server returns.
Plug in policy(attempt, last_status, state) -> delay_seconds or None (give up).
Acceptance:
  - peak offered load during outage <= 2.0x base rate
  - p99 time-to-success for requests issued AFTER recovery (t>60) <= 2s
  - success ratio for requests during healthy periods >= 99.5%
score(policy) prints all three.
"""
import random
def score(policy, seed=13):
    rng=random.Random(seed)
    offered=[0]*121; outcomes=[]
    for t in range(120):
        for _ in range(1000):
            t_try=t; attempt=0; state={}
            start=t
            while True:
                if t_try>120: outcomes.append(("gaveup",start,None)); break
                offered[int(t_try)]+=1
                server_up = not (30<=t_try<60)
                cap_ok = offered[int(t_try)] <= 1500
                if server_up and cap_ok:
                    outcomes.append(("ok",start,t_try-start)); break
                attempt+=1
                d=policy(attempt, "down" if not server_up else "overload", state)
                if d is None: outcomes.append(("gaveup",start,None)); break
                t_try += d
    peak=max(offered[30:60])/1000
    post=[o[2] for o in outcomes if o[0]=="ok" and o[1]>60]
    post.sort()
    p99=post[int(len(post)*0.99)] if post else 999
    healthy=[o for o in outcomes if o[1]<30 or o[1]>61]
    succ=sum(1 for o in healthy if o[0]=="ok")/len(healthy)
    return {"peak_amplification":round(peak,2),"post_recovery_p99_s":p99,"healthy_success":round(succ,4)}
def baseline(attempt,last,state):
    return 0 if attempt<=3 else None
if __name__=='__main__': print("baseline:", score(baseline))
