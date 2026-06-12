# Causal structure: loops, joint causes, and structured differencing

The core loop's causal machinery (but-for controls, temporality, dose-response
— rigor.md §3) assumes linear, separable causation: a cause node you can point
at, preceding its effect. Real systems break that assumption two ways —
feedback loops and jointly-necessary causes — and several traditions converged
on the same repairs. Everything here still ends as ledger rows with probes;
structure changes *which* hypotheses exist, not the standard of proof.

## 1. When to stop hunting a broken component

Switch from component-hunt to **control-loop modeling** (STAMP's reframe:
accidents as inadequate control, not failure chains) when any of these hold:

- Every component met its spec and the loss still happened.
- Two or more controllers act on shared state (autoscaler + operator,
  retry layer + rate limiter, cache + invalidator).
- The symptom is oscillation, runaway, or overshoot-then-collapse — feedback
  signatures, not breakage signatures.

Model the loop in text: controller → action → process → sensor → controller,
and mark each arrow that has a **delay** (`//`). The central failure mode to
hunt is the **process-model gap**: the controller's belief about the system
diverged from the real state, so it issued an action it believed was safe.
That gap is probe-able — log the controller's view next to ground truth.

- **Delay-corrected temporality.** In a delayed loop, the event just before
  the symptom is usually the loop *feeding back*, not the cause — the real
  trigger sits roughly one delay-length earlier. Naive temporality checks
  point at the wrong arrow; a loop-breaking control (open the loop, pin the
  signal, canary one side) is mandatory before any temporal verdict.
- Hypotheses become claims about **loop dominance** ("the reinforcing retry
  loop dominates above 80% saturation"), falsified by a counter-reading or a
  config-flip canary like any other claim.
- **Choose the fix by leverage** (Meadows): changing a parameter (retry count)
  is the weakest intervention; changing loop gain, delays, or information flow
  (retry *budget*, request coalescing, back-pressure) is stronger. Pre-commit
  the expected short-term AND long-term effect signs — delayed loops routinely
  flip sign (better-before-worse, or the reverse), and a fix judged only on
  its first week is a Forrester trap. If a "fix" decays, suspect policy
  resistance: the loop is compensating; rank the next fix higher on the
  ladder.

## 2. Joint causes: trees, cut sets, and the causal set

When evidence shows two or more conditions were each necessary and none
sufficient, a flat H1..Hn list misrepresents the structure. Use a small fault
tree: the loss at the top, AND/OR gates beneath, basic causes at the leaves.

- A **minimal cut set** is the smallest set of leaves that jointly produce the
  top event. A size-1 cut set is a single point of failure — top priority. A
  size-2 cut set *forces* the verdict to name both causes; "root cause +
  contributing trigger" demotion becomes structurally impossible.
- Falsifying a leaf prunes the tree — it maps onto the existing `ruled_out`
  list. Check **common-cause failures**: if two "independent" branches share a
  dependency (same disk, same config push, same clock), the tree's redundancy
  is an illusion.
- **"Root cause" is a stopping decision, not a discovery** (the
  complex-systems critique is right about this much): catastrophe in a complex
  system requires multiple necessary-but-insufficient failures, and where you
  stop digging is editorial. The repair that keeps decisive verdicts: attach
  verdicts to measurable **necessity and sufficiency claims** about each
  factor — those are controllable and decidable — and report the **causal
  set**, not a singular trunk. Beware the **hindsight-bias stopping point**:
  "human error" as a terminal cause is almost always a premature stop — ask
  what made the erroneous action look reasonable at the time.

## 3. Verdict taxonomy: proximate / root / contributing

Borrowed from mishap investigation, with per-tier confidence:

- **Proximate cause** — the event that directly produced the loss (often
  observable: high confidence cheaply).
- **Root cause(s)** — the condition(s) whose removal would have prevented it
  (the but-for test the loop already uses; usually needs the control case).
- **Contributing factors** — raised likelihood or severity without being
  necessary.

Tiered confidence is the honest form: "proximate CONFIRMED 0.95; root
INCONCLUSIVE 0.6, deciding probe is X" beats one blended number.

## 4. IS / IS-NOT — structured differencing (Kepner-Tregoe)

Before hypothesizing at all, specify the problem in four dimensions, each as
IS vs **could-plausibly-be-but-IS-NOT**:

| dimension | IS | IS-NOT (but could be) | what distinguishes them? |
|---|---|---|---|
| WHAT (object/defect) | | | |
| WHERE (system/segment) | | | |
| WHEN (onset/pattern) | | | |
| EXTENT (how many/how big) | | | |

The IS-NOT column is a built-in negative control: any candidate cause must
explain *both* columns — why it hit what it hit AND spared what it spared. A
cause that fails one spec line is falsified before a single probe runs. The
distinctions column (what is different about the IS side?) and the changes
question (what changed at the WHEN boundary?) are the generator.

## 5. ACH matrix — verdicts across ≥3 competing hypotheses (Heuer)

When three or more hypotheses compete, evaluate the **evidence against all of
them simultaneously** instead of one at a time:

- Build an evidence × hypothesis matrix; mark each cell consistent (C),
  inconsistent (I), or neutral (—). Work **across rows**: a row consistent
  with everything has zero diagnosticity — strike it, whatever it cost to
  obtain.
- The leading hypothesis is the one with the **fewest inconsistencies — least
  evidence against — not the most support**. Confirmation accumulates for
  several hypotheses at once; refutation discriminates.
- Sensitivity check: if the verdict hinges on one or two cells, those cells
  are the next probes (and the place to hunt deception/instrument error).
- Known limits (use as scaffolding, not an oracle): the matrix cannot surface
  a hypothesis nobody listed (run the generators in anticipate.md first), and
  it treats evidence rows as independent when they often aren't. Ties are
  routed to a probe, never a vote.

## 6. Second-order effects — before the fix ships

The ecology of action: an intervention enters the same loop-ridden system and
escapes its intentions. Before any irreversible step, one pass: what does the
fix feed back into? (Meadows' policy resistance, the cobra effect, Forrester's
better-before-worse.) Pre-register guardrails for the fix itself, stage the
rollout, and record the expected long-term sign next to the short-term one so
next quarter can tell whether the fix decayed or the system compensated.
