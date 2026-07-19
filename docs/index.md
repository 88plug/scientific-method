# Scientific Method

A Claude Code plugin that runs investigations, debugging, performance work, and claim validation as falsification-first campaigns — for engineers who need to be right, not just confident.

[![plugin-validate](https://github.com/88plug/scientific-method/actions/workflows/plugin-validate.yml/badge.svg)](https://github.com/88plug/scientific-method/actions/workflows/plugin-validate.yml)
[![License: FSL-1.1-ALv2](https://img.shields.io/badge/license-FSL--1.1--ALv2-blue?style=flat)](https://github.com/88plug/scientific-method/blob/main/LICENSE)
[![Claude Code plugin](https://img.shields.io/badge/Claude%20Code-plugin-8A2BE2?style=flat)](https://github.com/88plug/claude-code-plugins)
[![Docs](https://img.shields.io/badge/docs-online-blue?style=flat)](https://88plug.github.io/scientific-method/)

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

Run a full campaign on any problem in one command:

```text
/scientific-method:investigate the API returns 500 under load but not in tests
```

You get labeled hypotheses (H1..Hn), a prediction for each written before any measurement, the cheapest probe run first, and a calibrated verdict — every result logged to a persistent ledger so killed ideas stay killed.

## What it does

Most debugging is guessing dressed up as analysis. This plugin makes Claude work like a scientist:

1. Turn each assertion into a falsifiable hypothesis.
2. Predict the outcome before measuring.
3. Run a controlled experiment.
4. Attack the result before trusting it.
5. Record the verdict so it survives across sessions.

It is distilled from real session transcripts: a GPU codec campaign that falsified four asserted "physical" performance walls, a fleet forensics investigation that killed two plausible-but-wrong root causes with control cases before filing a vendor bug, and benchmark work where honest baselines caught regressions that averages hid.

!!! note
    This is a methodology plugin. It ships a skill, commands, agents, and one read-only hook — no MCP server, output style, or statusline. The hook is the only thing that runs automatically, and it only reads `EXPERIMENTS.md`.

## What it enforces

| Rule | Why it matters |
|---|---|
| Labeled hypotheses (H1..Hn) with explicit nulls | Assertions stop being free-floating claims |
| Predictions before measurement | Blocks post-hoc rationalization |
| Cheapest falsification first | One probe beats five agents arguing |
| Controls and baselines mandatory | Correlation is not a finding |
| REFUTE-first adversarial gate | Author of a finding cannot referee it |
| Calibrated confidence (0.90+ needs ground truth) | Confidently-wrong is worse than inconclusive |
| Persistent ledger (`EXPERIMENTS.md`) | Killed ideas stay killed across sessions |

## Workflow at a glance

Each stage maps to a command you can run alone, or that `investigate` chains for you. Full detail: [Workflow](https://github.com/88plug/scientific-method/blob/main/workflow.md).

| Stage | What happens |
|---|---|
| Hypothesis | Assertion → labeled falsifiable claim + null |
| Prediction | Outcome→conclusion table, written before measuring |
| Experiment | Cheapest controlled probe that can falsify the claim |
| Refute | Adversarial attack on surviving findings |
| Verdict | `confirmed` / `prototype` / `research` / `kill` |
| Ledger | Persist so DO-NOT-RE-ATTACK entries never restart |

## Commands

| Command | What it does |
|---|---|
| `/scientific-method:investigate <problem>` | Full campaign: hypotheses, probes, verdicts, ledger |
| `/scientific-method:falsify <claim>` | Attack an asserted limit, ceiling, or claim |
| `/scientific-method:invent <problem>` | Invention campaign past a confirmed limit |
| `/scientific-method:verdict [claims]` | REFUTE-first review before you act on a finding |
| `/scientific-method:ledger [sync]` | Create or update the hypothesis ledger |
| `/scientific-method:council <question>` | Multi-model council; dissent + factual cruxes → probes |
| `/scientific-method:peer-review <work>` | Blind lensed review + rebuttal + area-chair decision |

Full reference: [Commands](https://github.com/88plug/scientific-method/blob/main/commands.md).

## Agents

These fan out under campaigns. You can also invoke them directly. Full detail: [Agents](https://github.com/88plug/scientific-method/blob/main/agents.md).

| Agent | Role | Typical parent |
|---|---|---|
| `experiment-designer` | Design one hypothesis, probe, and outcome table (does not run it) | `investigate`, `falsify` |
| `refuter` | Try to kill a finding; return confirmed / prototype / research / kill | `verdict`, invent pipeline |
| `council-member` | One independent council seat: position, evidence, would-change-my-mind | `council` |
| `peer-reviewer` | One blind, execution-grounded review with a lens and scores | `peer-review` |
| `meta-reviewer` | Area chair: evidence over votes; final accept/revise/reject | `peer-review` |

<details>
<summary>Skill and hook</summary>

- **`scientific-method` skill** — the method itself, artifact templates, and multi-agent campaign patterns. Auto-triggers on phrases like "prove it", "root cause this", "no guessing", or any challenge to an asserted number, limit, or cause.
- **SessionStart hook** — if `EXPERIMENTS.md` exists, surfaces the ledger so killed hypotheses stay killed. Read-only; silent no-op when the file is absent.

</details>

## How to trigger

Run any command above, or let the skill auto-trigger. It activates on phrases like "use the scientific method", "prove it", "validate these claims", "root cause this 100%", "no guessing", or any challenge to an asserted number, limit, or cause.

!!! tip
    When you want a finding double-checked before you act on it, run
    `/scientific-method:verdict` — it puts the claim through the REFUTE-first
    gate without rerunning the whole campaign.

## Install from a local clone

```text
git clone https://github.com/88plug/scientific-method
/plugin marketplace add ./scientific-method
/plugin install scientific-method@88plug
```

## Updating

This plugin ships rolling — every commit is a release. Your installed version (`claude plugin list`) and the one in the [88plug catalog](https://github.com/88plug/claude-code-plugins) are shown as `vYEAR.MONTH.BUILD`; if they differ, run `/plugin update scientific-method@88plug`. With marketplace auto-update enabled, you always get the latest automatically.

## Contributing

Issues and pull requests are welcome at [88plug/scientific-method](https://github.com/88plug/scientific-method). The [plugin-validate](https://github.com/88plug/scientific-method/actions/workflows/plugin-validate.yml) workflow runs on every change — make sure it passes before you open a PR.

## License

[FSL-1.1-ALv2](https://github.com/88plug/scientific-method/blob/main/LICENSE) © 2026 [88plug](https://github.com/88plug) —
Functional Source License; converts to Apache 2.0 two years after each release.

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

## Development

Local clone for contributors (marketplace install above is preferred):

```text
git clone https://github.com/88plug/scientific-method
/plugin marketplace add ./scientific-method
/plugin install scientific-method@88plug
```
