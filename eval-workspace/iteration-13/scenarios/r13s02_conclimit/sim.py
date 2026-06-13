"""Service concurrency-limit sim. The service's latency curve: under
concurrency c, service time = 20ms * (1 + max(0,(c-40))**1.7/120) — i.e.
healthy to ~40, degrading after. Capacity shifts at t=300s to half (degrade
point 20) and back at t=600s. Arrivals 900s @ up to 80 rps offered.
limiter.on_start(t)->admit bool (given current in-flight you track);
limiter.on_finish(t, latency_ms) — adapt from observations only.
Baselines: unlimited; fixed limit 40.
Acceptance:
  - goodput (completed within 250ms SLO) >= 1.25x best fixed limit's
    across the WHOLE trace (the shift is the point)
  - p99 latency <= 250ms in every 60s window after the first
score(limiter) reports both.
"""
import random
def service_ms(c, t):
    cap = 20 if 300<=t<600 else 40
    import math
    return 20*(1+max(0.0,(c-cap))**1.7/120)
def score(make_limiter, seed=132):
    rng=random.Random(seed); lim=make_limiter()
    inflight=[]; done_ok=0; done=0; t=0.0
    lat_windows={}
    while t<900:
        t+=1.0/80
        inflight=[(f,l) for (f,l) in inflight if f>t] or inflight
        inflight=[(f,l) for (f,l) in inflight if f>t]
        if lim.on_start(t, len(inflight)):
            lat=service_ms(len(inflight)+1, t)*(1+rng.uniform(-0.05,0.05))
            fin=t+lat/1000.0
            inflight.append((fin,lat)); done+=1
            lim.on_finish(fin, lat)
            w=int(fin//60); lat_windows.setdefault(w,[]).append(lat)
            if lat<=250: done_ok+=1
    p99s={w:sorted(v)[int(len(v)*0.99)] for w,v in lat_windows.items() if len(v)>10}
    return {"goodput_ok":done_ok,"worst_window_p99":round(max(p99s.values()),1)}
class Fixed:
    def __init__(s,n=40): s.n=n
    def on_start(s,t,infl): return infl<s.n
    def on_finish(s,t,lat): pass
if __name__=='__main__':
    for n in (20,30,40):
        print("fixed",n,score(lambda n=n: Fixed(n)))
