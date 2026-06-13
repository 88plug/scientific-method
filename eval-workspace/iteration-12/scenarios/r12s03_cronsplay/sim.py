"""Scheduled-job thundering herd. 2,000 tenants each run a 'nightly' job;
naive: all fire at 02:00:00 -> the shared API melts (capacity 50 jobs/s;
queueing beyond that). You control each tenant's offset assignment
offset(tenant_id) -> seconds in [0, 3600) (assigned once, no coordination
at runtime; tenants may join/leave daily — assignment must stay stable
per-tenant and well-spread under churn).
Baseline: random hash splay (offset = hash(tenant) % 3600).
Acceptance: with 30% daily tenant churn over 30 simulated days,
worst-second load <= 2.2x the ideal mean on EVERY day (random splay's
worst-second is typically ~3-4x ideal due to birthday clustering),
measured by score(offset_fn).
"""
import random, hashlib, collections
def score(offset_fn, days=30, seed=123):
    rng=random.Random(seed)
    tenants=set(range(2000)); next_id=2000; worst=[]
    for d in range(days):
        churn=int(len(tenants)*0.30)
        gone=rng.sample(sorted(tenants),churn)
        for g in gone: tenants.discard(g)
        for _ in range(churn): tenants.add(next_id); next_id+=1
        buckets=collections.Counter(int(offset_fn(t))%3600 for t in tenants)
        ideal=len(tenants)/3600
        worst.append(max(buckets.values())/ideal)
    return {"worst_second_ratio_max":round(max(worst),2),"mean":round(sum(worst)/len(worst),2)}
def baseline(t):
    return int(hashlib.sha256(str(t).encode()).hexdigest(),16)%3600
if __name__=='__main__': print("baseline:",score(baseline))
