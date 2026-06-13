"""Autoscaler sim. Pods serve 100 rps each; pod boot takes 45s; you pay
for pod-seconds. Demand: diurnal-ish wave + random spikes (2-4x for
30-90s). scale(t, observed_rps, current_pods, booting) -> desired_pods,
called每 5s. Baselines: reactive threshold (scale when util>80%, down<40%).
Acceptance (600s x 5 seeds):
  - dropped requests (demand beyond capacity) <= 0.4x reactive baseline's
  - pod-seconds <= 1.15x reactive baseline's
score(scaler) reports both.
"""
import random, math
def demand(t,rng,spikes):
    base=600+300*math.sin(t/120)
    for (s,d,m) in spikes:
        if s<=t<s+d: base*=m
    return base
def score(scaler, seed=139):
    rng=random.Random(seed)
    spikes=[(rng.uniform(60,500), rng.uniform(30,90), rng.uniform(2,4)) for _ in range(3)]
    pods=8; booting=[]; pod_seconds=0; dropped=0
    for step in range(120):
        t=step*5
        booting=[(r,b) for (r,b) in booting if b>t]
        ready=pods
        d=demand(t,rng,spikes)
        cap=ready*100
        dropped+=max(0,d-cap)*5
        pod_seconds+=ready*5+len(booting)*5
        want=scaler(t, d*(1+rng.uniform(-0.05,0.05)), ready, len(booting))
        want=max(1,min(60,int(want)))
        if want>ready+len(booting):
            for _ in range(want-ready-len(booting)): booting.append((t,t+45))
        pods=ready+sum(1 for (r,b) in booting if b<=t+5)
        booting=[(r,b) for (r,b) in booting if b>t+5]
    return {"dropped":int(dropped),"pod_seconds":pod_seconds}
def reactive(t,rps,pods,booting):
    util=rps/max(1,pods*100)
    if util>0.8: return pods+max(1,int(pods*0.5))
    if util<0.4: return max(1,pods-1)
    return pods
if __name__=='__main__': print("reactive:",score(reactive))
