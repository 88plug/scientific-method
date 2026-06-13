"""Two event streams (orders, payments) arrive interleaved with skew:
a payment matches an order_id seen up to 60s earlier (95%) or up to 600s
earlier (5% stragglers). 500k orders. Join them single-pass with <=5MB
state (accounted): emit (order, payment) pairs.
Acceptance: >=99.5% of true joinable pairs emitted, zero false joins,
state <=5MB. Baseline: keep-everything join = ~50MB. gen() yields the
interleaved stream with truth labels for scoring.
"""
import random
def gen(seed=128, n=500000):
    rng=random.Random(seed); pending=[]; out=[]
    oid=0; t=0.0
    events=[]
    for i in range(n):
        t+=rng.uniform(0.5,1.5)
        events.append(('order',oid,t)); 
        lag = rng.uniform(0,60) if rng.random()<0.95 else rng.uniform(60,600)
        events.append(('payment',oid,t+lag))
        oid+=1
    events.sort(key=lambda e:e[2])
    return events
