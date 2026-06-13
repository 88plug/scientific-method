"""Cache with heterogeneous miss costs. Keys have sizes (1) but different
re-fetch costs (provided per key: 1, 10, or 100 — e.g. local/regional/origin).
policy(key, cache_dict, cost) -> key_to_evict. cap=200.
Baseline LRU. Acceptance: total miss COST <= 0.60x LRU's on the trace,
robust across >=5 seeds.
"""
import random, collections
def make(seed=121, n=60000):
    rng=random.Random(seed)
    cost={}; tr=[]
    hot=list(range(60))
    for i in range(n):
        r=rng.random()
        k = rng.choice(hot) if r<0.55 else (rng.randint(60,600) if r<0.8 else rng.randint(600,8000))
        if k not in cost: cost[k]=rng.choice([1,1,10,10,100])
        tr.append(k)
    return tr,cost
def score(policy, seed=121):
    tr,cost=make(seed); cache=collections.OrderedDict(); miss_cost=0
    for k in tr:
        if k in cache: cache.move_to_end(k); continue
        miss_cost+=cost[k]
        if len(cache)>=200:
            ev=policy(k,cache,cost); cache.pop(ev)
        cache[k]=1
    return miss_cost
def lru(k,cache,cost): return next(iter(cache))
if __name__=='__main__': print("LRU miss cost:", score(lru))
