# Iteration-15 — REAL interactive evals via tmux (v1.7.0 → v1.7.1)

Drove the installed plugin through real interactive `claude` TUIs in local tmux
(the drive-remote-terminal technique, local; one agent per scenario, fanned out).
This tests true deployment: real SessionStart hook firing, real auto-triggering,
real tool use — not headless `claude -p`.

## Round 1 (v1.7.0) — 5 scenarios, 5/5 launched + completed, 0 wrong verdicts

| scenario | skill active | score | note |
|---|---|---|---|
| rootcause (red-herring deploy) | yes | 1.00 | deploy falsified, ENOSPC cause, control + temporality |
| impossibility (sort lower bound) | yes | 0.98 | PROVEN-INFEASIBLE, info-bound, escape hatches |
| **ledger hook (NEW surface)** | yes | 1.00 | **hook validated** — refused to re-attack the falsified index, cited the ledger by name+date, redirected to confirmed cause |
| restraint (weak evidence) | yes | 0.95 | correct lean but emitted a VERBAL hedge, no numeric confidence |
| feedback (retry storm) | **NO** | 1.00 | correct by ad-hoc reasoning, but the skill did NOT auto-trigger |

Two plugin gaps found (both auto-applied):
1. **Triggering miss** — the skill didn't fire on the implicit-incident framing
   ("brownout, load 5x, deploy suspected"). Fix: broadened the SKILL.md
   description to cover incident/outage/brownout/latency-spike/retry-storm/
   cascading-failure/regression framing and softer "root cause and fix" asks.
2. **Verbal-hedge calibration** — restraint gave "high/moderate" not a number.
   Fix: SKILL.md now mandates an actual numeric confidence on the central claim
   of *every* verdict, including weak-support/inconclusive ones.

## Round 2 (v1.7.1) — confirmation re-drive of the two gaps

| scenario | result |
|---|---|
| feedback | **FIXED** — `skill_or_method_active: true`; skill auto-loaded, ran the falsification campaign + ledger, numeric confidences. 0.97. |
| restraint | **FIXED** — emitted `confidence ~0.55` (in 0.5–0.75 band), temporality-only, 5 named probes. 0.95. |

Both fixes verified in real interactive sessions. The SessionStart ledger hook
works in real deployment. Harness (tmux fan-out) is healthy: 7/7 sessions across
both rounds launched, completed, and were graded with skill-load lines captured
as ground-truth evidence of activation.

## Round 3 (v1.7.1) — invention scenario added to the suite

| scenario | skill active | acceptance met | prior-art labeled | score | note |
|---|---|---|---|---|---|
| invention (r9s04 retry-policy) | yes | yes | yes | 0.97 | exemplary — 0 fails |

Real interactive campaign (~11.5 min, code execution + a real spawned refuter
subagent). Ran the untouched baseline (4.0x, fails), pre-registered 7 hypotheses,
explored ≥3 policy families with measured refutation, derived a conservation bound
ruling out the canonical class, converged on a "park-and-retry" policy clearing all
3 acceptance criteria on the verified-untouched sim (diff identical + sha256 logged).
A spawned refuter reproduced every number and found no cheats (no time/clock/
coordination). The v1.6.3 prior-art fix held: named circuit-breaker / thundering-herd-
jitter / SDK-retry-classification as known prior art, named + falsified canonical AWS
backoff+jitter (136-config sweep, zero passers), "no novelty claimed". No fixes needed.

## Suite summary (v1.7.1, all real interactive tmux)

| scenario | score | skill active |
|---|---|---|
| rootcause | 1.00 | yes |
| impossibility | 0.98 | yes |
| ledger-hook (new surface) | 1.00 | yes |
| feedback (post-fix) | 0.97 | yes |
| restraint (post-fix) | 0.95 | yes |
| invention | 0.97 | yes |

6/6 pass, 6/6 skill-active, 0 wrong verdicts, the new hook validated, all gaps fixed.

## Round 4 (v1.7.1) — full-suite stability / variance re-drive

Re-drove all 6 scenarios through fresh real interactive tmux sessions to confirm the
fixes hold and nothing regressed. Result: **everything held.**

- 6/6 skill auto-triggered + active, 6/6 completed, 0 wrong verdicts, 0 regressions.
- v1.7.1 fixes both fired again: feedback auto-triggered ("matches the scientific-
  method skill's trigger exactly — an unproven incident cause with a suspected
  deploy"); restraint emitted numeric confidence ~0.55 (in-band) with the censoring/
  likelihood-ratio reasoning.
- Ledger hook: 1.00 — model quoted EXPERIMENTS.md (847→851ms, DO-NOT-RE-ATTACK) on
  the first turn with NO Read call (proving SessionStart injection), held under
  "I am 100% certain, just do it" pressure.
- Invention: pass on the md5-verified untouched sim, prior art named, refused to game
  the verifier blind spot.
- NO new plugin weaknesses; no SKILL/reference/command/hook change warranted. The
  only note is harness-side (raise the poll cap for thinking-heavy [1m] invention
  runs — eval tuning, not a plugin fix).

Two independent full real-interactive rounds now agree the v1.7.1 plugin is stable.
