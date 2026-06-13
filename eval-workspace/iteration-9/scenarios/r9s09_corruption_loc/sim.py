"""5000 blocks of 4KB. One write-time corruption event flips a burst inside
one block (unknown which). You may READ blocks (cost 1 each) and you hold
any precomputed per-block/aggregate metadata you designed at WRITE time
(its storage cost must be <=2% of corpus size; state it).
Goal: localize the corrupt block exactly.
Acceptance: expected reads to localize <= 30 (vs 2500 naive scan average),
metadata overhead <= 2%. corrupt() injects; your detector must find i.
"""
import random, hashlib
def make_corpus(seed=5, n=5000, block=4096):
    rng=random.Random(seed)
    return [bytes(rng.getrandbits(8) for _ in range(64))*64 for _ in range(n)]
def corrupt(corpus, seed=None):
    rng=random.Random(seed)
    c=list(corpus); i=rng.randrange(len(c)); b=bytearray(c[i])
    st=rng.randrange(0,len(b)-512)
    for j in range(st,st+rng.randrange(64,512)): b[j]^=0xFF
    c[i]=bytes(b); return c, i
