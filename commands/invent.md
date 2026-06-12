---
description: "Run a full invention campaign: ideate past a limit, refute, build, measure against acceptance criteria, provenance-search, certify"
argument-hint: "[the problem to solve or the limit to break, with acceptance criteria if known]"
disable-model-invocation: true
allowed-tools: Task
---

Run an invention campaign on: $ARGUMENTS

Read the scientific-method skill's `references/invent.md` (the pipeline),
`references/anticipate.md` (generators), and `references/campaigns.md`
Pattern B (ideate→refute) before starting. Then:

1. **Frame the target as falsifiable acceptance criteria.** If the user gave
   criteria, pre-register them; if not, derive them (quantified effect vs a
   tuned baseline, on a stated scope) and confirm. Measure the baseline
   first — the wall is a number, not a vibe. If the target itself may be
   infeasible, say so early and consider proving it (impossibility toolkit).
2. **Ideate with quotas and forced diversity** — Pattern B lenses plus the
   anticipate.md generators (TRIZ separations, ideal final result,
   recombination of surviving partials). Each idea carries mechanism,
   beats-wall-because, and a provenance guess.
3. **Refute before building** — fresh-context refutation per idea; kills go
   to the falsification log with reasons. Survivors ranked by expected
   effect ÷ build cost.
4. **Build and measure the survivors** — against the pre-registered
   acceptance criteria / tuned baseline, n + spread, environment tagged
   (lab/relevant/operational), round-trip or correctness oracles where they
   apply. Honest failures iterate or die; never adjust the criteria to fit
   the result (deviations get a dated scope correction).
5. **Provenance-search every surviving mechanism** (invent.md protocol:
   query families, venue sweep, citation chase, saturation; documented
   search log). Claim grammar: "closest found: X, differing in Y" — a
   no-prior-art conclusion requires the log, and an unsearched mechanism is
   never presented as new.
6. **Certify and ledger it** — grade the claim on the certification ladder
   (asserted → functional → reproduced → certified), write the claim chart
   (element | evidence | how verified), file kills as DO-NOT-RE-ATTACK,
   record opened questions and reopen tripwires. High-stakes inventions then
   go to `/scientific-method:peer-review` with the prior-art/provenance lens
   doing real searches.
