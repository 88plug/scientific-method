# Duplicate IDs (3 incidents this quarter)
IDs are generated as: milliseconds-since-epoch (from system clock) appended
with a 4-bit counter. Duplicates appeared exactly when ops ran `ntpdate -b`
(step mode) to fix drifted clocks — time jumped BACKWARD ~800ms on some hosts.
Propose the fix; we cannot accept duplicate IDs, ever.
