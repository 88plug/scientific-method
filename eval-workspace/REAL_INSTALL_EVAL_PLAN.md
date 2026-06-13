# Real-deployment eval plan — drive the installed plugin via `claude -p`

Why: every round so far pointed agents at the skill *files by path* and graded
the outputs. That measures the method's content, not what a real user gets —
which is the **installed v1.6.0 plugin triggering on its own from a natural
prompt**, in a sandbox cwd, through genuine `claude -p`. This is the gap the
headless description-optimizer couldn't close (it only measured triggering, and
that was broken for this model). Real-install eval closes it.

## What we now know about the harness (from claude-code-guide research)

- Bash long jobs → `run_in_background: true` (tracked, survives turns, dies on
  CLI exit, 5 GB output cap). Not hand-rolled `nohup &`.
- Files → Write tool, not heredocs (heredocs don't commit on non-zero exit).
- cwd → absolute paths; `cd` only persists inside project/`--add-dir`.
- `pkill` → isolate in its own call with `; true` (broad pkill self-signals the
  session's process group → exit 144).
- `claude -p` nested calls need `CLAUDECODE` unset in the child env (the
  description-optimizer's run_eval.py already does this).

## The eval design

1. **Sandbox per scenario.** Copy a scenario's sandbox to a fresh temp dir
   OUTSIDE the repo (so no skill-file paths are reachable and cwd is neutral).
   The prompt is what a real user would type — a TICKET/CLAIM/sim, no mention of
   the skill or its path.

2. **Invoke the real install.** `env -u CLAUDECODE claude -p "<user prompt>"
   --model claude-fable-5[1m] --output-format stream-json --verbose
   --add-dir <sandbox>` — the installed scientific-method plugin is at user
   scope, so it's in `available_skills` and must trigger on its own.

3. **Two measurements per scenario:**
   - **Triggering:** did the Skill tool fire for scientific-method? (parse the
     stream-json for the Skill tool_use). This is the real in-session triggering
     the headless optimizer could not measure.
   - **Quality:** grade the final output against the same planted ground truth /
     assertions used in the file-pointer rounds — verdict correctness, rung
     honesty, provenance, the verifier-audit discipline.

4. **Baseline arm:** same prompt with the plugin DISABLED (or a vanilla
   `claude -p`) → isolates what the installed skill adds in real deployment.

5. **Scenario set:** a stratified 10 from the existing 140 — one per capability
   family (red-herring, false-ceiling, restraint/INCONCLUSIVE, feedback-loop,
   prior-art-landmine, acceptance-gated invention, impossibility, provability
   ladder, calibration, open-records-lite) — so real-install behavior is checked
   across the whole method, not one mode.

## Honest expectations (pre-registered)

- Triggering in real `claude -p` may be LOWER than file-pointer rounds: the
  model handles many tasks directly without consulting a skill (the documented
  under-triggering). Measuring it is the point — if it under-triggers on
  genuinely method-shaped prompts, the fix is description work, now measurable.
- Quality when triggered should match the file-pointer rounds (same skill
  content). A gap there would mean path-pointing was doing hidden work the
  install doesn't replicate — a real finding.

## Sequencing

Run AFTER the grand-challenge campaign resolves (record or measured frontier),
so compute isn't split. One `run_in_background` task driving the 10×2 `claude -p`
invocations serially (nested claude -p is heavy), a Monitor on the progress log,
then grade. This is the eval that tells us what users actually experience.
