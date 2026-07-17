# Commands

All commands are namespaced under `scientific-method:`. Run them from Claude Code after installing the plugin.

## Commands table

| Command | Argument | What it does |
|---|---|---|
| [`investigate`](#investigate) | `<problem>` | Full campaign: hypotheses, controlled experiments, verdicts, ledger |
| [`falsify`](#falsify) | `<claim>` or `all` | Attack an asserted limit, ceiling, or claim with designed probes |
| [`invent`](#invent) | `<problem>` | Invention campaign past a confirmed limit |
| [`verdict`](#verdict) | `[claims]` | Adversarial REFUTE-first review before trusting findings |
| [`ledger`](#ledger) | `[sync]` | Create or update the persistent hypothesis ledger |
| [`council`](#council) | `<question>` | Multi-model council; dissent + factual cruxes → probes |
| [`peer-review`](#peer-review) | `<work>` | Blind lensed reviewers, rebuttal, area-chair decision |

## investigate

```text
/scientific-method:investigate the API returns 500 under load but not in tests
```

Full falsification-first investigation. Contract:

1. Cheapest probe first.
2. Hypothesis ledger — every candidate as a numbered falsifiable claim with null; check DO-NOT-RE-ATTACK first.
3. Predict, then probe — outcome tables before measuring; controls for causal claims; baselines for performance claims.
4. Verdicts with evidence and calibrated confidence.
5. Adversarial pass via the [refuter](agents.md#refuter).
6. Loop until clean (dry pass, all verdicts filled).

If no problem is given, investigates the most recently discussed open question.

## falsify

```text
/scientific-method:falsify the bidirectional PCIe aggregate is 32.9 GB/s
/scientific-method:falsify all
```

Attack an asserted limit, ceiling, or claim. With `all` (or empty), sweeps docs/benchmarks/conversation for every "ceiling", "wall", "maximum", "can't", "impossible", and derived formula.

Derived numbers (X/2, spec-sheet values, library metadata) are prime targets — past campaigns falsified four of five asserted "physical" walls.

A confirmed limit is as valuable as a broken one: it ends a search honestly.

## invent

```text
/scientific-method:invent break the measured encode ceiling past 12.2% with acceptance ≥ +2pp over tuned baseline
```

Full invention campaign:

1. Frame falsifiable acceptance criteria; measure the baseline first.
2. Ideate with quotas and forced diversity.
3. Refute before building; kills go to the falsification log.
4. Build and measure survivors against pre-registered criteria.
5. Provenance-search every surviving mechanism.
6. Certify and ledger; high-stakes inventions go to peer-review.

## verdict

```text
/scientific-method:verdict
/scientific-method:verdict the outage was caused by the 14:00 deploy
```

The gate between "we found something" and "we act on it / report it externally". Spawns one fresh [refuter](agents.md#refuter) per claim. Empty argument collects load-bearing claims from the conversation.

Report: verdict table, kills with reasons (appended to the falsification log), surviving claims with calibrated confidence.

## ledger

```text
/scientific-method:ledger
/scientific-method:ledger sync
```

Maintain `EXPERIMENTS.md` (or the project's incident/docs convention):

- Create from the skill's artifact template if missing.
- `sync` backfills untracked findings from the conversation.
- Integrity check: demote verdicts without evidence; recalibrate 100% confidence with named unknowns; spot-check Reproduce commands.

Keep it append-only. The audit trail — including wrong turns — is what makes verdicts trustworthy.

## council

```text
/scientific-method:council should we ship the rewrite or keep patching the hot path?
```

Convene a model council for **judgment calls**, not empirical questions:

1. Frame the question with evidence; do not include your own lean.
2. Seat 3–5 [council-member](agents.md#council-member) agents on different models, blind to each other.
3. Optional out-of-family seat via `COUNCIL_OOF_ENDPOINT` (local OpenAI-compatible endpoint).
4. Aggregate by evidence. Factual disagreements become ledger hypotheses with probes.

## peer-review

```text
/scientific-method:peer-review the encode-pipeline invention in EXPERIMENTS.md
```

True peer review after the refute gate, before build/merge/publish:

1. Assemble submission packet (claim + all evidence + working Reproduce block).
2. Round 1 — 3–5 blind [peer-reviewer](agents.md#peer-reviewer) agents with distinct lenses.
3. Rebuttal — answer with new evidence or applied revisions only.
4. Re-score, then [meta-reviewer](agents.md#meta-reviewer) area-chair decision.

Decision maps to the ledger: accept → CONFIRMED; reject → falsification log with DO-NOT-RE-ATTACK.
