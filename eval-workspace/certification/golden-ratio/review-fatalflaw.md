# Peer Review — FATAL FLAW lens

**Submission:** `DecorrelatedSpreadPolicy` — deterministic golden-ratio retry
timing, claimed to *provably avoid retry clustering during outage recovery,
beating random jitter*.
Artifacts: `eval-workspace/iteration-9/r9s04/with_skill/outputs/{policy.py,sim.py,repro.py,VERDICT.md}`.

---

SUMMARY: The policy assigns each retry a delay `base + ((ctr*PHI)%1)*span`
where `ctr` is a counter and `PHI=0.618…` (1/φ). The VERDICT claims this is
"decorrelated jitter without an RNG": deterministic, seed-invariant, and
strictly better than random jitter because a golden-ratio low-discrepancy
sequence "never clusters" (H5), where random jitter occasionally bunches and
caps healthy-success at ~0.997 (H4). All three acceptance criteria pass in
the sim with peak 1.0 / post-p99 0 / healthy 1.0. **Reproduced verbatim — the
numbers are real.** The question this lens asks is whether they mean what the
VERDICT says they mean.

LENS: fatal-flaw. I built four adversarial sims and re-ran the submission's
own `sim.py` with a one-line change. Executed:
`attack1_cross_client.py`, `attack1b_in_sim.py`, `attack234.py` (all in this
dir). I also verified the prior-art collision against AWS/Brooker 2015.

---

## THE KILL — cross-client synchronization (attack 1)

The entire low-discrepancy spread is produced by **`self.ctr`, a single
module-level counter incremented once per request across the whole sim**.
`sim.py` instantiates exactly one shared `_policy`, so all 120k requests draw
*distinct* slots `ctr*φ mod 1` → a perfect god's-eye sweep of the window.
That shared, globally-monotonic counter is the load-bearing trick — and **no
population of independent distributed clients can have it.** The claim is
explicitly "a *client* retry policy" beating "per-client random jitter," i.e.
the distributed-fleet regime.

I modeled the realistic regime: N=30,000 clients all fail at the same instant
(the outage) and each computes its own deterministic delay. Every plausible
per-client phasing an engineer would actually ship (`attack1_cross_client.py`):

| phasing scheme                                   | peak retries in one 1s bin | bins used |
|--------------------------------------------------|---------------------------:|----------:|
| Deterministic **by attempt number** (literal claim) | **30000** | 1 |
| Deterministic **per-client local counter** (clean clients) | **30000** | 1 |
| Submission's **shared global counter** (god's-eye, sim-only) | 430 | 70 |
| **Per-client random jitter** (the baseline it "beats") | 483 | 70 |

Independent clients running the deterministic policy land **every single
retry in one 1-second bin** — a 70× *worse* thundering herd than the random
jitter the submission claims to beat. The golden ratio decorrelates
*consecutive draws from one shared counter*; it does **nothing** to
decorrelate *different clients that share an attempt index*. They all compute
the identical number.

**Confirmed inside the submission's own harness** (`attack1b_in_sim.py`),
changing exactly one thing — each request gets its own policy instance, as a
real client would:

```
submission_shared (god's-eye global ctr) : peak 1.0, post_p99 0, healthy 1.0   ← their result
independent_det   (per-client by attempt): peak 1.0, post_p99 0, healthy 0.9091 ← FAILS (<0.995)
independent_rand  (per-client jitter)     : peak 1.0, post_p99 0, healthy 1.0   ← PASSES
```

The thesis inverts. With genuinely independent clients the **deterministic
policy fails the healthy-success criterion (0.909 ≪ 0.995)** while the
**per-client random jitter it claims to beat passes cleanly.** (Peak still
reads 1.0 only because `sim.py` hard-caps `offered≤1500` and *bounces* the
herd; the wave reappears as the healthy-success collapse and give-ups.)

## Secondary attacks (all confirm the same root cause)

