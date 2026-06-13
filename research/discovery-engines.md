# Machine Discovery Engines: Architecture Lessons for the Plugin

Automated systems have produced *verified-new*, human-competitive results — not
by being smarter generators, but by pairing a high-volume generator with a
**mechanical, ungameable verifier** inside a selection loop. The lesson for this
plugin is structural: our acceptance-gated sims and eval-harness ground truth are
the same verifier, and Pattern B is the same generate→refute→keep-frontier loop.

---

## The common architecture: GENERATOR + mechanical VERIFIER + selection loop

Every system below reduces to the same three parts. What they share is that the
verifier is **execution, not persuasion** — a candidate either satisfies an
objective check or it is discarded, and no amount of fluent rationale moves it.

| System | Generator | Mechanical verifier | Selection | Verified-new result |
|---|---|---|---|---|
| **FunSearch** (DeepMind, 2023) | LLM mutates a function slotted into a fixed skeleton, prompted with prior high-scorers | Runs the program; scores by objective (e.g. *is this a valid cap set, how large?*) | Island-based evolution over a program DB; favors high scorers, forces diversity | New cap set of size 512 in dim 8 (beat known constructions); better online bin-packing heuristics |
| **AlphaEvolve** (DeepMind, 2025) | Gemini-class LLM produces code variants of an existing algorithm | User-supplied **evaluation function**: executes candidate, scores against objective metrics — "evaluate code programmatically, reducing reliance on human input" | Keeps top scorers to seed next generation | Improved 50 open math problems (SOTA 75%, *improved* 20%, incl. kissing number); recovered 0.7% of Google fleet's stranded compute; faster Gemini training kernel |
| **AlphaDev** (DeepMind, 2023) | AlphaZero RL agent appends assembly instructions (search as single-player game) | Correctness + latency reward; true latency measured on <0.002% of programs; **independent vetting** before merge | MCTS/value-network self-play | Shorter sort routines (VarSort4 −29 instrs) merged into **LLVM libc++** — first change in a decade; faster Abseil hashing, run trillions of times/day |
| **Genetic programming** (Koza et al.) | Population of evolved programs, crossover + mutation | Fitness function executes each program against the spec | Tournament/fitness selection over generations | 70+ human-competitive results; multiple **patented / re-invented** circuits and controllers (GECCO "Humies") |

**Four invariants that make these engines work — and map onto the plugin:**

1. **The verifier is mechanical and ungameable.** Correctness is decided by
   running the candidate, not by a model judging itself. A hallucinated or wrong
   answer *fails verification* — it cannot talk its way past. FunSearch's evaluator
   "simply runs the program"; AlphaEvolve scores "programmatically … mitigating
   hallucination." This is precisely our **acceptance-gated simulation**: the gate
   is the objective oracle, and the agent is graded against ground truth it cannot
   see or edit.
2. **Generation is high-volume + diversity-forced.** Thousands of candidates, with
   an explicit anti-collapse mechanism — FunSearch's *islands*, GP's population
   diversity — so the search doesn't converge to one local optimum. One brilliant
   guess is worth less than a wide, varied stream.
3. **Selection keeps the verified frontier.** Only candidates that *passed* the
   mechanical check seed the next round. The kept set is the moving frontier of
   what is provably better; everything else is dropped, not argued over.
4. **Programs/artifacts are human-auditable.** Outputs are inspectable code, not
   opaque weights — researchers can read, simplify, and re-verify them. Mechanical
   verification + human auditability is the trust stack.

---

## Koza's 8 criteria — the bar for claiming a real invention

A result is **human-competitive** if it satisfies *at least one*. This is the bar
a Pattern B survivor should clear before we call it an invention rather than a tidy
idea. (Source: human-competitive.org / GECCO "Humies".)

