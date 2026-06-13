"""Cache policy sim, cap=50, trace below. score(policy) -> hit rate.
policy(key, cache_keys) -> key_to_evict (when full).
Belady's OPT (future-knowledge) on this trace: computed by opt() below.
"""
import random
def make_trace(seed=46, n=30000):
    rng=random.Random(seed); hot=list(range(30)); tr=[]
    for i in range(n):
        r=rng.random()
        if r<0.5: tr.append(rng.choice(hot))
        elif r<0.75: tr.append(rng.randint(30,300))
        else: tr.append(rng.randint(300,4000))
    return tr
def score(policy, trace=None):
    tr=trace or make_trace(); cache=set(); hits=0
    for i,k in enumerate(tr):
        if k in cache: hits+=1; continue
        if len(cache)>=50:
            cache.discard(policy(k, frozenset(cache)))
        cache.add(k)
    return hits/len(tr)
def opt(trace=None):
    tr=trace or make_trace(); cache=set(); hits=0
    for i,k in enumerate(tr):
        if k in cache: hits+=1; continue
        if len(cache)>=50:
            future={c: (tr[i+1:].index(c) if c in tr[i+1:] else 10**9) for c in cache}
            cache.discard(max(future,key=future.get))
        cache.add(k)
    return hits/len(tr)
if __name__=='__main__':
    print("OPT (clairvoyant):", round(opt(),4))
