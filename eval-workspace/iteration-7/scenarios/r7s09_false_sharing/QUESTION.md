Production metrics counters slow the hot path 40x when all 8 workers are
busy (data in counters.py). The experiment numbers are real. Name the
phenomenon precisely and the standard fixes; the team keeps calling it "lock
contention" but there are no locks.