- **(A)** Was patented, improves a patented invention, or would qualify today as a patentable new invention.
- **(B)** Matches/exceeds a result accepted as new when published in a peer-reviewed journal.
- **(C)** Matches/exceeds a result in a database/archive maintained by an internationally recognized expert panel.
- **(D)** Could be published on its own merits as a new finding — *independent of the fact that it was mechanically created*.
- **(E)** Matches/exceeds the most recent human solution to a long-standing problem with a succession of better human solutions.
- **(F)** Matches/exceeds a result considered an achievement in its field when first discovered.
- **(G)** Solves a problem of indisputable difficulty in its field.
- **(H)** Holds its own or wins a regulated competition against human contestants (live or human-written programs).

**The teeth are in (D):** the result must stand *on its merits*, stripped of the
romance of having been machine-generated. That is exactly the refuter's job in
Pattern B — strip the "we invented something" framing and ask whether the artifact
beats the **measured baseline** on its own.

---

## Mapping onto plugin assets

**Pattern B (Ideate → Refute → Synthesize) is a discovery engine with a human-or-agent verifier.**
The correspondence is one-to-one:

| Discovery-engine part | Pattern B element | Tightening from the engines |
|---|---|---|
| Generator (high-volume, diverse) | **Phase 1 Ideate** — one agent per lens, grounded in measured baselines | Force diversity like FunSearch islands: distinct lenses (each wall, self-audit, consumer contract, what competitors can't do) are our anti-collapse mechanism. More lenses, more candidates. |
| Mechanical verifier | **Phase 2 Refute** — fresh agent per idea, inventor can't referee its own | This is the engines' core lesson. The refuter must reduce to a **mechanical check** wherever possible (does it beat the *measured* baseline? buildable HERE? read-only probes), not a debate. "Default to the lower verdict" = fail-closed verification. |
| Selection / verified frontier | **Phase 3 Synthesize** — rank survivors, send kills to falsification log as DO-NOT-RE-ATTACK | Keeping the verified frontier *and* recording kills is exactly the program DB: survivors seed forward, kills are pruned permanently. |
| Human-competitive bar | (missing — add) | Gate `verdict: confirmed`/`prototype` on **at least one Koza criterion (esp. D)**: does it beat the most recent human/measured baseline on its own merits? If it only matches the baseline, it's not an invention. |

**Eval-harness (`eval-workspace/`) is the plugin's own mechanical verifier — already built right.**
Each `iteration-N/` holds `scenarios/` (the prompts/inputs), `ground_truth/` (the
ungameable oracle the agent never sees), and per-run `eval_metadata.json` with
`with_skill/` transcripts. This is FunSearch's evaluator applied to the skill
itself: the skill is the *generator*, the scenarios + hidden ground truth are the
*mechanical verifier*, and successive `iteration-N/` dirs are the *selection loop*
keeping the verified frontier of skill versions. Scenario design (e.g.
`r5s02_true_naive`, `r5s05_base_rate`, `r5s10_amdahl`) is adversarial-by-construction
— the same ungameability principle as an acceptance-gated sim.

**Concrete upgrades suggested by the engines:**

1. **Make the refute gate mechanical, not rhetorical.** Wherever an idea touches
   something runnable, the refuter should *run an acceptance-gated sim / read-only
   probe* and gate on its objective output — not adjudicate prose. Borrow
   FunSearch: "the evaluator simply runs it."
2. **Add the Koza-(D) test to the verdict schema.** A new field like
   `beats_measured_baseline_on_own_merits: true|false` (with the baseline named)
   makes "is this a real invention?" a checkbox, not a vibe.
3. **Force generation diversity explicitly.** Treat Pattern B lenses like islands:
   require N distinct lenses and forbid two ideas attacking the same wall the same
   way — diversity is what stops premature convergence in every engine above.
4. **The frontier is the kept set + the kill log together.** Persisting kills as
   DO-NOT-RE-ATTACK is the pruned half of the program DB; keep doing it, and seed
   future Ideate phases from the surviving frontier, not from scratch.

**Caveat:** these engines win in domains with a *cheap, exact* oracle (valid cap
set? sort correct? latency measured?). The plugin's edge depends on how mechanical
we can make the refuter — the closer our acceptance gates get to FunSearch's
"run it and score it," the more Pattern B behaves like a real discovery engine
rather than a structured brainstorm.
