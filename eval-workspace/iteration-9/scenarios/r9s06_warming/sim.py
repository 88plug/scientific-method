"""Cold-start cache warming. At t=0 the cache (cap 300) is empty; you may
PREWARM exactly 50 keys chosen from history.txt (yesterday's access log).
Today's trace (today.txt, generated with a different seed but same process)
then plays. Baseline prewarm: the 50 most-recent keys from history.
Acceptance: first-10k-access hit rate >= 1.25x baseline's.
score(prewarm_keys) prints hit rates."""
import random, collections
def make(seed,n=60000):
    rng=random.Random(seed); hot=[rng.randint(0,400) for _ in range(40)]
    out=[]
    for i in range(n):
        r=rng.random()
        if r<0.6: out.append(rng.choice(hot))
        elif r<0.8: out.append(rng.randint(0,400))
        else: out.append(rng.randint(400,8000))
    return out
def score(prewarm):
    today=make(16)
    cache=collections.OrderedDict((k,1) for k in list(prewarm)[:50])
    hits=0
    for j,k in enumerate(today[:10000]):
        if k in cache: hits+=1; cache.move_to_end(k)
        else:
            if len(cache)>=300: cache.popitem(last=False)
            cache[k]=1
    return hits/10000
if __name__=='__main__':
    hist=make(15)
    open('history.txt','w').write('\n'.join(map(str,hist)))
    recent=list(dict.fromkeys(reversed(hist)))[:50]
    print("baseline (50 most recent):", score(recent))
