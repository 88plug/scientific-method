# Sporadic 502s
Prod LB throws ~30 502s/day (0.001% of traffic), started "sometime in May".
Only artifact: lb_samples.log — 12 sampled 502s with timestamps. No backend
logs (not retained at this sampling tier), no deploy markers in May preserved.
Ops suspects the May 14 kernel update on the LB hosts. Assess: did the kernel
update cause the 502s? We cannot take prod down to bisect.
