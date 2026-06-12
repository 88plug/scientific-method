# Multi-agent campaign patterns

Fan-out patterns for campaigns too big for one context: many hypotheses,
fleet-wide forensics, ceiling-breaking sweeps. Both patterns below are lifted
from real campaigns that worked. Use the plugin's `experiment-designer` and
`refuter` agents (or embed the contracts below in your own prompts).

Scale agent count to stakes the way the originals did: 3 agents to validate
claims, 5 for a pre-go-live review, 10 for "root cause this completely".

---

## Pattern A — Falsify-the-limits (design/execute split)

One agent per asserted limit. Agents DESIGN experiments; the parent RUNS them
serially so numbers are clean (no device contention, no cross-talk).

Shared preamble (adapt the bracketed parts):

```
We have been ASSERTING limits without rigorously testing them. [State the
specific assertion that was already contradicted by a real measurement, if
any — this motivates the campaign.] Apply the scientific method — do not
assume.

YOUR JOB: take your assigned ASSERTED LIMIT, treat it as a falsifiable
HYPOTHESIS, and DESIGN A RIGOROUS EXPERIMENT to test/break it. WRITE the
experiment as a self-contained probe (script/microbenchmark) to a file under
[probe dir]. DO NOT RUN [expensive/contended resource] code — the parent
runs all experiments sequentially for clean numbers.

DELIVER:
(1) the hypothesis — what limit, what you predict happens, and the explicit
    null H0 (what you'd observe if the limit is real)
(2) the experiment file path you wrote
(3) an outcome table: what each possible result PROVES, and the action it
    justifies
(4) what it unlocks if the limit falls
```

