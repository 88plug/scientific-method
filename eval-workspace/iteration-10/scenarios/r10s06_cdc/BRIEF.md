# Invention brief (full pipeline)
A backup system dedupes v2 against v1 with fixed 4KB blocks; insertions shift
all subsequent blocks so dedup collapses. Measure that baseline (shared bytes
found by fixed 4KB blocking between backup_v1.bin and backup_v2.bin from
gen.py), then invent a chunking scheme achieving >=10x the baseline's
deduplicated (shared) bytes. Claim grammar + chart + LIVE provenance search +
honest rung + disclosure.
