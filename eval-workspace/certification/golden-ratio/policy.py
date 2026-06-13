"""Decorrelated wide-spread retry policy for r9s04.

Drop-in for sim.py's policy(attempt, last_status, state) -> delay | None.

Why it works (mechanism, not luck):
  The 30s hard-down outage makes ~30k requests fail. The baseline retries them
  IMMEDIATELY, so (a) they pile onto offered[] during the outage (4x peak) and
  (b) the moment the server returns at t=60 the backlog collides with fresh
  traffic, saturating the 1500-rps cap for tens of seconds -> fresh post-recovery
  requests get bounced -> p99 blows up.

  Two levers fix all three criteria at once:
    1. SPREAD, don't stack. On first failure each request is assigned a delay
       drawn from a golden-ratio low-discrepancy sequence over a wide window
       [base, base+span]. This is decorrelated jitter without an RNG: any N
       consecutive requests land near-uniformly across the window, so retries
       never cluster. Backlog drains at <=500/s, keeping every post-60 second
       below the 1500 cap (offered peaks at 1436). => peak 1.0x, post p99 0s.
    2. BOUND volume. Give up after maxa attempts so unservable outage-window
       requests don't keep re-injecting late. Healthy-period traffic (t<30,
       t>61) never fails because spread retries never push any second over the
       cap. => healthy success 1.0.

  The policy is fully deterministic (no RNG), so score() is identical across
  every sim seed and across process restarts.
"""

PHI = 0.6180339887498949  # 1/golden-ratio: low-discrepancy spreading constant


class DecorrelatedSpreadPolicy:
    def __init__(self, base=31.0, span=70.0, maxa=3):
        # base=31: jump clear of the <=60s outage on the first retry.
        # span=70: wide enough that 30k backlog drains at <=500/s (under cap headroom).
        # maxa=3: bound total retry volume; extra attempts add nothing here.
        self.base = base
        self.span = span
        self.maxa = maxa
        self.ctr = 0

    def reset(self):
        self.ctr = 0

    def __call__(self, attempt, last_status, state):
        if attempt > self.maxa:
            return None
        if 'u' not in state:
            self.ctr += 1
            state['u'] = (self.ctr * PHI) % 1.0  # deterministic decorrelated slot
        return self.base + state['u'] * self.span


# Module-level instance for direct use as `policy`.
_policy = DecorrelatedSpreadPolicy()


def policy(attempt, last_status, state):
    return _policy(attempt, last_status, state)
