# Problem
We can only afford to ship 5% of events.log to the central store, but every
ERROR must arrive, and WARN statistics (count, ms distribution) must stay
estimable within +-10%. INVENT a sampling scheme, implement it, and verify on
the generated log (gen.py): output <=5% of lines, 100% of ERRORs present,
WARN count and ms-median reconstruction within +-10% of truth (show the math
— sampled WARNs must carry whatever weight info reconstruction needs).
Pattern B; numbers + repro.
