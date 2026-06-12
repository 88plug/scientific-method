# scientific-method

A Claude Code plugin that turns investigations, debugging sessions,
performance campaigns, and claim validation into falsification-first
scientific campaigns.

Distilled from real session transcripts where the method cracked problems
ordinary debugging didn't: a GPU codec campaign that falsified four asserted
"physical" performance walls, a fleet forensics investigation that killed two
plausible-but-wrong root causes with control cases before filing a vendor
bug, and benchmark work where honest baselines caught regressions that
averages hid.

## What it enforces

- Every asserted limit/cause/claim becomes a labeled falsifiable hypothesis
  (H1..Hn) with an explicit null
- Predictions and outcome→conclusion tables are written **before** measuring
- Cheapest falsification first — one probe beats five agents arguing
- Controls and baselines are mandatory for causal/performance claims
- Findings pass a REFUTE-first adversarial gate before being trusted
- Confidence is calibrated (0.90+ needs ground-truth proof; confidently
  wrong is worse than inconclusive)
- Verdicts persist in a hypothesis ledger (`EXPERIMENTS.md`) with a
  falsification log marked DO-NOT-RE-ATTACK, so killed ideas stay killed
  across sessions and compactions

## Components

| Component | What it does |
|---|---|
| `/scientific-method:investigate <problem>` | Full campaign: hypotheses → controlled experiments → verdicts → ledger |
| `/scientific-method:falsify <claim>` | Attack an asserted limit/ceiling/claim with designed probes |
| `/scientific-method:invent <problem>` | Full invention campaign: ideate past a limit → refute → build → measure vs tuned baseline → provenance-search → certify |
| `/scientific-method:verdict [claims]` | Adversarial REFUTE-first review of findings before they're trusted |
| `/scientific-method:ledger [sync]` | Create/update the persistent hypothesis ledger |
| `/scientific-method:council <question>` | Model council: same question, independent seats on different models (+ optional local-LLM out-of-family seat), dissent surfaced, factual cruxes routed to probes, corrections applied |
| `/scientific-method:peer-review <work>` | True peer review: blind lensed reviewers (soundness/prior-art/repro/significance/fatal-flaw) who execute, rebuttal answered with evidence, revisions applied in-round, area-chair decision |
| `experiment-designer` agent | Designs one hypothesis + probe + outcome table (design/execute split) |
| `refuter` agent | Tries to refute a finding, returns confirmed/prototype/research/kill |
| `council-member` agent | One independent council seat: position + evidence + "what would change my mind" |
| `peer-reviewer` agent | One blind, execution-grounded review with scores + recommendation |
| `meta-reviewer` agent | Area chair: weighs evidence over votes, issues the final decision |
| `scientific-method` skill | The method itself + artifact templates + multi-agent campaign patterns |
| SessionStart hook | If `EXPERIMENTS.md` exists, surfaces the ledger at session start so killed hypotheses stay killed (read-only; silent no-op when absent) |

## Install

```
/plugin marketplace add 88plug/scientific-method
/plugin install scientific-method@scientific-method
```

Or from a local clone:

```
git clone https://github.com/88plug/scientific-method
/plugin marketplace add ./scientific-method
/plugin install scientific-method@scientific-method
```

The skill also auto-triggers on phrases like "use the scientific method",
"prove it", "validate these claims", "root cause this 100%", "no guessing",
or any challenge to an asserted number/limit/cause.

## What it bundles

A skill, 7 commands, 5 agents, and one read-only SessionStart hook — no MCP
server, output style, or statusline (a methodology plugin enforces discipline
over existing tools; it does not need new external capabilities). The hook is
the only thing that runs automatically, and it only reads `EXPERIMENTS.md`.

## License

[FSL-1.1-ALv2](LICENSE.md) © 2026 [88plug](https://github.com/88plug) — Functional
Source License; converts to Apache 2.0 two years after each release.
