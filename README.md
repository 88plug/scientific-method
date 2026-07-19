<div align="center">

# Scientific Method

**Falsification-first investigation and invention workflow for Claude Code** — hypothesis ledgers, controlled experiments, REFUTE-first verification, and provable invention for coding agents that need to be right.

[![plugin-validate](https://github.com/88plug/scientific-method/actions/workflows/plugin-validate.yml/badge.svg)](https://github.com/88plug/scientific-method/actions/workflows/plugin-validate.yml)
[![License: FSL-1.1-ALv2](https://img.shields.io/badge/license-FSL--1.1--ALv2-blue?style=flat)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-online-2ea44f?style=flat)](https://88plug.github.io/scientific-method/)
[![Claude Code plugin](https://img.shields.io/badge/Claude%20Code-plugin-8A2BE2?style=flat)](https://github.com/88plug/claude-code-plugins)
[![DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/88plug/scientific-method)

</div>

## Install

```text
/plugin marketplace add 88plug/claude-code-plugins
/plugin install scientific-method@88plug
```

### Grok Build

```text
grok plugin marketplace add 88plug/claude-code-plugins
grok plugin install scientific-method@88plug --trust
```


No setup, no API keys, no MCP server. The plugin enforces method over your existing tools.

## Quickstart

Run a full falsification campaign on any problem in one command:

```text
/scientific-method:investigate the API returns 500 under load but not in tests
```

You get labeled hypotheses (H1..Hn), a prediction for each written before any measurement, the cheapest probe run first, and a calibrated verdict — every result logged to a persistent ledger so killed ideas stay killed.

## What it does

Most AI coding-agent debugging is guessing dressed up as analysis. This Claude Code plugin turns investigations, performance work, claim validation, and invention into falsification-first campaigns: every assertion becomes a labeled hypothesis, you predict before measuring, run a controlled experiment, attack the result before trusting it, and persist the verdict.

It is a multi-agent verification workflow distilled from real sessions — a GPU codec campaign that falsified four asserted "physical" performance walls, fleet forensics that killed two plausible-but-wrong root causes with control cases, and benchmarks where honest baselines caught regressions that averages hid. Developer tools, automation, and CLI commands enforce the method so LLM agents stay honest under pressure.

> [!NOTE]
> This is a methodology plugin. It ships a skill, commands, agents, and one read-only SessionStart hook — no MCP server, output style, or statusline. The hook only reads `EXPERIMENTS.md` and is a silent no-op when the file is absent.

## Features

| Feature | Detail |
| --- | --- |
| Falsifiable hypotheses | Every limit, cause, or claim becomes H1..Hn with an explicit null |
| Predict before measure | Outcome-to-conclusion tables written before any probe runs |
| Cheapest falsification first | One controlled experiment beats five agents arguing |
| Controls and baselines | Mandatory for causal and performance claims |
| REFUTE-first gate | Adversarial verification before a finding is trusted |
| Calibrated confidence | 0.90+ needs ground-truth proof; confidently wrong loses to inconclusive |
| Hypothesis ledger | Verdicts persist in `EXPERIMENTS.md` with DO-NOT-RE-ATTACK log |
| Multi-agent campaigns | Designer, refuter, council, and peer-review agents fan out under the hood |
| Invention path | Ideate past a limit, refute, measure vs tuned baseline, certify |
| Auto-trigger skill | Activates on "prove it", "no guessing", root-cause, and claim challenges |

## Workflow

Each stage maps to a command you can run alone, or that `investigate` chains for you. Full detail: [workflow docs](https://88plug.github.io/scientific-method/workflow/).

| Stage | What happens |
| --- | --- |
| Hypothesis | Turn each assertion into a labeled, falsifiable claim with a null |
| Prediction | Write what each outcome would mean, before measuring |
| Experiment | Run the cheapest controlled probe that can falsify the claim |
| Refute | Attack surviving findings adversarially before trusting them |
| Verdict | Issue a calibrated result: confirmed, prototype, research, or kill |
| Ledger | Persist verdicts so killed ideas are never re-attacked |

## Commands

| Command | What it does |
| --- | --- |
| `/scientific-method:investigate <problem>` | Full campaign: hypotheses, controlled experiments, verdicts, ledger |
| `/scientific-method:falsify <claim>` | Attack an asserted limit, ceiling, or claim with designed probes |
| `/scientific-method:invent <problem>` | Invention campaign: ideate, refute, build, measure vs baseline, certify |
| `/scientific-method:verdict [claims]` | Adversarial REFUTE-first review of findings before they are trusted |
| `/scientific-method:ledger [sync]` | Create or update the persistent hypothesis ledger |
| `/scientific-method:council <question>` | Independent model seats, dissent surfaced, cruxes routed to probes |
| `/scientific-method:peer-review <work>` | Blind lensed reviewers, evidence-backed rebuttal, area-chair decision |

## Agents

These run under the hood when a campaign fans out. You can also invoke them directly.

| Agent | Role |
| --- | --- |
| `experiment-designer` | Designs one hypothesis, probe, and outcome table (design split from execute) |
| `refuter` | Tries to refute a finding; returns confirmed, prototype, research, or kill |
| `council-member` | One independent seat: position, evidence, and what would change its mind |
| `peer-reviewer` | One blind, execution-grounded review with scores and a recommendation |
| `meta-reviewer` | Area chair: weighs evidence over votes and issues the final decision |

<details>
<summary>Skill and hook</summary>

- `scientific-method` skill — the method itself, artifact templates, and multi-agent campaign patterns.
- SessionStart hook — if `EXPERIMENTS.md` exists, surfaces the ledger at session start so killed hypotheses stay killed. Read-only; silent no-op when the file is absent.

</details>

## How to trigger

Run any command above, or let the Claude skill auto-trigger. It activates on phrases like "use the scientific method", "prove it", "validate these claims", "root cause this 100%", "no guessing", or any challenge to an asserted number, limit, or cause.

> [!TIP]
> When you want a finding double-checked before you act on it, run
> `/scientific-method:verdict` — it puts the claim through the REFUTE-first
> gate without rerunning the whole campaign.

## Development

Local clone for contributors (marketplace install above is preferred):

```text
git clone https://github.com/88plug/scientific-method
/plugin marketplace add ./scientific-method
/plugin install scientific-method@88plug
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

Docs: [88plug.github.io/scientific-method](https://88plug.github.io/scientific-method/) · [DeepWiki](https://deepwiki.com/88plug/scientific-method)

## License

[FSL-1.1-ALv2](LICENSE) © 2026 [88plug](https://github.com/88plug) —
Functional Source License; converts to Apache 2.0 two years after each release.
