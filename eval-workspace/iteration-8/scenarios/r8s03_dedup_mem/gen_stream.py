import random
def stream(n=200000, dup_rate=0.2, seed=3):
    rng=random.Random(seed); seen=[]
    for i in range(n):
        if seen and rng.random()<dup_rate:
            yield rng.choice(seen), True
        else:
            x=f"id-{rng.getrandbits(48):012x}"; seen.append(x)
            if len(seen)>50000: seen.pop(0)
            yield x, False
