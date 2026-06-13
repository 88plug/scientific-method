import random, hashlib
def make_corpus(n_blocks=5000, block=4096, seed=5):
    rng=random.Random(seed)
    return [bytes(rng.getrandbits(8) for _ in range(64))*64 for _ in range(n_blocks)]
def corrupt(corpus, seed=6):
    rng=random.Random(seed); c=list(corpus)
    i=rng.randrange(len(c)); b=bytearray(c[i])
    start=rng.randrange(0,len(b)-512)
    for j in range(start,start+rng.randrange(64,512)): b[j]^=0xFF
    c[i]=bytes(b); return c, i
