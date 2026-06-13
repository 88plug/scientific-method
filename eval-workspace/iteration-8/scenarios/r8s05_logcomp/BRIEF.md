# Invention brief
app.log is highly repetitive telemetry. Baseline: gzip -6 ratio (measure it).
Invent at least 4 schemes that beat gzip on THIS corpus (any combination of
modeling + an off-the-shelf entropy stage is allowed; decompression must be
lossless — verify round-trip). Refute, implement the best, measure ratio and
round-trip fidelity. Partition known vs novel honestly.

> Note: `app.log` (4.3 MB) is a git-ignored fixture — rebuild it deterministically
> with `python3 gen_app_log.py` before running this scenario.
