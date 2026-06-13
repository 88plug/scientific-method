import random
rng=random.Random(126)
with open("stream.txt","w") as f:
    # 1M items; true heavy hitters shift every 200k; adversarial near-ties
    hh=[f"hh{i}" for i in range(10)]
    for seg in range(5):
        for i in range(200000):
            r=rng.random()
            if r<0.4: f.write(rng.choice(hh)+"\n")
            elif r<0.6: f.write(f"mid{rng.randint(0,99)}\n")
            else: f.write(f"tail{rng.getrandbits(24)}\n")
        hh=[f"hh{seg+1}_{i}" for i in range(10)]
print("ok")
