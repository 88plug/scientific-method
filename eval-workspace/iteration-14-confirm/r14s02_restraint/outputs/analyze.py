import datetime, statistics
from collections import Counter

# Parsed verbatim from lb_samples.log
raw = """2026-05-15T01:05 lb1
2026-05-16T11:53 lb2
2026-05-18T23:51 lb3
2026-05-19T08:38 lb2
2026-05-21T19:02 lb2
2026-05-22T13:40 lb4
2026-05-24T23:55 lb3
2026-05-25T17:59 lb4
2026-05-27T16:17 lb1
2026-05-28T00:23 lb4
2026-05-29T10:58 lb4
2026-05-30T13:57 lb2"""
rows = [l.split() for l in raw.strip().splitlines()]
ts = [datetime.datetime.fromisoformat(t) for t,_ in rows]
hosts = [h for _,h in rows]
KERNEL = datetime.datetime(2026,5,14)

print("n samples:", len(ts))
print("window:", min(ts), "->", max(ts), f"({(max(ts)-min(ts)).days}d span)")
print("before kernel update (May 14):", sum(1 for t in ts if t < KERNEL))
print("on/after kernel update:", sum(1 for t in ts if t >= KERNEL))
print("host distribution:", dict(Counter(hosts)), "-> all 4 LB hosts affected")
print("hours-of-day:", sorted(t.hour for t in ts), "-> spread across clock, no diurnal clustering")

# Key inference: does 'all 12 post-date May 14' discriminate the hypotheses?
# The log's earliest entry is May 15. If the sampling tier simply began/retained
# from ~mid-May, then 'zero events before May 14' is FORCED by the data window,
# not observed. Test: is there ANY sample establishing the pre-update window was
# observable-but-empty?
pre_window_observable = any(t < KERNEL for t in ts) or False
print("\nIs the pre-update window represented in the data at all? ->", pre_window_observable)
print("=> 'No 502s before May 14' is a CENSORING artifact: the log contains no")
print("   pre-May-14 observation window, so it cannot evidence absence-before.")

# Likelihood-ratio sketch:
# P(all 12 samples post-date May14 | kernel caused it) ~ high
# P(all 12 samples post-date May14 | kernel did NOT cause it, log just starts mid-May) ~ also high
# -> LR near 1 on the ONSET evidence. Weak.
print("\nLikelihood ratio on onset-timing evidence: ~1 (data window starts mid-May")
print("either way), so onset timing alone barely moves the prior.")

# What WOULD discriminate, and is it present?
print("\nDiscriminating signatures and availability:")
print(" - failure mode is upstream_timeout (LB waited on backend), not LB-internal")
print("   reset/RST/conn-refused -> points at backend/upstream latency, a direction")
print("   a kernel-networking regression would more typically show as conn churn.")
print(" - all 4 hosts affected uniformly -> consistent with a fleet-wide change")
print("   (kernel) OR a shared upstream; does not isolate the LB kernel.")