- **(4) Correlated restart / state-loss** (`attack234.py`): a fleet that
  crash-loops together — common *during the very outage this targets* — all
  reset their counter and re-emit attempt 1 → **30000 retries in 1 bin, total
  synchronization.** Even the shared-counter version is non-durable: any
  counter reset re-collides.
- **(3) Quantization collapse**: rounding delays to a real timer grid caps
  distinct slots at `window/grid` regardless of φ. 1s grid → 71 slots; 2s →
  35; **5s → 15 slots, ≥2000 clients per slot.** Low-discrepancy over a
  continuum is meaningless once quantized to coarse ticks.
- **(2) Phase adversary**: `state['u']` is frozen on first failure, so a
  cohort forced to fail in lockstep replays one slot indefinitely — an
  adversary or unlucky topology that correlates failures defeats the spread by
  construction.

## The repair is the prior art it claims to beat

The minimal fix is a **per-client random phase offset**:
`delay = base + ((u0 + k*φ)%1)*span`, `u0~U(0,1)`. This restores the spread
(peak 478/70 bins, `attack234.py`). But the entropy doing all the work is the
*random* `u0` — the golden ratio is now decorative. This is **literally
per-client random jitter**, i.e. AWS / Marc Brooker, "Exponential Backoff and
Jitter" (2015) and the AWS Builders' Library "Timeouts, retries and backoff
with jitter," which states the governing principle outright: *"If all the
failed calls back off to the same time, they cause contention or overload
again when they are retried. Our solution is jitter [randomness]."* A
deterministic, RNG-free backoff is the exact anti-pattern jitter was invented
to cure. The submission's headline — "decorrelated jitter **without an RNG**"
— is a contradiction in terms; the decorrelation *is* the RNG.

---

STRENGTHS:
- In-sim numbers reproduce exactly; determinism/seed-invariance claims hold as stated.
- Mechanism for the *single-counter* sim is correctly diagnosed (H1–H3 are sound).
- Honest about give-up accounting.

WEAKNESSES:
- **[blocking]** The spread depends on a global shared counter that no
  independent-client deployment has. Under independent clients the policy
  synchronizes into a maximal herd (1 bin) and **fails healthy-success
  (0.909)** in the submission's own sim — the opposite of the claim.
- **[blocking]** Claim "beats random jitter" is falsified: random jitter
  passes where the deterministic policy fails. The win was an artifact of
  testing one god's-eye instance instead of a client population.
- **[blocking]** Prior-art collision: the only working version is per-client
  random jitter (AWS/Brooker 2015). "Decorrelated jitter without an RNG" is
  self-contradictory.
- **[non-blocking]** Non-durable to restart; collapses under timer
  quantization; defeated by correlated-failure phase adversary.
- **[non-blocking]** VERDICT confidence 0.97 with a residual that names only
  parameter-retuning — never the cross-client / shared-state assumption that
  actually governs the result.

QUESTIONS FOR AUTHORS:
1. What is the real-world analog of `self.ctr`? Show a distributed protocol
   by which independent clients obtain *distinct* counter values without
   coordination. (Probe: `attack1_cross_client.py`.)
2. Re-run `sim.py` with one policy instance **per request** (independent
   clients). Does healthy-success stay ≥0.995? (Probe: `attack1b_in_sim.py` —
   I get 0.9091.)
3. Once a per-client random phase offset is added to make it work, what does
   the golden ratio contribute that the random offset does not? How is the
   result distinct from AWS decorrelated/full jitter (2015)?

SCORES: soundness 2/5, provenance 1/5, reproducibility 5/5,
significance 1/5  *(fatal-flaw lens authoritative; maps to soundness/significance:
the central claim fails under the regime it targets)*

RECOMMENDATION: reject

REVIEWER CONFIDENCE: 0.9 — the kill is executed in the submission's own
harness with a single-line, well-motivated change and corroborated by an
independent sim and a named prior-art collision; residual uncertainty is only
whether the authors intended a coordinated-counter deployment, which the
"beats per-client random jitter" claim rules out.
