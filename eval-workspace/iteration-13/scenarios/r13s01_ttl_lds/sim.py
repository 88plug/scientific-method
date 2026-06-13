"""Cache-expiry alignment sim. 5,000 hot keys are (re)written continuously;
each write assigns a TTL. With ttl=base (300s) exactly, expiries align with
write waves and the backend sees synchronized expiry storms.
assign_ttl(key, write_index) -> ttl_seconds in [240, 360] (deterministic
per (key,write_index) or randomized — your choice; no global state shared
between keys at runtime).
Baselines provided: fixed (300), uniform random jitter in [240,360].
Acceptance over the 2h sim, across 5 write-pattern seeds AND the
adversarial synchronized-write pattern (all keys written in the same
second after a "deploy"):
  - max expiries in any 1-second bucket <= 0.55x random jitter's max
  - mean refetch rate within 2% of random jitter's (no TTL inflation trick)
score(assign_ttl) reports both.
"""
import random, collections, hashlib
def score(assign_ttl, seed=131, sync_start=True):
    rng=random.Random(seed)
    expiry=collections.Counter(); refetches=0
    t0 = 0
    writes={k: t0 if sync_start else rng.uniform(0,300) for k in range(5000)}
    widx={k:0 for k in range(5000)}
    t=0
    events=[(writes[k],k) for k in writes]
    import heapq; heapq.heapify(events)
    end=7200
    while events:
        wt,k=heapq.heappop(events)
        if wt>end: break
        ttl=assign_ttl(k, widx[k])
        ttl=max(240,min(360,float(ttl)))
        exp=wt+ttl
        expiry[int(exp)]+=1; refetches+=1
        widx[k]+=1
        heapq.heappush(events,(exp,k))   # rewrite on expiry (cache-aside refill)
    return {"max_1s_expiries":max(expiry.values()),"refetches":refetches}
def fixed(k,i): return 300
def randj(k,i):
    return random.uniform(240,360)
if __name__=='__main__':
    print("fixed:",score(fixed)); print("random:",score(randj))
