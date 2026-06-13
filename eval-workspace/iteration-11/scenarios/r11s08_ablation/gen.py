import random
rng=random.Random(48)
with open("queries.txt","w") as f:
    words=["alpha","beta","gamma","delta","epsilon","zeta","eta","theta"]
    for i in range(200000):
        f.write(" ".join(rng.choices(words, k=rng.randint(2,6)))+"\n")
print("ok")
