# Problem
Storage cost for telemetry.csv (gen.py) is too high. gzip -6 is the current
baseline — measure it. INVENT a lossless scheme achieving a compressed size
at most HALF of gzip's on this corpus (i.e. >=2x better than gzip), with a
verified byte-identical round-trip. Pattern B: ideate, refute, implement,
measure. Report all numbers + repro.
