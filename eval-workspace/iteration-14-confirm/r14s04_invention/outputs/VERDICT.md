# VERDICT — Invented client retry policy (r14s04)

**Status: CONFIRMED (prototype).** An invented client retry policy meets all
three acceptance criteria from `sim.py`, with margin, and is robust across 40
jitter seeds and 30 sim seeds (0 failures). Confidence **0.93** — direct,
reproduced-on-demand simulator measurement; residual is that "robustness" is
in-model only (the policy is tuned to this sim's 30s-outage horizon; see
Refutation §R3).

## Acceptance criteria (from sim.py docstring)

| # | Criterion | Threshold | Baseline | Invention | Pass |
|---|---|---|---|---|---|
| C1 | Peak offered load during outage | ≤ 2.0× | **4.0×** | **1.42×** | ✅ |
| C2 | p99 time-to-success, requests issued after recovery (t>60) | ≤ 2s | 0s* | **1.48s** | ✅ |
| C3 | Success ratio during healthy periods | ≥ 99.5% | 100% | **100%** | ✅ |

\* Baseline's p99=0 is not a win: it passes C2/C3 only because immediate-retry
requests issued during the outage **give up** (3 retries, all at the same
instant) rather than waiting, so they never create post-recovery backlog. The
baseline fails **only C1** (4.0× amplification). The invention had to cut
amplification in half-and-then-some without re-introducing post-recovery
congestion.

## The invention (Pattern B: separate-in-condition + decorrelate)

`policy(attempt, last_status, state)` branches on the failure signal:

- **`last_status == "down"`** (server hard-down): `delay = uniform(3, 75)` s.
  Long + wide jitter. Two effects: (a) the first retry of an outage-issued
  request almost always lands at t ≥ 60, so it never amplifies the outage-second
  buckets; (b) the 30k-request outage backlog is spread *thinly* across the whole
  recovery window instead of slamming t=60 (no thundering herd at recovery).
- **`last_status == "overload"`** (server UP, 1500-rps bucket full — transient
  contention / backlog drain): `delay = uniform(0.3, 1.2)` s. Retry soon with
  small jitter, so a fresh post-recovery request resolves within ~1.5 s (C2)
  while staying decorrelated from its neighbors.
- Give up after 40 attempts (a final bound; unreached by healthy/recovery
  traffic — 0/59000 post-recovery give-ups).

Why this shape and not plainer ones (measured, in `repro.py`):

- Plain capped exponential backoff (no jitter): **5.0×** amplification — fixed
  delays synchronize retries onto identical integer buckets.
- Decorrelated jitter without the down/overload split: **6.3×** — short retries
  during a 30s outage just refill the outage buckets.
- The split + long down-backoff is what converts in-outage retries into spread
  post-recovery load; jitter is what keeps them from re-colliding.

## Refutation pass (tried to kill the finding)

- **R1 — Is jitter actually load-bearing, or decoration?** ABLATION: split-only,
  fixed delays → amp 1.0 but **p99=15s, healthy=96%** (FAIL). Synchronized
  retries thunder-herd into the same buckets and re-fail. Jitter survives as
  necessary. ✅ load-bearing.
- **R2 — Is the down/overload split load-bearing?** ABLATION: jitter-only, long
  backoff for both states → **p99 passes only via mass give-up past the t=120
  horizon**, not via genuine fast service. The split is what makes p99 real. ✅
  load-bearing.
- **R3 — Is C2's pass a horizon artifact (requests give up past t=120 instead of
  succeeding slowly)?** HONEST ACCOUNTING: **0 / 59000** post-recovery-issued
  requests give up; the 1.48s p99 is from genuine successes. Total give-up is
  **1.66%**, *all* of it outage-issued (6.63% of the 30k requests that arrived
  during a hard-down window and could not have succeeded then anyway). This is an
  honest load-shed during the outage, not a metric exploit. Guardrail noted: a
  tighter no-give-up requirement would need a longer sim horizon or a higher
  attempt cap; the policy already keeps post-recovery give-ups at zero.
- **R4 — Overfit to one RNG draw / one seed?** Robust across **40 jitter seeds**
  (amp max 1.48, p99 max 1.749 — always ≤2.0, healthy always 100%, 0 fails) and
  **30 sim seeds** (0 fails). Not seed-luck.
- **R5 — Does it secretly still pay the baseline's cost?** No: peak outage bucket
  is 1419 req/s vs baseline's 4000; the amplification is genuinely halved-plus.

**Surviving caveat (residual):** the numeric constants (down upper bound 75 s,
overload window 0.3–1.2 s) are tuned to *this* sim's single 30 s outage with a
120 s horizon. In a real client the "down" backoff should be a jittered capped
exponential whose cap is sized to the expected outage / circuit-breaker timeout
rather than a hardcoded 75 s, and "overload" vs "down" should come from a real
signal (503/Retry-After vs connection failure). This is a prototype that proves
the mechanism in-model, not a drop-in production constant set. Hence verdict
**prototype**, confidence 0.93.

## Provenance

- Jittered/decorrelated backoff to avoid retry thundering herd — **KNOWN** prior
  art (AWS Architecture Blog, Marc Brooker, "Exponential Backoff And Jitter",
  2015). Used as a named building block.
- Splitting retry aggressiveness on a down-vs-overload signal + sizing the "down"
  jittered backoff to exceed the outage horizon so in-outage retries become
  spread post-recovery load, tuned to these three criteria —
  **NO-PRIOR-ART-FOUND** for this exact combination (combination of two known
  ideas; not an exhaustive search).

## Reproduce

Provenance header: inputs `sim.py` (sha256
`0f2c5dee94a71f96b3db3c085c1905d9a45a7a218d4071a3a1a71eafc21ce54d`),
`policy.py` (sha256
`e69915a2fd3cd987daac7868145a8f17fd825d01935ff2ccf2b50c59ccb49689`);
Python 3, stdlib only; date 2026-06-12.

```
cd <this outputs dir>
python3 repro.py     # prints baseline, invention, robustness sweeps, ablations, accounting
```

Expected headline:
```
baseline:  {'peak_amplification': 4.0,  'post_recovery_p99_s': 0,    'healthy_success': 1.0}
invention: {'peak_amplification': 1.42, 'post_recovery_p99_s': 1.48, 'healthy_success': 1.0}  -> PASS
```

Files: `policy.py` (the invention), `repro.py` (regenerates every number),
`sim.py` (copy of the scenario simulator).
