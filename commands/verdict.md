---
description: "Adversarial REFUTE-first review of current findings/claims before they are trusted"
argument-hint: "[findings to review, or empty to review this conversation's claims]"
disable-model-invocation: true
allowed-tools: Task
---

Adversarially review: $ARGUMENTS

If no argument, collect the load-bearing claims made in this conversation so
far (by you or by research agents) — root causes, performance numbers,
"X is confirmed", "Y is impossible", external facts about repos/products —
and review those.

This is the gate between "we found something" and "we act on it / report it
externally". The bar: would this survive a skeptical partner who pays the
cost if it's wrong? A confidently-wrong claim anchors everyone downstream —
it is strictly worse than reporting "inconclusive".

For each claim, spawn the plugin's refuter agent (one fresh agent per claim —
fresh context is the point; the author cannot referee its own finding). For
small claim sets or when agents are unavailable, apply the rubric inline:

1. Try to refute it first. What is the cheapest observation that would kill
   it? Run that probe now — fetch the primary source, re-run the
   measurement, check the control case. Arguing from memory is not review.
2. Check the evidence chain: does every claim have an evidence reference
   (command, log line, timestamp+value)? Unreferenced claims get demoted to
   discovery status with a named next probe.
3. Check for the classic holes: per-component win presented as end-to-end
   win; correlation without a control case; derived number presented as
   measurement; baseline missing so a regression could hide; contradictions
   between independent sources (numbers that disagree by integer factors are
   a hallucination signature).
4. Verdict per claim: confirmed / prototype (needs one more measurement —
   name it) / research / kill (with kill_reason). Default to the lower
   verdict when uncertain.

Report a verdict table for all claims, the kills with reasons (append to the
ledger's falsification log if one exists), and the surviving claims with
their calibrated confidence. If anything was demoted, say what single probe
would promote it back.
