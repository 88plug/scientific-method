# Review comment on PR #212
Senior dev wrote: "Keep the naive linear scan for the hot path — with our
access pattern (list mutated between every lookup, n≈50) the linear scan is
FASTER than the dict-index version. Do not 'optimize' it."
A new grad calls this "obviously wrong, linear scan is O(n)". Settle it with
data — the two files reproduce the prod access pattern exactly.
