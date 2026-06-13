# Problem
Design + implement the write-time metadata and read-time search that localizes
the corrupt block within the budgets in sim.py (reads <= 30 expected, metadata
<= 2%). Verify over >=20 random corruption trials (different seeds): 100%
localization, mean reads reported. Pattern B; numbers + repro.
