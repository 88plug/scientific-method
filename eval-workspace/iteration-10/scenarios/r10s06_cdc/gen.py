import random
rng=random.Random(26)
base=bytearray(rng.getrandbits(8) for _ in range(2_000_000))
open("backup_v1.bin","wb").write(bytes(base))
# v2: same data with 30 random small insertions (shifts everything after)
v2=bytearray(base)
for _ in range(30):
    pos=rng.randrange(len(v2)); ins=bytes(rng.getrandbits(8) for _ in range(rng.randint(3,40)))
    v2[pos:pos]=ins
open("backup_v2.bin","wb").write(bytes(v2))
print("ok")
