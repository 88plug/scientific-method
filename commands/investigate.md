---
description: "Run a full scientific investigation: hypotheses, controlled experiments, verdicts, ledger"
argument-hint: "[problem or question to investigate]"
disable-model-invocation: true
allowed-tools: Task
---

Run a falsification-first investigation of: $ARGUMENTS

If no problem was given, investigate the most recently discussed open question
in this conversation; if there is none, ask what to investigate.

Follow the scientific-method skill (read its SKILL.md if not already loaded).
The contract for this command:

1. **Cheapest probe first.** Identify and run the single cheapest observation
   that could settle or kill the leading explanation before any planning.
2. **Hypothesis ledger.** Enumerate every candidate explanation as a numbered
   falsifiable hypothesis with an explicit null. Include the inconvenient
   ones ("it's our own change", "it's not their bug") — convenient
   explanations require the same controls as everyone else. Create or update
   `EXPERIMENTS.md` (or the project's existing incident/docs convention)
   before running experiments. Check the ledger's falsification log first —
   anything marked DO-NOT-RE-ATTACK is settled; don't re-litigate it.
3. **Predict, then probe.** For each hypothesis write the outcome→conclusion
   table before measuring. Design probes with controls (negative control
   cases for causal claims, baselines for performance claims) and confounds
   named. Scale out with parallel agents when there are many independent
   hypotheses — use the campaign patterns in the skill's
   references/campaigns.md and the plugin's experiment-designer agent.
4. **Verdicts with evidence.** Every hypothesis ends CONFIRMED / FALSIFIED /
   INCONCLUSIVE with an evidence reference and calibrated confidence
   (0.90+ only with direct ground-truth proof; never a silent default).
   INCONCLUSIVE must name the exact next probe.
5. **Adversarial pass.** Before presenting conclusions, run the refuter agent
   (or its rubric inline) against your primary finding. If it survives,
   report it; if not, loop.
6. **Loop until clean.** A pass that finds something means the search is
   incomplete. Stop only on a dry pass with all verdicts filled.

Final report: lead with the verdict and confidence, then the hypothesis table,
ruled-out list with evidence, residual unknowns with next probes, and the
ledger path. Negative results are findings — report them with the same weight.
