"""Canary rollout sim. Releases arrive; each is secretly GOOD (error rate
0.5%, same as prod) or BAD (error rate 1.5-4%). Your controller routes a
fraction f(t) of 1,000 rps to the canary and observes per-request success;
it must decide PROMOTE or ABORT.
Costs: each bad-canary request that errors = 1 unit of user harm;
each second of delay before promoting a GOOD release = 0.5 units.
Acceptance over a 60-release schedule (25% bad), >=3 seeds:
  - all BAD releases aborted (zero bad promotions)
  - mean GOOD promote time <= 90s
  - total user harm <= 0.5x the fixed-strategy baseline (5% for 300s)
score(controller_factory) provided.
"""
import random
def score(cf, seed=136):
    rng=random.Random(seed); harm=0.0; promote_times=[]; bad_promoted=0
    for rel in range(60):
        bad = rng.random()<0.25
        er = rng.uniform(0.015,0.04) if bad else 0.005
        c=cf(); t=0; decided=None
        while t<600 and decided is None:
            f=max(0.0,min(1.0,c.fraction(t)))
            n=int(1000*f)
            errs=sum(1 for _ in range(n) if rng.random()<er)
            if bad: harm+=errs/1000.0*1.0*1   # scaled
            decided=c.observe(t,n,errs)
            t+=1
        if decided=='promote':
            if bad: bad_promoted+=1
            else: promote_times.append(t)
        elif decided is None and not bad: promote_times.append(600)
    return {"bad_promoted":bad_promoted,
            "mean_good_promote_s":round(sum(promote_times)/max(1,len(promote_times)),1),
            "harm":round(harm,2)}
class Fixed:
    def __init__(s): s.e=0; s.n=0
    def fraction(s,t): return 0.05 if t<300 else 0.0
    def observe(s,t,n,errs):
        s.e+=errs; s.n+=n
        if t>=300: return 'abort' if s.e/max(1,s.n)>0.009 else 'promote'
        return None
if __name__=='__main__': print("fixed 5%/300s:", score(Fixed))
