# TRIZ + Peircean abduction → adoptions for the scientific-method plugin

Research for the falsification-first investigation workflow. Sources: SEP *Abduction*
(plato.stanford.edu/entries/abduction/ + supplement `peirce.html`), SEP *Peirce*,
Wikipedia *TRIZ*, TRIZ40 principle list, and the standard TRIZ separation-principle
canon (Altshuller). CP citations are to Peirce's *Collected Papers*.

The plugin today is a strong **falsification** engine (refute, control, calibrate) but
a weak **generation** engine. Its loop starts at step 1 "convert assertions into
hypotheses" — it assumes the hypotheses already exist. TRIZ and Peirce both supply the
missing front half: *where do good hypotheses come from, and which do you test first.*
That is exactly the gap Pattern B (Ideate→Refute→Synthesize) gestures at but never
formalizes.

---

## Part 1 — Distilled principles

### TRIZ (Altshuller)

TRIZ was induced from studying patterns across global patent literature. Three empirical
findings ground it: problems/solutions repeat across industries; patterns of technical
evolution replicate across fields; breakthroughs resolve a contradiction rather than
optimize around it.

- **Technical contradiction** — improving one parameter degrades a *different* one
  (lighter mass ⇒ thinner material ⇒ higher failure risk). The classical **contradiction
  matrix** arrays 39 engineering parameters (improving × worsening) and, in each cell,
  names the **inventive principles** statistically most successful at resolving that
  pairing — mined from patents, not theorized.
- **Physical contradiction** — the *same* parameter must hold two opposite values
  (coffee hot to drink AND cold not to burn; landing gear present for landing AND absent
  in flight; chain rigid per-link AND flexible overall). This is the sharper, more
  resolvable form — and the one our performance ceilings actually are.
- **The 40 inventive principles** — a checklist of moves that historically broke
  contradictions. The most reusable for software/perf work: **#1 Segmentation** (divide
  into independent parts), **#3 Local quality** (make different parts do different jobs),
  **#10 Preliminary/prior action** (do the work before it's needed — precompute, prefetch),
  **#13 The other way round** (invert), **#15 Dynamics** (let a fixed property become
  adaptive), **#19 Periodic action**, **#20 Continuity of useful action**, **#35 Parameter
  changes** (change a phase/state — e.g. switch precision/representation).
- **Separation principles** — the four ways to dissolve a physical contradiction instead
  of trading it off. *This is the crown jewel for us:*
  - **Separation in TIME** — opposite values at different moments. Landing gear retracts.
  - **Separation in SPACE** — opposite values at different locations. Bridge rigid on the
    deck, flexible at expansion joints.
  - **Separation on CONDITION** — value depends on circumstance/interaction. A sieve is
    solid to pasta, open to water; photochromic lenses clear indoors, dark in sun.
  - **Separation between SYSTEM and COMPONENTS** — opposite properties at different scale
    levels. Each chain link rigid; the chain as a whole flexible.
- **Ideal Final Result (IFR)** — "the desired result is achieved by itself," with no added
  cost, complexity, or harm. The system delivers its function as if the mechanism weren't
  there. IFR is a *forcing function*: by demanding the ideal you refuse the compromise and
  are pushed toward a separation or an inventive principle rather than a trade-off curve.

The load-bearing TRIZ stance for us: **a trade-off ("we must accept X to get Y") is a
contradiction not yet resolved, not a law of physics.** That is the same energy as our
"every asserted ceiling is a falsifiable hypothesis" — applied to *ceilings of design*
rather than *ceilings of measurement*.

### Peirce — abduction as the logic of discovery

- **The triad / cycle of inquiry.** Inquiry runs **abduction → deduction → induction**.
  Abduction *generates* explanatory hypotheses; deduction "helps to derive testable
  consequences from the explanatory hypotheses that abduction has helped us to conceive";
  induction "finally helps us to reach a verdict on the hypotheses," the verdict depending
  on how many derived consequences are verified. (SEP, *Abduction* supplement.)
