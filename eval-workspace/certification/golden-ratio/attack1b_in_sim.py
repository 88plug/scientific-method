"""ATTACK 1b — confirm the kill INSIDE the submission's own sim harness.

The submission scores ONE shared module-level _policy instance, so its
self.ctr increments globally across all 120k requests = god's-eye spread.
We change exactly one thing to reflect independent clients: give each
request its OWN policy instance (a real client only knows its own state).
Everything else (sim.py) is byte-identical and unmodified.

We compare:
  - submission_shared : the original (one shared instance) -> their numbers
  - independent_det   : per-request fresh instance, deterministic-by-attempt
  - independent_rand  : per-request fresh instance, per-client random jitter
"""
import sys, random
sys.path.insert(0, "/home/andrew/scientific-method-plugin/eval-workspace/iteration-9/r9s04/with_skill/outputs")
import sim
from policy import DecorrelatedSpreadPolicy, PHI

# --- the submission as-shipped: one global instance, shared ctr ---
shared = DecorrelatedSpreadPolicy(31.0, 70.0, 3)
shared.reset()
print("submission_shared (god's-eye global ctr):", sim.score(shared))

# --- independent clients, deterministic by attempt (no shared state) ---
def independent_det(attempt, last, state):
    if attempt > 3:
        return None
    if 'u' not in state:
        state['u'] = (attempt * PHI) % 1.0   # client only knows its own attempt
    return 31.0 + state['u'] * 70.0
print("independent_det  (per-client, by attempt):", sim.score(independent_det))

# --- independent clients, per-client random jitter (the 'inferior' baseline) ---
def independent_rand(attempt, last, state):
    if attempt > 3:
        return None
    if 'u' not in state:
        state['u'] = state.get('_rng', random).random()
    return 31.0 + state['u'] * 70.0
# sim creates state={} per request, so seed a per-request rng deterministically:
def independent_rand2(attempt, last, state):
    if attempt > 3:
        return None
    if 'rng' not in state:
        state['rng'] = random.Random()  # entropy-seeded per client = real jitter
        state['u'] = state['rng'].random()
    return 31.0 + state['u'] * 70.0
print("independent_rand (per-client jitter)     :", sim.score(independent_rand2))
