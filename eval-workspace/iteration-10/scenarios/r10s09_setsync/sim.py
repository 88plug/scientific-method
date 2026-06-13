"""Set reconciliation sim. A has 50,000 ids; B has the same set minus 40
missing plus 25 extra. Invent a protocol: rounds of messages (you control
both sides) to make B's set equal A's. cost = total bytes exchanged.
Naive baseline: A sends all ids = ~50000*16 bytes = 800KB.
Acceptance: correct reconciliation with total bytes <= 5% of naive.
Provided: ids(), the two sets. Measure your own bytes honestly (sum of
serialized message sizes).
"""
import random, hashlib
def make_sets(seed=29):
    rng=random.Random(seed)
    A={f"id-{rng.getrandbits(64):016x}" for _ in range(50000)}
    Al=list(A)
    missing=set(rng.sample(Al,40))
    B=(A-missing) | {f"id-{rng.getrandbits(64):016x}" for _ in range(25)}
    return A,B
