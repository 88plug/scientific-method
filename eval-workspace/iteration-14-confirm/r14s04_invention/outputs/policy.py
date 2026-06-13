"""Invented client retry policy for the retry-amplification sim.

Mechanism (Pattern B — separate-in-condition + decorrelate):
  Two falsifiable failure modes are distinguished by last_status:
    * "down"     -> server is hard-down (outage). A retry issued now cannot
                    succeed until t>=60, so back off LONG with WIDE jitter:
                    uniform(3, 75) seconds. This (a) pushes nearly every retry
                    of an outage-issued request past the 30s outage window so it
                    never amplifies the outage buckets, and (b) spreads the
                    30k-request outage backlog thinly across the whole recovery
                    window instead of slamming t=60 (no thundering herd).
    * "overload" -> server is UP but the per-second 1500-rps bucket is full
                    (transient contention, including post-recovery backlog drain).
                    Retry SOON with SMALL jitter: uniform(0.3, 1.2) seconds, so a
                    fresh post-recovery request resolves within ~1.5s (p99<=2s)
                    while still being decorrelated from its neighbors.

  Jitter (not fixed backoff) is load-bearing: fixed delays synchronize every
  retry onto the same integer second buckets and re-collide (ablation: no-jitter
  -> p99=15s, healthy=96%). The down/overload split is load-bearing: a single
  long backoff for both states makes post-recovery p99 a horizon artifact
  (mass give-up) rather than genuine fast service.

  give_up after 40 attempts (effectively unreached in healthy/recovery traffic;
  acts only as a final bound on stuck outage requests).

  state is fresh per request in this sim, so the policy is memoryless across
  requests by construction; all coordination is achieved statistically via jitter.

Provenance:
  - decorrelated/jittered exponential backoff to avoid retry thundering herd:
    KNOWN prior art (AWS Architecture Blog, "Exponential Backoff And Jitter",
    Marc Brooker, 2015). Used as a named building block.
  - splitting retry aggressiveness on a down-vs-overload signal and using a
    long jittered backoff sized to exceed a known outage horizon to convert
    in-outage retries into spread post-recovery load: NO-PRIOR-ART-FOUND for
    this exact combination tuned to the three acceptance criteria (not searched
    exhaustively; combination of two known ideas).
"""
import random

# Module-level RNG so the policy is a pure (attempt,last,state)->delay function.
# Seed is fixed for reproducibility; results are robust across seeds (see VERDICT.md).
_R = random.Random(12345)


def policy(attempt, last_status, state):
    if attempt > 40:
        return None  # give up (final bound; unreached by healthy/recovery traffic)
    if last_status == "down":
        return _R.uniform(3.0, 75.0)   # long, wide jitter: clear the outage window
    return _R.uniform(0.3, 1.2)        # overload: retry soon, small jitter
