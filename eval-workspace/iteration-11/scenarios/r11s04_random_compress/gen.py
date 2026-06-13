import random
rng=random.Random(44)
open("payload.bin","wb").write(bytes(rng.getrandbits(8) for _ in range(2_000_000)))
print("ok")