- **Abduction is the sole originary inference.** "Abduction is the process of forming
  explanatory hypotheses. It is the only logical operation which introduces any new idea"
  (CP 5.172). It covers "all the operations by which theories and conceptions are
  engendered" (CP 5.590). Deduction and induction can only elaborate or test ideas already
  on the table; *neither can put a new candidate into play.*
- **The syllogistic schema** (CP 5.189): "The surprising fact, *C*, is observed; but if
  *A* were true, *C* would be a matter of course; hence there is reason to suspect that
  *A* is true." Note the trigger is a **surprising fact** — abduction fires on
  *anomaly/surprise*, which is precisely what Twyman's law flags ("a surprisingly good
  number is a measurement bug until proven otherwise").
- **Economy of research** (CP vol. 7, esp. 7.220ff.). Hypothesis generation is unbounded
  but research labor is scarce, so it is "wasteful, indeed irrational, to squander"
  person-hours and apparatus; the aim is the "most cognitive bang for the buck" — to
  *maximize the reduction in indeterminacy of belief per unit cost* at every step. Peirce's
  selection criteria for which hypothesis to test first: **cost** (cheapness — test the
  cheap one first), **caution** (prefer a hypothesis you can break into small independently
  testable steps — Peirce's *Twenty Questions* analogy: a question that halves the field
  beats twenty narrow guesses), **breadth** (prefer hypotheses with wide explanatory
  reach), and **incomplexity** (prefer the simpler hypothesis). (SEP *Peirce*; criteria
  detailed in CP 7.)

**Peirce's economy of research IS our step 0** ("cheapest falsification first") — but
Peirce names two dimensions step 0 currently underweights: **caution** (decomposability —
the Twenty-Questions / halving structure, which we only invoke later as the "budget
ladder") and **breadth** (one probe that discriminates among many hypotheses beats one
that touches a single hypothesis).

### Polya (heuristics) — one transferable move

Polya's *How to Solve It* mostly restates discipline we already have (understand the
problem, devise a plan, carry it out, look back ≈ our loop). The one non-redundant
heuristic worth importing: **the inverse/auxiliary-problem move** — "can you solve a
related or relaxed problem?" Solve the problem with a constraint dropped to learn which
constraint is actually binding. That maps to a control: relax the suspected ceiling and
measure whether the wall moves.

---

## Part 2 — Concrete plugin adoptions

### Adoption 1 — Name the missing abduction step in the loop (SKILL.md)

The loop's step 1 is "convert *assertions* into hypotheses" — it presupposes the
hypotheses exist. Peirce's point is that the *generative* step is its own logical
operation and the only one that adds new ideas. **Add an explicit abduction step** (call
it step 0.5 or fold into a renamed step 1) framing the full cycle:

> **Abduction → deduction → induction.** Our loop already does deduction (step 2:
> derive the outcome→conclusion table from each hypothesis) and induction (step 4: run,
> reach a verdict from how many predictions held). The generative move that puts a
> hypothesis on the table in the first place — *abduction* — is the only operation that
> introduces a new idea (Peirce, CP 5.172), and it is the one the loop currently leaves
> implicit. Make it explicit: a **surprising fact** (an anomaly, a Twyman's-law spike, a
> trade-off everyone has accepted) is the *trigger* to abduce — "if A were true this
> would be a matter of course; suspect A." Generate the candidate set *deliberately*
> (TRIZ lenses below) before collapsing to the leading hypothesis.

This closes the loop's logical triad and gives Pattern B a named theoretical spine.

### Adoption 2 — TRIZ contradiction framing for performance-ceiling campaigns

Today a ceiling campaign treats "we need X fast AND X correct" as a trade-off to measure.
Reframe it as a **physical contradiction** and try the four separations *before* accepting
any trade-off curve. Add to Pattern B's ideation lenses (campaigns.md):