Per-agent assignment: one falsifiable claim each, with concrete numbers and
the suspected flaw in the original measurement ("that was a single-buffer,
single-stream artifact").

Parent then: run probes serially → fill verdicts into the ledger → write the
walls doc (see artifacts.md). Don't run the designed probes in arbitrary
order: rank them by expected information gain and run the most informative
first — its result reshapes which remaining probes are worth running at all.
Structure multi-wave campaigns as a halving ladder (cheapest falsifier for
all, expensive probes for survivors only), and when sweeping a knob space,
sample randomly, never on a grid (rigor.md §1).

---

## Pattern B — Ideate → Refute → Synthesize (adversarial gate)

For "invent past the wall" or "what are we missing" campaigns. Three phases;
an idea only advances if it survives an attempt to refute it.

**Phase 1 — Ideate** (one agent per lens). Ground every agent in the measured
baselines first; forbid claims above measured ceilings. Useful lenses: each
measured wall; "audit our own prior verdicts for soft walls mislabeled as
hard" (self-audit lens — past campaigns found their best wins here); the
consumer/producer contract; what competitors can't do.

Idea schema:

```json
{
  "name": "...",
  "wall": "which measured baseline this attacks",
  "mechanism": "the concrete mechanism",
  "beats_wall_because": "the physical/architectural reason it gets past the measured wall",
  "feasible_here": true,
  "est_effect": "...",
  "provenance": "known technique (named) | no prior art found (search log ref) | unsearched",
  "risk": "..."
}
```

**Phase 2 — Refute** (one fresh agent per idea — fresh context is the point;
the inventor cannot referee its own idea). Wherever an acceptance probe or
sim exists, the refuter RUNS it — a mechanical pass/fail is immune to fluent
rationale; prose adjudication is the fallback, not the default. Prompt core:

```
An engineer proposes this finding/invention. Your job is to REFUTE it first,
then judge what survives. Be skeptical: does it actually beat the measured
baseline, or does it secretly still pay it? Is the per-component win also an
end-to-end win under the binding constraint? Is it truly buildable HERE
(check installs/hardware — read-only probes allowed)? Default to the lower
verdict when uncertain. Kill anything physically impossible or hand-wavy.
```

Verdict schema:

```json
{
  "name": "...",
  "verdict": "confirmed | prototype | research | kill",
  "stands_on_own_merits": "does it beat the tuned baseline on the prior art's terms (Koza's test)?",
  "physically_sound": true,
  "feasible_here": true,
  "realistic_gain": "honest expected gain after skepticism — may be 'none'",
  "reasoning": "the refutation attempt and what survived it",
  "kill_reason": "required when verdict=kill"
}
```

**Phase 3 — Synthesize** (one agent): rank survivors by impact × feasibility,
list the kills with reasons (they go to the falsification log as
DO-NOT-RE-ATTACK), produce the build/action plan.

Workflow-tool sketch (pipeline so refutes start as ideation lenses finish):

```js
const results = await pipeline(
  LENSES,
  l => agent(ideatePrompt(l), {label: `ideate:${l.key}`, phase: 'Ideate', schema: IDEA_SCHEMA}),
  out => parallel(out.inventions.map(i => () =>
    agent(refutePrompt(i), {label: `refute:${i.name}`, phase: 'Refute', schema: VERDICT_SCHEMA})
      .then(v => ({...i, verdict: v}))))
)
const survivors = results.flat().filter(Boolean).filter(r => r.verdict?.verdict !== 'kill')
```

---

## Pattern C — Forensic investigation (controls + confidence contract)

For root-cause work over logs/metrics/history. Each agent gets one
prove-or-disprove question with the control built into the prompt:

```
Prove or disprove: <causal claim>.
1. Did <suspected cause> actually occur on ALL affected items in the window?
   If only some, the causation theory is wrong — say so.
2. CONTROL CASE: were there items where <suspected cause> occurred but the
   symptom did NOT? Find them.
   2b. DOSE-RESPONSE: does more of the suspected cause yield more symptom?
   2c. TEMPORALITY: did the cause precede the symptom in EVERY case? A
       causal claim without temporality is dead on arrival.
3. Confidence rating (0-1) that <cause> triggered <effect> — and where the
   evidence sits on the causal ladder (correlation / temporality /
   dose-response / controlled experiment).
4. If confidence < 0.9: what is the remaining unknown, and what exact query
   would close it?
```

Two traps on observational causal claims (rigor.md §3): an aggregate effect
can reverse inside a segment — check segmentation before declaring a single
cause; and a before/after delta needs a **parallel-trends check** (would the
control group have moved the same way absent the treatment?) before it
counts as anything more than correlation.

Conventions that made these investigations land:
- **Replication across samples**: reproduce the symptom on ≥3 independent
  items before calling it a pattern.
- **Synchronized-burst evidence**: N hosts flipping within seconds across
  heterogeneous hardware is control-plane-grade proof — name the window.
- **Escalate to ground truth** when logs only suggest: disassemble the
  binary, read the silicon, fetch the primary source. The gap between "logs
  suggest a missing Clear()" and "the binary has no Clear()" is the gap
  between hypothesis and filed bug.
- **Verification vs discovery tool split**: agents synthesizing a verdict get
  cheap confirmatory tools; agents generating hypotheses get the expensive
  exploratory ones. A synthesizer with discovery tools never converges; an
  investigator with only verification tools rubber-stamps the first
  plausible story.
- Final pass before reporting externally: a review wave that loops while it
  keeps finding defects ("found stuff → there may be more → again until
  clean").

---

## Pattern D — Model council (decorrelated judgment)

For judgment calls — design choices, ambiguous-result interpretation,
go/no-go — where the risk is a shared blind spot, not a missing measurement.
One model asked twice gives the same prior twice; different tiers and
especially a different model family fail differently.

Patterns D and E are the campaign's **experiment review board** — but a
review board can only judge a working experiment. Run the pre-flight trust
checks (allocation sanity, A/A, Twyman's law — rigor.md §4) *before*
convening either; reviewers asked to interpret a broken experiment produce
confident nonsense.

- 3-5 `council-member` seats spawned in parallel with different `model`
  overrides (haiku / sonnet / opus / inherit), identical question packet,
  blind to each other and to the orchestrator's lean.
- Optional out-of-family seat: a local OpenAI-compatible endpoint (probe
  reachability first, e.g. `curl -s --max-time 5 <host>/v1/models`; configure
  via `COUNCIL_OOF_ENDPOINT` or the project's docs). POST the same packet +
  council-member output contract to `/v1/chat/completions`. This seat can't
  run probes — weigh it accordingly. Skip silently if down.
- Aggregate by evidence, not votes: weigh seats by what they actually
  probed. Unanimity with no probes behind it = shared prior → run the
  cheapest "would change my mind" probe before adopting.
- Dissent is the product: factual cruxes become ledger hypotheses with
  probes (the council routes empirical disputes to experiments — it never
  votes facts); judgment cruxes get decided on the record with minority
  positions preserved.
- Feedback loop: surviving counterarguments are applied as corrections to
  the artifact/claim immediately; optionally reconvene seats on the revised
  version with the diff.

Seat output contract: `POSITION / KEY EVIDENCE / REASONING / STRONGEST
COUNTERARGUMENT / CONFIDENCE / WOULD CHANGE MY MIND / UNRESOLVED EMPIRICAL
QUESTIONS` (see the council-member agent).

---

## Pattern E — Peer review (correction round for inventions)

After Pattern B's refute gate, before build/merge/publish/external send.
Refutation asks "is this wrong?"; peer review asks "what must change before
anyone builds on it?" — and the changes get applied during the round.

- Submission packet: claim + ALL evidence + working Reproduce block, with
  author-confidence language stripped (review the evidence, not the
  enthusiasm). No Reproduce block → not reviewable; build it first.
- Round 1: 3-5 blind `peer-reviewer` agents in parallel, one lens each —
  `soundness`, `prior-art/provenance`, `reproducibility`, `significance`, and
  always `fatal-flaw`. Execution-grounded: reproducibility RUNS the
  Reproduce block; prior-art actually searches (including the project's own
  falsification log for DO-NOT-RE-ATTACK collisions); soundness re-derives
  the numbers. Vary models across reviewers at high stakes.
- Rebuttal = corrections: every `blocking` weakness answered with (a) a new
  measurement run now, (b) a revision applied now (reference the diff), or
  (c) a documented concession in the writeup. Words alone don't move scores.
- Re-score via SendMessage to the same reviewers (they keep context), then
  one `meta-reviewer` area chair: weighs evidence over votes (one failed
  reproduction outweighs three approving skims), flags rounds where nobody
  executed anything as failed rounds.
- Decision mapping to the ledger: accept → CONFIRMED; minor-revision →
  prototype (apply + verify revisions now); major-revision → weaknesses
  become new hypotheses, revised work gets a FRESH review round; reject →
  falsification log, DO-NOT-RE-ATTACK, kill_reason + reopen condition.
- Report the delta, not the score: how the work is concretely better than
  before the round.

---

## Reporting contract (all patterns)

Agents return, in order: hypothesis (with H0) → evidence/probe → outcome
mapped through the pre-committed table → verdict + calibrated confidence →
named residual unknowns with exact next probes. Negative and inconclusive
results are deliverables, not failures to report.
