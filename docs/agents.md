# Agents

Five specialized agents fan out under campaigns. Each has a narrow contract and a structured return format the orchestrator consumes raw. You can also invoke them directly by name.

## Agents table

| Agent | Color | Tools | Role |
|---|---|---|---|
| [`experiment-designer`](#experiment-designer) | blue | Read, Grep, Glob, Write, WebFetch | Design one hypothesis + probe + outcome table — does **not** run it |
| [`refuter`](#refuter) | orange | Read-only (no Write/Edit) | Try to kill a finding first; return confirmed / prototype / research / kill |
| [`council-member`](#council-member) | purple | Read-only (no Write/Edit) | One independent council seat: position, evidence, would-change-my-mind |
| [`peer-reviewer`](#peer-reviewer) | yellow | Read-only (no Write/Edit) | One blind, lensed, execution-grounded review with scores |
| [`meta-reviewer`](#meta-reviewer) | red | Read, Grep, Glob | Area chair: evidence over votes; final accept/revise/reject |

## experiment-designer

Turns one asserted limit, claim, or candidate root cause into a rigorously designed experiment — without running it.

**When to spawn:** one per hypothesis when fanning out a falsification campaign. The parent runs probes serially so measurements do not contaminate each other (device contention, cache state, cross-talk).

**Returns, in order:**

1. **HYPOTHESIS** — falsifiable claim, prediction, explicit null H0
2. **EXPERIMENT** — probe file path, how to run it, expected runtime, controls applied
3. **OUTCOME TABLE** — outcome → what it proves → next action (all plausible results)
4. **UNLOCKS** — what becomes possible if the assertion falls; what search closes if confirmed

Design discipline: name the suspected flaw in how the original assertion was produced (single-stream artifact, hot cache, derived formula, vendor default). Prefer the cheapest probe that fully discriminates the outcomes.

Used by: `/scientific-method:investigate`, `/scientific-method:falsify`.

## refuter

Evaluates a finding by attempting to **refute it first**, then judging what survives. Fresh context is the point — the author of a finding must not referee it.

**When to spawn:** one fresh refuter per claim, before acting on any finding, sending conclusions externally, merging a "fix", or relaying research-agent results the parent has not independently verified.

**Verdict enum:**

| Verdict | Meaning |
|---|---|
| `confirmed` | Survived refutation; evidence chain complete; safe to act on |
| `prototype` | Promising but needs exactly one more measurement — name it |
| `research` | Real but speculative or not feasible here yet |
| `kill` | Refuted, physically impossible, unbuildable, or no real gain (`kill_reason` required) |

**Classic holes it hunts:**

- Per-component win presented as end-to-end win
- Correlation without a control case
- Derived/spec-sheet number presented as a measurement
- Missing baseline (regression could hide inside the "improvement")
- Internal contradictions between sources
- Claims above a measured physical ceiling

Used by: `/scientific-method:verdict`, invent pipeline, end of investigate campaigns.

## council-member

One independent seat on a deliberative council. Several models get the same question; seats are blind to each other. The value is an *independent* path to an answer — dissent is the point.

**When to spawn:** 3–5 seats in parallel for judgment calls (design decisions, interpretation of ambiguous results, risk assessments, go/no-go). Do **not** use a council to settle purely empirical questions — those go to experiments.

**Ground rules:**

- Probe before opining (read-only access to code/config/data).
- Separate fact from judgment; name the probe that would settle unmeasured facts.
- Commit to a position; "it depends" without naming what it depends on is a non-answer.

**Returns exactly:**

```text
POSITION: <one-sentence answer/recommendation>
KEY EVIDENCE: <2-4 observations/probes with refs>
REASONING: <causal chain from evidence to position>
STRONGEST COUNTERARGUMENT: <best case against your own position>
CONFIDENCE: <0-1; 0.90+ only if grounded in direct evidence you checked>
WOULD CHANGE MY MIND: <specific observation that would flip you>
UNRESOLVED EMPIRICAL QUESTIONS: <facts + exact probes>
```

Used by: `/scientific-method:council`. Orchestrator aggregates by evidence not votes; factual cruxes become ledger hypotheses with probes.

## peer-reviewer

One independent reviewer in a peer-review round for an invention, design, finding, or paper-style writeup. Each reviewer gets the same submission packet plus **one** assigned lens and works blind to the others.

**Lenses:**

| Lens | What it executes |
|---|---|
| `soundness` | Logic chain, controls, confounds, causal ladder |
| `prior-art/provenance` | Actual search log; closest found vs claimed novelty |
| `reproducibility` | Run the Reproduce block; check provenance header |
| `significance` | Does the gain matter end-to-end? |
| `fatal-flaw` | Always assigned — hunts the single blocker |

Reviews are execution-grounded: run the Reproduce block, search prior art, or re-derive the numbers depending on lens. Return structured scores plus accept/revise/reject.

Used by: `/scientific-method:peer-review` (3–5 in parallel after refute gate, before build/merge/publish).

## meta-reviewer

The area chair who closes a peer-review round. Receives the submission packet, all independent reviews, the author rebuttal, and any re-scores. Issues the final decision.

**How it weighs:**

- **Evidence beats votes.** One reviewer who ran the Reproduce block and watched it fail outweighs three approving skims.
- **Rebuttal against reviews, not fluency.** Blocking weaknesses answered only with new evidence or applied revisions.
- **Disagreement is information.** Factual splits become named probes in the decision's requirements — not adjudicated by the chair.

**Decision enum:** `accept` / `minor-revision` / `major-revision` / `reject`, with camera-ready requirements. Maps straight to the ledger (accept → CONFIRMED; reject → falsification log with DO-NOT-RE-ATTACK).

Spawn exactly one, after rebuttal, never before all reviews are in.

Used by: `/scientific-method:peer-review`.

## Skill

The `scientific-method` skill is the method itself. It carries:

- The full campaign loop (hypothesis → ledger)
- Artifact templates (`references/artifacts.md`)
- Multi-agent campaign patterns (`references/campaigns.md`) — design/execute split, invent pipeline, council and peer-review contracts
- Anticipation generators, rigor checks, causal structure, open-records playbook

It auto-triggers on phrases like "use the scientific method", "prove it", "validate these claims", "root cause this", "no guessing", "falsify", "invent", or any challenge to an asserted number, limit, or cause — and proactively before the model asserts a ceiling or root cause of its own.
