# Workflow

The scientific-method skill runs a falsification-first loop. Every asserted limit, cause, or claim is a hypothesis until measured. Confirmed limits are not endings — they are entry criteria for invention.

## The loop

```text
assertion → hypothesis → prediction → probe → verdict → refute → ledger
                              ↑                                      │
                              └──────── loop until clean ────────────┘
```

### 0. Cheapest falsification first

Before designing anything, ask: what single cheap observation could kill the leading hypothesis right now? One HTTP GET, one grep, one log query. Run it first. Agents arguing from priors while a two-second fetch sits unexecuted is the most expensive failure mode this method exists to prevent.

**Method weight scales with evidence cost.** A question one file-read answers gets a three-line mini-ledger, not a full H-table. Spend ceremony where uncertainty lives.

### 1. Hypothesis

Sweep assertions into numbered, labeled hypotheses:

- **Falsifiable claim** with concrete numbers where possible.
- **Explicit null (H0)** — what the world looks like if the claim is wrong.
- Include the *reversed* hypothesis when one explanation is suspiciously convenient.

Record them in the ledger immediately. Hypotheses that live only in conversation get silently mutated to fit results.

### 2. Prediction

Write the outcome→conclusion table *before* measuring:

| Outcome | What it proves | Next action |
|---|---|---|
| A | claim falsified | unlock the next lever |
| B | claim confirmed | close that search branch |
| C | confound | redesign the probe |

Every plausible outcome maps to a verdict and an action. If an outcome would not change what you do next, the experiment is not worth running.

### 3. Experiment

One isolated probe per hypothesis. Discipline that mattered in practice:

- Name confounds, then kill them (cache, contention, clock variance, run-order).
- Controls are mandatory for causal claims (but-for test).
- Baselines before treatments; report signed deltas, never bare points.
- Design/execute split on fan-outs: agents *write* probes; parent runs them serially so numbers stay clean.

The [`experiment-designer`](agents.md#experiment-designer) agent owns design-only work.

### 4. Verdict

Every hypothesis ends in exactly one of:

| Verdict | Meaning |
|---|---|
| **CONFIRMED** | Survived the probe; evidence chain complete |
| **FALSIFIED** | Probe killed it; real measurement replaces the assertion |
| **INCONCLUSIVE** | Decisive evidence missing — name the exact next probe |

Rules:

- INCONCLUSIVE is a first-class deliverable, not a failure.
- Emit confidence as a number (e.g. `confidence ~0.6`), not a verbal hedge.
- 0.90+ requires direct ground-truth proof. Never default to 0.85/0.95.
- Every verdict carries an evidence reference (command, log line, timestamp+value).

### 5. Refute

A finding you produced is a hypothesis someone else has not tried to kill yet. Before acting on it or reporting it externally:

- Spawn the [`refuter`](agents.md#refuter) agent (fresh context — the author cannot referee).
- Verdict enum: `confirmed` / `prototype` / `research` / `kill` (with `kill_reason`).
- Default to the lower verdict when uncertain.

`/scientific-method:verdict` runs this gate without replaying the whole campaign.

### 6. Ledger

Write findings to `EXPERIMENTS.md` (or the project's incident/docs convention):

- Hypothesis table: `| # | Hypothesis | Prediction | Probe | Verdict |`
- **Falsification log** — every dead end marked **DO-NOT-RE-ATTACK**
- **Reproduce** block with provenance (commit, machine, env, input hashes)
- **Scope corrections** left visible when you retract a claim

The SessionStart hook surfaces the ledger so killed ideas stay killed across sessions and compactions.

### 7. Loop until clean

Stop only when a full pass produces no new findings, every hypothesis has a verdict, and every INCONCLUSIVE names its missing probe. Before irreversible steps (go-live, vendor report, publish): one final adversarial review plus staged rollout where the domain allows it.

## Escalation gates

Two correction loops sit above refute. Both apply feedback to the work during the round — they do not file comments for later.

### Model council

For judgment calls (design choices, ambiguous results, go/no-go):

1. Frame the question with evidence; do not include your own lean.
2. Spawn 3–5 [`council-member`](agents.md#council-member) seats on *different models*, blind to each other.
3. Aggregate by evidence, not votes. Unanimity with no probes is a shared prior.
4. Factual disagreements are never voted on — the crux becomes a ledger hypothesis with a probe.

Command: `/scientific-method:council <question>`

### Peer review

For inventions/findings that survived refutation, before build/merge/publish:

1. Assemble a submission packet with a working Reproduce block.
2. Spawn 3–5 [`peer-reviewer`](agents.md#peer-reviewer) agents with distinct lenses, blind to each other.
3. Rebuttal answers only with new evidence or applied revisions.
4. [`meta-reviewer`](agents.md#meta-reviewer) issues the area-chair decision (evidence over vote counts).

Command: `/scientific-method:peer-review <work>`

## Invention continuation

A confirmed limit is the entry criterion for `/scientific-method:invent`:

1. Frame acceptance criteria against a measured baseline.
2. Ideate with forced diversity (TRIZ separations, recombination of partials).
3. Refute before building; survivors ranked by expected effect ÷ build cost.
4. Build, measure, provenance-search every surviving mechanism.
5. Certify on the ladder (asserted → functional → reproduced → certified).

## Failure modes this method prevents

- Asserting derived numbers as physical facts
- Premature closure from fatigue, not a dry pass
- Arguing from memory instead of measuring
- Manufactured closure under verdict pressure
- Blaming the convenient party without control cases
- Quietly absorbing a regression (missing baseline)
- Stopping at "human error" without the system conditions that made it look reasonable
