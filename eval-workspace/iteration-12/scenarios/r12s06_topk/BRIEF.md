# Open invention brief (full pipeline + §8)
Single pass over stream.txt (gen.py), <=200KB state (accounted): report the
top-10 most frequent items of the FINAL 200k-item segment (the heavy-hitter
set shifts every 200k). Acceptance: >=9/10 of the true final-segment top-10
identified (compute truth exactly for scoring), state accounted, single pass.
The drift is the hard part — global counters remember dead segments.
Quota/refute/build/measure; LIVE provenance (heavy-hitter sketches are
famous; recency-aware variants exist — find both); chart; rung; disclosure;
§8 ranking.
