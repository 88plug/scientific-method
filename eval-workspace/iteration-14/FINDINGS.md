# Iteration-14 eval — findings & fixes (2026-06-12, plugin v1.6.2 → v1.6.3)

5 scenarios × {with-skill v1.6.2, baseline}, graded vs the planted ground truth
from prior iterations. Scenarios: root-cause/red-herring (s01), restraint/weak-
evidence (r2s03), feedback-loop/retry-storm (r6s01), invention/retry-policy
(r9s04), impossibility/sort-lower-bound (r11s02).

## Results

| scenario | with-skill | note |
|---|---|---|
| s01 root-cause | 1.00 | clean — deploy falsified, disk/ENOSPC cause, IS/IS-NOT |
| r6s01 feedback-loop | 1.00 | clean — retry storm, deploy exonerated |
| r11s02 impossibility | 1.00 | clean — PROVEN-INFEASIBLE, info-bound, Stirling, escape hatches |
| **r9s04 invention** | **0.86 → 0.97** | FIXED (prior-art labeling) |
| **r2s03 restraint** | **0.71 → 0.72** | fix improved form; residual is a GT-leniency edge case |

## Weakness 1 — invention pipeline under-applied prior-art discipline (FIXED, verified)

r9s04 (v1.6.2) invented a flat-backoff policy and argued it was "strictly better"
than exponential backoff, beating a weak strawman baseline (3 immediate retries),
without naming the canonical industry solution (capped exponential backoff + jitter,
AWS canon) as prior art.

**Fix:** invent.md §2 — "Name the canonical solution, especially when you re-derive
it": find the industry-standard answer, name it as prior art AND make it the tuned
baseline (not a strawman), and scope novelty to the measured delta when your
mechanism shares its ingredients.

**Verified:** re-run against patched skill → 0.97. The run now names AWS
decorrelated/capped backoff+jitter (Brooker 2015) as prior art, scopes its claim to
the down-vs-overload split delta, labels it NO-PRIOR-ART-FOUND (not "novel"), and
keeps a calibrated 0.93/prototype verdict.

## Weakness 2 — over-restraint vs calibrated lean (fix improved form; GT debatable)

r2s03 (v1.6.2) verdicted INCONCLUSIVE @ 0.35 (lean *against* the kernel). The GT
prescribes a calibrated weak lean *toward* the kernel at 0.5–0.75 (temporality).

**Fix:** SKILL.md §4 — a calibrated weak lean ≠ INCONCLUSIVE; weigh by likelihood
ratio, avoid both inflation to 0.9+ and collapse to a flat no-lean refusal; let the
headline reflect the lean; name the probe.

**Outcome (honest):** the patched run is now calibrated, numeric, directional, and
probe-bearing (the substantive win), but still lands ~0.40 near-neutral. The grader
found the model is *right*: the incident log starts May 15 (one day post-update), so
"all 12 post-date May 14" is FORCED by the observation window — likelihood ratio ≈ 1,
the temporality is censored. The model's near-neutral verdict is "defensible and
arguably sharper" than the GT's prescribed toward-kernel band. So the residual fail
is **ground-truth leniency** (r2s03 GT underweights the May-15 log-start censoring),
not a skill defect — the fix was deliberately written to treat demonstrable
censoring as good science, not forced into the GT's number. Meta-finding: r2s03's
ground truth should be sharpened to credit the censoring analysis.

## Net

Two minimal skill edits (+~30 lines, no bloat), one verified by re-run, one improving
calibration form without overfitting to a debatable GT. No regressions on the three
clean scenarios.
