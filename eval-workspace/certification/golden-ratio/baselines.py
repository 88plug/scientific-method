"""Competing policies for the fair-comparison gate.

GoldenFactory : the submission's policy, re-instantiated fresh per run.
JitterFactory : a WELL-TUNED random decorrelated-jitter baseline -- the AWS
                "Exponential Backoff and Jitter" decorrelated-jitter recipe:
                    sleep = min(cap_delay, random_between(base, prev*3))
                widened here to the SAME [base..base+span] envelope as the
                golden policy so the comparison is apples-to-apples (same window,
                same attempt bound). The ONLY difference under test is
                deterministic LDS spreading vs RNG draws.

Both factories take the sim's rng so the jitter baseline shares the sim seed
stream (this is what makes it seed-sensitive, the property under test).
"""
import math

PHI = 0.6180339887498949


def GoldenFactory(base=31.0, span=70.0, maxa=3):
    def make(rng):
        ctr = [0]
        def policy(attempt, last_status, state):
            if attempt > maxa:
                return None
            if 'u' not in state:
                ctr[0] += 1
                state['u'] = (ctr[0] * PHI) % 1.0
            return base + state['u'] * span
        return policy
    return make


def JitterFactory(base=31.0, span=70.0, maxa=3):
    """Decorrelated jitter: first retry uniformly random in [base, base+span].
    Same envelope/attempt bound as golden; spread is RNG instead of LDS."""
    def make(rng):
        def policy(attempt, last_status, state):
            if attempt > maxa:
                return None
            if 'u' not in state:
                state['u'] = rng.random()
            return base + state['u'] * span
        return policy
    return make
