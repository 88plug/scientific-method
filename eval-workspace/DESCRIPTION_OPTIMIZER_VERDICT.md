# Description-optimizer run — verdict (2026-06-11)

Setup: skill-creator run_loop, 20-query trigger eval (10 pos / 10 hard-negative),
12 train / 8 test, model claude-fable-5[1m], runs-per-query 3.

## Result: KILLED after 2 iterations — measurement invalid for this model

- Iter 1 (current description): precision 100%, recall 0%, accuracy 50%
- Iter 2 (rewritten, situation-first description): precision 100%, recall 0%, accuracy 50%
- Two structurally different descriptions scoring identically 0/30 on positives
  falsified "description quality drives the trigger rate" in this harness.
- Decisive probe: manual `claude -p` with a clean targeted description, 110s
  budget (vs the harness's 30s): the model made 14 Bash tool calls answering the
  benchmark-verification query directly and NEVER invoked the Skill tool.
  Recall=0 is real headless behavior, not a timeout artifact: in bare -p mode
  this model investigates immediately rather than consulting a matching skill.

## Decision

Keep the current (committed) description — it has in-session trigger evidence
and the 50-scenario behavioral campaign behind it. Do NOT adopt the optimizer's
candidate off a flat-zero signal; that would be fitting noise (the same
Twyman/A-A discipline the skill itself teaches).

Iter-2 candidate preserved below as a qualitatively reasonable alternative if a
valid trigger harness (in-session, or a model that consults skills headless)
becomes available:

> Use this skill whenever someone doubts a number or demands rigorous proof of a
> cause — any time a benchmark result, metric, performance limit, or root-cause
> story needs to be verified rather than trusted. Typical situations: a
> measurement looks suspicious or too good ("2x faster but I don't trust it",
> "is this number real or an artifact?"); a regression, error spike, or incident
> needs its true cause established before a decision ("the team blames X —
> confirm it, no guessing"); an asserted ceiling, cap, or "impossible" limit
> needs to be broken or proven real; numbers in a report or README need
> validation before publishing. It runs the work as a falsification-first
> campaign: numbered hypotheses, predictions recorded before measurement,
> controlled experiments, adversarial refutation, calibrated confidence, a
> persistent ledger. Also use it proactively before asserting any ceiling or
> root cause of your own. Do NOT use for ordinary feature work, refactoring, or
> questions answerable by reading one file.

Eval set kept at trigger_eval_set.json for re-runs. Full log: descopt.log.
