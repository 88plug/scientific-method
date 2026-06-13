# Invention brief
A stream of ~2M item-ids/day must be deduplicated with at most ~1MB of
memory; small false-positive rate acceptable (drop a few uniques), false
negatives (passing a duplicate) must be <0.5%. INVENT approaches, refute,
implement the best, and measure FP/FN rates + memory on the generator below.
gen_stream.py yields (id, is_duplicate_truth) pairs for scoring.
Be explicit about which parts of your design are known prior art.
