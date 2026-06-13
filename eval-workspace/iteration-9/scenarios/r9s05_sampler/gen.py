import random
rng=random.Random(14)
with open("events.log","w") as f:
    for i in range(500000):
        r=rng.random()
        if r<0.001: f.write(f"e{i} ERROR payment_failed code={rng.randint(500,599)}\n")
        elif r<0.004: f.write(f"e{i} WARN slow_query ms={rng.randint(200,900)}\n")
        else: f.write(f"e{i} INFO ok ms={rng.randint(1,50)}\n")
print("ok")
