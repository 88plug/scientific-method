<div align="center">

# Scientific Method

A Claude Code plugin that runs investigations, debugging, performance work, and claim validation as falsification-first campaigns — for engineers who need to be right, not just confident.

[![plugin-validate](https://github.com/88plug/scientific-method/actions/workflows/plugin-validate.yml/badge.svg)](https://github.com/88plug/scientific-method/actions/workflows/plugin-validate.yml)
[![License: FSL-1.1-ALv2](https://img.shields.io/badge/license-FSL--1.1--ALv2-blue?style=flat)](LICENSE.md)
[![Claude Code plugin](https://img.shields.io/badge/Claude%20Code-plugin-8A2BE2?style=flat)](https://github.com/88plug/claude-code-plugins)
[![Docs](https://img.shields.io/badge/docs-online-2ea44f?style=flat)](https://88plug.github.io/scientific-method/)

</div>

## Install

```text
/plugin marketplace add 88plug/scientific-method
/plugin install scientific-method@scientific-method
```

## Quickstart

Run a full campaign on any problem in one command:

```text
/scientific-method:investigate the API returns 500 under load but not in tests
```

You get back labeled hypotheses (H1..Hn), a prediction for each written before
any measurement, the cheapest probe run first, and a calibrated verdict — with
every result logged to a persistent ledger so killed ideas stay killed.

No setup, no API keys, no MCP server. The plugin enforces method over your
existing tools.

## What it does

Most debugging is guessing dressed up as analysis. This plugin makes Claude
work like a scientist: turn each assertion into a falsifiable hypothesis,
predict the outcome before measuring, run a controlled experiment, attack the
result before trusting it, and record the verdict so it survives across
sessions.

It is distilled from real session transcripts where the method cracked
problems ordinary debugging did not — a GPU codec campaign that falsified four
asserted "physical" performance walls, a fleet forensics investigation that
killed two plausible-but-wrong root causes with control cases before filing a
vendor bug, and benchmark work where honest baselines caught regressions that
averages hid.

> [!NOTE]
> This is a methodology plugin. It ships a skill, commands, agents, and one
> read-only hook — no MCP server, output style, or statusline. The hook is the
> only thing that runs automatically, and it only reads `EXPERIMENTS.md`.

## What it enforces

- Every asserted limit, cause, or claim becomes a labeled falsifiable
  hypothesis (H1..Hn) with an explicit null.
- Predictions and outcome-to-conclusion tables are written before measuring.
- Cheapest falsification first — one probe beats five agents arguing.
- Controls and baselines are mandatory for causal and performance claims.
- Findings pass a REFUTE-first adversarial gate before being trusted.
- Confidence is calibrated — 0.90+ needs ground-truth proof, and being
  confidently wrong is worse than being inconclusive.
- Verdicts persist in a hypothesis ledger (`EXPERIMENTS.md`) with a
  falsification log marked DO-NOT-RE-ATTACK, so killed ideas stay killed across
  sessions and compactions.

## The workflow

Each stage maps to a command you can run on its own, or that `investigate`
chains for you.

- Hypothesis — turn each assertion into a labeled, falsifiable claim with a null.
- Prediction — write what each outcome would mean, before measuring.
- Experiment — run the cheapest controlled probe that can falsify the claim.
- Refute — attack surviving findings adversarially before trusting them.
- Verdict — issue a calibrated result: confirmed, prototype, research, or kill.
- Ledger — persist verdicts so killed ideas are never re-attacked.

## Commands

| Command | What it does |
|---|---|
| `/scientific-method:investigate <problem>` | Full campaign: hypotheses, controlled experiments, verdicts, ledger |
| `/scientific-method:falsify <claim>` | Attack an asserted limit, ceiling, or claim with designed probes |
| `/scientific-method:invent <problem>` | Invention campaign: ideate past a limit, refute, build, measure vs tuned baseline, provenance-search, certify |
| `/scientific-method:verdict [claims]` | Adversarial REFUTE-first review of findings before they are trusted |
| `/scientific-method:ledger [sync]` | Create or update the persistent hypothesis ledger |
| `/scientific-method:council <question>` | Model council: same question to independent seats on different models, dissent surfaced, factual cruxes routed to probes |
| `/scientific-method:peer-review <work>` | Blind lensed reviewers who execute, rebuttal answered with evidence, area-chair decision |

## Agents

These run under the hood when a campaign fans out. You can also invoke them
directly.

- `experiment-designer` — designs one hypothesis, probe, and outcome table (design and execute are split).
- `refuter` — tries to refute a finding, returns confirmed, prototype, research, or kill.
- `council-member` — one independent council seat: position, evidence, and "what would change my mind".
- `peer-reviewer` — one blind, execution-grounded review with scores and a recommendation.
- `meta-reviewer` — the area chair: weighs evidence over votes and issues the final decision.

<details>
<summary>Skill and hook</summary>

- `scientific-method` skill — the method itself, artifact templates, and multi-agent campaign patterns.
- SessionStart hook — if `EXPERIMENTS.md` exists, surfaces the ledger at session start so killed hypotheses stay killed. Read-only; a silent no-op when the file is absent.

</details>

## How to trigger

Run any command above, or let the skill auto-trigger. It activates on phrases
like "use the scientific method", "prove it", "validate these claims", "root
cause this 100%", "no guessing", or any challenge to an asserted number, limit,
or cause.

> [!TIP]
> When you want a finding double-checked before you act on it, run
> `/scientific-method:verdict` — it puts the claim through the REFUTE-first
> gate without rerunning the whole campaign.

## Install from a local clone

```text
git clone https://github.com/88plug/scientific-method
/plugin marketplace add ./scientific-method
/plugin install scientific-method@scientific-method
```

## Updating

This plugin ships rolling — every commit is a release. Your installed version
(`claude plugin list`) and the one in the
[88plug catalog](https://github.com/88plug/claude-code-plugins) are shown as
`vYEAR.MONTH.BUILD`; if they differ, run
`/plugin update scientific-method@88plug`. With marketplace auto-update
enabled, you always get the latest automatically.

## Contributing

Issues and pull requests are welcome at
[88plug/scientific-method](https://github.com/88plug/scientific-method). The
[plugin-validate](https://github.com/88plug/scientific-method/actions/workflows/plugin-validate.yml)
workflow runs on every change — make sure it passes before you open a PR.

## License

[FSL-1.1-ALv2](LICENSE.md) © 2026 [88plug](https://github.com/88plug) —
Functional Source License; converts to Apache 2.0 two years after each release.
