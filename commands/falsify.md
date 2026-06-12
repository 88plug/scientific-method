---
description: "Attack an asserted limit, ceiling, or claim with designed experiments"
argument-hint: "[the claim/limit/ceiling to attack, or 'all' for every assertion in scope]"
disable-model-invocation: true
allowed-tools: Task
---

Falsify or confirm: $ARGUMENTS

If the argument is "all" (or empty), first sweep the current project's docs,
benchmarks, and this conversation for asserted limits — every "ceiling",
"wall", "maximum", "can't", "impossible", and derived formula — and list
them. Derived numbers (X/2, spec-sheet values, library metadata, "the paper
says") are prime targets: past campaigns falsified four of five asserted
"physical" walls, and the real measurements were already contradicting one
of them when someone finally checked.

Follow the scientific-method skill. For each assertion:

1. Restate it as a falsifiable hypothesis with concrete numbers, plus the
   null (what you'd observe if the limit is real). Identify the suspected
   flaw in how the original number was produced ("single-stream artifact",
   "measured with cache hot", "vendor default, never probed").
2. Write the prediction and outcome→conclusion table BEFORE running anything.
3. Design one isolated probe per hypothesis. Control the confounds: serial
   execution on a clean device, cache bypass, locked clocks, isolation
   between passes — name every control you applied. For many hypotheses,
   fan out with the experiment-designer agent using the design/execute split
   (agents write probes, you run them serially) per the skill's
   references/campaigns.md.
4. Run, then fill verdicts: FALSIFIED (with the real measured ceiling) or
   CONFIRMED (with the measurement proving it's physical, reported as % of a
   measured — not spec-sheet — maximum), or INCONCLUSIVE with the named
   missing probe.
5. Record everything in the walls-doc/ledger format from the skill's
   references/artifacts.md, including a Reproduce block with exact commands,
   and append kills to the falsification log marked DO-NOT-RE-ATTACK.

A confirmed limit is as valuable as a broken one — it ends a search honestly.
Report both with the evidence and what each unlocks or closes.
