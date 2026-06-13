"""Failure-detector sim. A peer sends heartbeats ~every 100ms with jitter
regimes that SHIFT (calm: sigma=10ms; congested: sigma=80ms, mean 140ms).
Three real crashes occur (heartbeats stop). detector(t_since_last, history)
-> 'suspect' | 'trust' is polled every 10ms.
Baseline: fixed 300ms timeout.
Acceptance: detect all 3 crashes within 1s each AND <=2 false suspicions
over the full 600s trace (baseline false-suspects ~20+ times during
congestion). score(detector) reports both.
"""
import random
def make(seed=122):
    rng=random.Random(seed); beats=[]; t=0.0
    crashes=[150.0, 350.0, 520.0]; ci=0; regime_until=0; sigma=10; mu=100
    while t<600:
        if ci<len(crashes) and t>=crashes[ci]:
            t+=rng.uniform(20,30); ci+=1; beats.append(('recover',t)); continue
        if t>regime_until:
            congested=rng.random()<0.35
            sigma,mu = (80,140) if congested else (10,100)
            regime_until=t+rng.uniform(20,60)
        t+=max(10,rng.gauss(mu,sigma))/1000.0
        beats.append(('beat',t))
    return beats, crashes
def score(detector, seed=122):
    beats,crashes=make(seed)
    beat_times=[t for k,t in beats if k=='beat']
    t=0.0; last=0.0; bi=0; suspected=[]; in_suspect=False; hist=[]
    while t<600:
        while bi<len(beat_times) and beat_times[bi]<=t:
            if last: hist.append(beat_times[bi]-last)
            last=beat_times[bi]; bi+=1; in_suspect=False
        if detector((t-last)*1000.0, hist[-50:])=='suspect' and not in_suspect:
            suspected.append(t); in_suspect=True
        t+=0.01
    detected=[]; false=0
    for s in suspected:
        if any(c<=s<=c+25 for c in crashes): detected.append(s)
        else: false+=1
    det_ok=sum(1 for c in crashes if any(c<=s<=c+1.0 for s in suspected))
    return {"crashes_detected_within_1s":det_ok,"false_suspicions":false}
def baseline(ms_since,hist): return 'suspect' if ms_since>300 else 'trust'
if __name__=='__main__': print("baseline:",score(baseline))
