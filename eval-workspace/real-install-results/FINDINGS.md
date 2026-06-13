# Real-install eval — findings (installed v1.6.0 via genuine `claude -p`)

Drove the **installed** plugin through `env -u CLAUDECODE claude -p` from neutral
`/tmp` sandboxes (no skill-file paths reachable) — what a real user gets, not a
path-pointed eval.

## Triggering (resolves what the headless description-optimizer could not measure)

| scenario | prompt shape | skill fired |
|---|---|---|
| s01 root-cause (deploy red herring) | "root cause this completely, no guessing" | **yes** |
| s02 restraint (weak evidence) | "assess whether X caused Y" | no |
| s03 feedback loop (retry storm) | "root cause and propose the fix" | no |
| s04 invention (retry policy) | "invent ... meeting acceptance criteria" | **yes** |
| s05 impossibility (sort lower bound) | "evaluate the vendor's claim" | **yes** |

3/5 triggered on their own. The two non-triggers were the routine-analysis-sounding
prompts — the documented under-trigger, now **measured in real deployment** (the
optimizer's stripped headless harness couldn't measure it; a real session with the
full system prompt + available_skills can, and does).

## Quality (graded vs the existing planted ground truth)

- **s01 — exact.** Deploy FALSIFIED, disk/ENOSPC cause, temporality used to also kill
  the "r1 filled the disk" variant, hosts 1/3/6 as but-for negative control, 0.92.
- **s02 — correct without the skill.** INCONCLUSIVE lean, the sampling-baseline
  critique (e⁻¹¹ under the "sampler ran all May" hypothesis), confound awareness —
  matched the GT's demand for a calibrated lean, not an overclaim.
- **s03 — correct without the skill.** Retry storm identified, deploy exonerated,
  trigger = the 30s carrier flap, mechanism traced minute-by-minute from the data.
- **s04 — pipeline runs, exceeds the time box.** Skill triggered, read Pattern B,
  began building (Bash/Write/Edit) — a full acceptance-gated invention campaign does
  not fit in a single 600s `claude -p`. Needs Workflow-style multi-agent
  orchestration (what the file-pointer rounds used) or a larger budget. Not a defect.
- **s05 — exact.** FALSIFIED, 18,488,885-comparison Stirling bound, 18.49× too small,
  0.99 — computed by hand when the sandbox blocked code execution.

## The reframe (the load-bearing conclusion)

The base Fable-5 model **already internalizes the verification discipline** —
calibrated restraint, confound control, feedback-loop diagnosis — and produces
ground-truth-grade analysis even when the skill does not formally trigger. So the
plugin's differential value is **not** teaching carefulness; it is the structured
apparatus for what the base model won't spontaneously run end-to-end: full
falsification campaigns, the invention pipeline with executable acceptance gates +
provenance + certification rungs, the provability ladder, verify-the-verifier, and
the open-records attack methodology.

## Harness lessons (for the next real-deployment eval)

- Grant execution for invention/impossibility scenarios: `--permission-mode
  bypassPermissions` (the first s04 run was blocked by sandbox exec-deny).
- Invention campaigns need Workflow orchestration or >600s, not one serial call.
- Analysis/impossibility scenarios are fast and faithful in a single `claude -p`.
