sandbox bench (constant 2k rps, single service, no mem caps), n=10:
static pool: p99 = 480ms (spikes present)
dynamic pool: p99 = 95ms (spikes eliminated)
medians stable, spread +/-4%. Methodology clean.
