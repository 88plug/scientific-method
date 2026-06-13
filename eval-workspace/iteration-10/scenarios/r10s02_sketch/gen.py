import random
rng=random.Random(22)
with open("stream.txt","w") as f:
    for i in range(800000):
        v=rng.lognormvariate(3.0,0.6) if rng.random()>0.01 else rng.uniform(800,2000)
        f.write(f"{v:.3f}\n")
print("ok")