> **Contradiction lens.** State the ceiling as a physical contradiction: "parameter P must
> be HIGH (for requirement R1) AND LOW (for requirement R2)." Then walk the four
> separations as ideation prompts — each is a distinct invention, not a compromise:
> - **Time** — can R1 and R2 be satisfied at *different moments*? (precompute/prefetch =
>   inventive principle #10; do the expensive-correct pass offline, serve the fast pass
>   hot; amortize.)
> - **Space** — at *different locations / data partitions / cores*? (hot path vs cold path;
>   fast approximate region + exact region; SoA split.)
> - **Condition** — make P *adaptive to circumstance* (#15 Dynamics): fast path on the
>   common case, exact path on the rare case detected by a cheap predicate.
> - **System/component** — opposite properties at different *scales*: each shard/link
>   rigid (exact), the aggregate flexible (fast); or vice-versa.
>
> A campaign may NOT file "X fast and X correct is a fundamental trade-off" until all four
> separations have a recorded outcome. An unexplored separation is an unresolved
> contradiction, not a law — same burden of proof as an unprobed ceiling.

This maps cleanly onto the existing idea schema: `wall` = the contradiction, `mechanism` =
which separation/principle, `beats_wall_because` = "separates P in time/space/…".

### Adoption 3 — Ideal Final Result as an ideation prompt

Add IFR to the Pattern-B ideate phase as a first, divergent prompt run *before* the
mechanism-bound lenses:

> **IFR prompt.** Before proposing mechanisms, state the Ideal Final Result: "the function
> is delivered *by itself*, at zero added cost/latency/complexity, as if the bottleneck
> weren't there." Then ask what would have to be true for that to hold. IFR deliberately
> over-shoots to break trade-off anchoring; back off to the nearest *achievable* point.
> The gap between IFR and the current baseline is the campaign's headroom estimate — and
> if the IFR is already nearly met, that is itself a finding (the ceiling is soft / near
> ideal; stop optimizing).

IFR pairs with the existing **self-audit lens** ("soft walls mislabeled as hard"): IFR
says where the ceiling *should* be; the self-audit asks why we accepted it higher.

### Adoption 4 — Peirce's economy of research → upgrade step 0

Step 0 ("cheapest falsification first") already has **cost**. Cite Peirce and add his
other two criteria so the "cheapest probe" ranking is richer than raw cost:

> **Economy of research** (Peirce, CP 7.220ff.): research labor is scarce, so rank probes
> by *reduction-in-uncertainty per unit cost*, not cost alone. Three dimensions:
> - **Cost** — run the cheap probe first (already step 0).
> - **Caution / decomposability** — prefer a probe that *halves the hypothesis space*
>   over one that confirms a single hypothesis (Peirce's *Twenty Questions*: a bisecting
>   question beats twenty narrow guesses). This is the "budget ladder" (§7) pulled forward
>   to probe-selection time, where it belongs.
> - **Breadth** — prefer one probe that discriminates among *several* live hypotheses
>   over one that touches a single one.
>
> Concretely: when ranking probes by expected information gain (already required in step 2
> and Pattern A), the rank function is *information gain ÷ cost* — Peirce's economy made
> quantitative. A bisecting, multi-hypothesis-discriminating, cheap probe wins on all
> three axes and should always run first.

This gives the existing "expected information gain" language a named provenance and folds
the budget ladder, the halving-question heuristic, and step 0 into one principle.

### Adoption 5 (small) — Polya's relaxed-problem control

In step 3 (controlled experiments), add the relaxed-constraint control as a standard move:
to test whether a suspected constraint is the binding one, *drop it* and measure whether
the ceiling moves. If the wall doesn't move, the constraint wasn't binding — a cheap,
decisive control that often beats instrumenting the suspected mechanism directly.

---

## Summary table — where each idea lands

| Source idea | Plugin home | Status |
|---|---|---|
| Abduction = sole generative inference (CP 5.172) | SKILL.md loop: name the missing abduction step | **new step** |
| Abduction→deduction→induction triad | SKILL.md: frame loop as the full cycle | reframing |
| Physical contradiction + 4 separations | Pattern B contradiction lens (campaigns.md) | **new lens** |
| Ideal Final Result | Pattern B ideate phase, run before mechanism lenses | **new prompt** |
| Economy of research (CP 7.220ff.) | Step 0 upgrade: cost + caution + breadth | enriches step 0 |
| Twenty-Questions / bisection | Probe ranking = info-gain ÷ cost | unifies budget ladder |
| Polya relaxed-problem | Step 3 control move | small add |
