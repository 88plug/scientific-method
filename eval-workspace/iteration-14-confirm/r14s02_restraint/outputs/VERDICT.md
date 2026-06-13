# Did the May 14 kernel update cause the sporadic 502s?

**VERDICT: INCONCLUSIVE** — weak counter-lean against the kernel-update story.
**Confidence that the kernel update is the cause: ~0.40** (i.e. slightly below
even; the available evidence does not support the accusation and mildly points
elsewhere, but cannot exonerate it either). Causal-ladder rung reached:
**none above "post-change correlation that is itself censored"** — not even clean
temporality.

Evidence environment: `operational` data, but the decisive window is missing.

---

## Why not CONFIRMED

The only positive argument is "all 12 sampled 502s post-date the May 14 update."
That argument is **structurally void here**, because the sample log itself begins
**2026-05-15** and contains **zero observation window before May 14**:

- Samples before May 14: **0 of 12** — but not because the pre-update window was
  observed and found clean. It was **never sampled.** The earliest row is one day
  after the update.
- This is textbook **censoring**: "no 502s before the change" is *forced by the
  data window*, not *measured*. Absence-of-evidence here is an artifact of when
  the log starts, not evidence-of-absence.
- Likelihood ratio on the onset-timing evidence is **~1**: P(all samples post-date
  May 14 | kernel caused it) ≈ P(all samples post-date May 14 | log just starts
  mid-May regardless of cause). Evidence with LR≈1 does not move the prior.

The incident itself only claims onset "sometime in May" — vague, no precise step
at May 14. There is no deploy marker, no backend log, no pre-update baseline. The
single witness that would settle it (the pre-May-14 502 rate) is exactly the one
not retained.

Per the method: before writing CONFIRMED, ask "what would I have observed either
way?" Given a log that starts May 15, **I would have observed all-post-May-14
samples whether or not the kernel was the cause.** That mandates INCONCLUSIVE.

## Why a weak counter-lean (not neutral, and not "blame the kernel")

Two operational signatures mildly point *away* from a kernel-networking regression:

1. **Failure mode is `upstream_timeout` on every sample** — the LB timed out
   waiting on the backend, i.e. the symptom lives upstream of the LB, in
   backend/upstream latency. A kernel networking regression on the LB hosts more
   typically manifests as connection resets / SYN-retransmits / conntrack
   exhaustion, not clean upstream read-timeouts. This is suggestive, not decisive.
2. **All four LB hosts (lb1–lb4) affected uniformly** — consistent with a
   fleet-wide kernel change, *but equally* consistent with a single shared
   upstream/backend dependency. It does not isolate the LB kernel; if anything,
   uniform upstream-timeout across all LBs points at a common backend.

These drop the kernel-cause probability modestly below 0.5 rather than holding it
at neutral. Calibration guard applied: the censoring caveat *widens the band and
lowers confidence*, it does not by itself flip to "definitely not the kernel" —
the small push below 0.5 comes from the upstream-timeout signature, which is
independent positive reason, not from the censoring alone.

## What I explicitly did NOT do

I did not manufacture a CONFIRMED to satisfy "Ops suspects the kernel." Suspicion
is a prior, not a probe. Blaming the convenient party (the recent change) without
a control case is the exact failure this method exists to prevent. The honest
deliverable is the verdict + the probe that settles it.

---

## Hypotheses (mini-ledger)

| # | Hypothesis | Probe run | Verdict |
|---|---|---|---|
| H1 | May 14 kernel update caused the 502s | onset-timing vs data window | INCONCLUSIVE — onset evidence is censored (log starts May 15); LR≈1 |
| H0 | 502s pre-existed / unrelated to kernel | searched for pre-May-14 sample | INCONCLUSIVE — no pre-update data retained to confirm or deny |
| H2 | Cause is upstream/backend latency, not LB kernel | failure-mode = upstream_timeout on all 12; all 4 LBs uniform | weak SUPPORT (0.5–0.6); needs upstream p99 across May 14 boundary |

## Ruled out
- **Nothing can be ruled out** from the 12-sample log alone. The host spread
  (all 4 LBs) and time-of-day spread (hours 0–23, no diurnal clustering) are
  recorded so they aren't silently dropped, but neither discriminates the
  hypotheses.

## The probes that WOULD settle it (none break the "no prod bisect" rule)
See `settling_probes.md`. Ranked by power-per-cost:

1. **P1 — pull the 502 *counter* (not sampled logs) from the metrics TSDB back to
   May 1.** Counters usually outlive sampled request logs. A non-zero ~30/day 502
   rate on May 1–13 **falsifies** the kernel-onset story outright; a clean step at
   May 14 **confirms** it (temporality + step change). This is the single cheapest
   decisive probe and should be run first.
2. **P2 — compare SYN-retransmit / connection-reset / conntrack counters across the
   May 14 boundary**, plus upstream p99 latency. Discriminates kernel-networking
   regression vs upstream latency. Read-only.
3. **P3 — canary, not bisect:** one LB on the pre-May-14 kernel behind a 1–5%
   traffic split (or shadow traffic) for ~3–4 days; compare 502 rate canary vs
   fleet. This is the controlled but-for test and respects "cannot take prod down."

## Reproduce
```
cd <this dir>
python3 analyze.py     # parses lb_samples.log timestamps, prints censoring proof
```
Inputs: `iteration-2/scenarios/r2s03_weak_evidence/lb_samples.log` (12 rows),
`INCIDENT.md`. Kernel update date asserted as 2026-05-14.

## Reopen tripwire
If P1 returns a clean step at May 14 → reopen as CONFIRMED (raise to ~0.85+).
If P1 returns non-zero pre-May-14 502 rate → close H1 FALSIFIED, pursue H2.
