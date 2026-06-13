# Invention brief (design only — no sandbox)
CI runs 12k tests/commit; ~40 are flaky at any time; current detection is
"humans notice". Re-running everything 3x is too expensive (3x compute).
Invent at least 5 detection/quarantine schemes that cost <15% extra compute.
For each: mechanism, expected detection latency, failure modes, and a
pre-committed outcome table for the experiment that would validate it. Refute
each; rank survivors. No implementation required — the DESIGNS and their
experiments are the deliverable.
