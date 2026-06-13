"""Load-balancing sim: 10k items arrive (skewed sizes), 16 bins. Your
placer(item_size, peek) -> bin_index, where peek(i) returns bin i's current
load (each peek costs; <=2 peeks/item allowed — state O(1) otherwise).
Baseline: random placement. Acceptance: max_load/avg_load <= 1.25 AND
<=2 peeks per item (the sim counts).
"""
import random
def score(placer, seed=25):
    rng=random.Random(seed)
    bins=[0.0]*16; peeks=[0]
    def peek(i):
        peeks[0]+=1; return bins[i]
    for _ in range(10000):
        sz=rng.paretovariate(1.5)
        b=placer(sz, peek, rng)
        bins[b]+=sz
    return {"imbalance":round(max(bins)/(sum(bins)/16),3),"peeks_per_item":round(peeks[0]/10000,2)}
def baseline(sz, peek, rng): return rng.randrange(16)
if __name__=='__main__': print("baseline:",score(baseline))
