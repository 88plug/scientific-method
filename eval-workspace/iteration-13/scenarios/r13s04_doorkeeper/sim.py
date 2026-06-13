"""Admission control sim. LRU cache cap=500. Trace mixes zipf working set
(alpha=0.9 over 5k keys) with periodic full scans (50k one-shot keys).
admit(key, hint_state)->bool decides if a MISSED key may enter the cache;
your persistent hint state is capped at 64 KILOBITS total (8KB) — account
it. Baselines: admit-all LRU; admit-all 2Q.
Acceptance: hit rate >= 1.30x admit-all LRU on the mixed trace, >=3 seeds,
state accounting verified.
"""
import random, collections
def make(seed=134,n=200000):
    rng=random.Random(seed); tr=[]
    zipf=[int(5000*(rng.random()**(1/0.1)))%5000 for _ in range(n)]  # rough zipf-ish
    i=0
    for j in range(n):
        if j%20000<2000: tr.append(100000+j)   # scan burst
        else: tr.append(zipf[i]); i+=1
    return tr
def score(admit, seed=134):
    tr=make(seed); cache=collections.OrderedDict(); hits=0
    for k in tr:
        if k in cache: hits+=1; cache.move_to_end(k); continue
        if admit(k):
            if len(cache)>=500: cache.popitem(last=False)
            cache[k]=1
    return hits/len(tr)
if __name__=='__main__':
    print("admit-all LRU:", round(score(lambda k: True),4))
