import random
random.seed(7)
with open("corpus.txt","w") as f:
    for i in range(2_000_000): f.write(f"  line-{random.randint(0,9999)}-payload  \n")
print("ok")
