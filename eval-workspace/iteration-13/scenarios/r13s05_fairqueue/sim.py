"""Multi-tenant queue sim. 6 tenants; capacity 100 jobs/s total; memory cap
2,000 queued jobs. Tenant arrival mix: two heavy (60/s each), three medium
(15/s), one whale-burst tenant (0/s baseline, 500/s bursts of 10s every
120s). Your queue decides: enqueue-or-reject(tenant, t) and dequeue()->job.
Acceptance (all simultaneously, 600s, >=3 seeds):
  - weighted fairness: served shares within +-10% of equal shares for
    backlogged tenants (Jain >= 0.95 over served-per-backlogged-tenant)
  - memory cap never exceeded
  - whale bursts never reduce any other tenant's served rate by >5%
    vs a no-whale control run
  - total throughput >= 97 jobs/s when backlog exists
score(queue_factory) reports all four.
"""
import random, collections
def score(qf, seed=135, whale=True):
    rng=random.Random(seed); q=qf()
    rates={0:60,1:60,2:15,3:15,4:15,5:0}
    served=collections.Counter(); backlogged=set(); mem_ok=True; total=0
    for s in range(600):
        for ten,r in rates.items():
            rr = r + (500 if (whale and ten==5 and s%120<10) else 0)
            for _ in range(rr):
                q.offer(ten, s)
        if q.size()>2000: mem_ok=False
        for _ in range(100):
            j=q.take()
            if j is None: break
            served[j]+=1; total+=1
    return {"served":dict(served),"mem_ok":mem_ok,"throughput":total/600}
