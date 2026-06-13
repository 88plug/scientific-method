"""Rate-limiter fairness sim. Plug a limiter class in and run score().
Clients: 3 heavy steady (80 rps each), 5 light bursty (avg 4 rps, bursts of 20).
Capacity: 200 rps total. A limiter decides admit/reject per request.
Baseline (baseline_limiter): global token bucket — bursty clients starve
during heavy load (their bursts arrive when the bucket is drained).
Acceptance for an invented limiter:
  - Jain fairness index over per-client admit RATIO >= 0.90
  - aggregate admitted throughput >= 95% of capacity utilization achieved by baseline
"""
import random
class BaselineLimiter:
    def __init__(self, rate=200): self.tokens=rate; self.rate=rate
    def tick(self):  self.tokens=min(self.rate, self.tokens+self.rate/10)
    def admit(self, client_id):
        if self.tokens>=1: self.tokens-=1; return True
        return False
def run(limiter, seconds=120, seed=11):
    rng=random.Random(seed)
    sent={c:0 for c in range(8)}; ok={c:0 for c in range(8)}
    for s in range(seconds):
        for _ in range(10):  # 10 ticks/sec
            limiter.tick() if hasattr(limiter,'tick') else None
            reqs=[]
            for c in range(3): reqs += [c]*8          # heavy: 8 per tick
            for c in range(3,8):
                if rng.random()<0.02: reqs += [c]*20   # light: rare bursts of 20
            rng.shuffle(reqs)
            for c in reqs:
                sent[c]+=1
                if limiter.admit(c): ok[c]+=1
    ratios=[ok[c]/sent[c] if sent[c] else 1 for c in range(8)]
    jain=sum(ratios)**2/(8*sum(r*r for r in ratios)) if any(ratios) else 0
    total=sum(ok.values())
    return {"jain":round(jain,3),"admitted":total,"ratios":[round(r,2) for r in ratios]}
if __name__=='__main__':
    print("baseline:", run(BaselineLimiter()))
