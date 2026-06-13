"""Torn-write sim. writer(records) -> bytes (your format). The sim truncates
the byte stream at a random point (a crash mid-write). reader(blob) must
return every COMPLETE record (exactly, in order) and never return a torn/
corrupt record. Acceptance over 200 random truncations:
  - zero corrupt/partial records returned
  - all records whose final byte was written are recovered
  - format overhead <= 12% over raw record bytes
"""
import random, os
def trial(writer, reader, seed):
    rng=random.Random(seed)
    recs=[os.urandom(rng.randint(20,400)) for _ in range(rng.randint(5,60))]
    blob=writer(recs)
    cut=rng.randint(0,len(blob))
    got=reader(blob[:cut])
    return recs, blob, cut, got
