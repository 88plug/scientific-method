# How Inventions Get Judged → A Scoring Rubric for the Plugin

Synthesized from established invention/innovation judging frameworks. Sources are primary
(award sites, TRIZ Journal) and cited inline. The goal: a defensible rubric the plugin can
use to rank its own inventions on a consistent scale.

## Source frameworks

### James Dyson Award (jamesdysonaward.org)
Student/early-career design-engineering prize. Multi-stage panel judging:
1. **National panel** (independent academics/professionals, *contact details withheld from
   judges* — blind-ish) picks top 3 per country; one is National Winner.
2. **Dyson engineer panel** cuts to a global Top 20 "purely on the merits of how well they
   respond to the brief."
3. **James Dyson personally** picks international winner + sustainability winner; IP team
   screens finalists for patent infringement before the final pick.

Explicit judging dimensions (2025 T&Cs + judge interviews):
- **Functionality** — does it actually work; the solution's value, not the problem's weight.
- **Design process** — evidence of iterative, trial-and-error development ("5127th prototype").
- **Differentiation / originality** — "truly original," solves what others couldn't.
- **Commercial viability** — will people want it; can it be made at a reasonable price (include
  manufacturing-cost / retail-price research).
- **Evidence grade** (2025 clause 9.1): "practical engineering merit, including evidence of
  design development, functional prototyping, **controlled testing with recorded results**, and
  demonstrated performance in **real-world or accurately simulated** use environments." Entries
  must include material proof (working prototypes, drawings, simulations, test results).

Key principle: *"Projects are judged on the strength of the entry, not just the invention."*
A real effect you can't evidence doesn't score.

### XPRIZE (en.wikipedia.org/wiki/XPRIZE)
The opposite philosophy and the one most useful for falsification: prizes go to **the first to
cross objective, pre-defined "finish line" requirements**, *not* a committee weighing relative
merit (explicitly contrasted with the Nobel model).
- Targets are **quantitative and pre-registered**: e.g. sequence 100 genomes in 10 days at
  <1 error/100k bp, ≥98% coverage, <$1,000/genome (Archon); 100 MPGe & <200 g/mi CO2e (auto);
  extract ≥2,000 L water in 24h on renewables at ≤$0.02/L (Water Abundance).
- **Verification is real-world demonstration**, not a pitch: Carbon XPRIZE finalists tested at
  actual coal/gas power plants; Tricorder devices had to diagnose "as well as a panel of board
  certified physicians."
- **Judges enforce the bar**: if no entrant clears the minimum, *no grand prize is awarded*
  (Feed the Next Billion paid nothing; Tricorder paid reduced amounts; Lunar XPRIZE expired
  unclaimed). Failing to beat the target ⇒ no award. This is the model to copy.

### R&D 100 Awards
Independent-judge panel scoring of the "100 most technologically significant products" of the
year; judges weigh technical significance, competitive advantage vs. existing tech, and
demonstrated performance. (Operationally similar to Dyson's panel + significance axis.)

### TRIZ — Ideality (the-trizjournal.com)
Systems evolve toward higher **ideality**:

    Ideality = Σ Benefits / (Σ Costs + Σ Harm)

The **Ideal Final Result** has all benefits, zero cost, zero harm. Altshuller's original
function form: I = ΣF / ΣC (functional capability over cost); weighted form
I = (Σ kᵢFᵢ) / (Σ KⱼCⱼ) lets you assign importance coefficients. Practical upshot: an invention
that adds a benefit but also adds large cost or a new harm has *low ideality even if the benefit
is real*. Rank by the ratio, not the numerator alone.

### TRIZ — Altshuller's 5 Levels of Invention (the-trizjournal.com; iitb.ac.in TRIZ intro)
From analysis of ~200,000 patents — "how deep is the change." (Percentages vary by source;
representative figures shown.)

| Level | What changed | Knowledge needed | Contradiction | ~% patents |
|-------|-------------|------------------|---------------|------------|
| **1** | Routine/parametric tweak of an existing system | Within the specialty | none resolved | ~30–32% |
| **2** | Minor improvement; resolves a *technical* contradiction | Within the industry | technical | ~45% |
| **3** | Major improvement; resolves a *physical* contradiction (Su-field) | From other industries | physical | ~18–20% |
| **4** | New concept/principle — replaces the technology itself (new principle delivers the function) | From other sciences (ARIZ) | transcended | ~4% |
| **5** | Discovery of a new phenomenon, enabling a whole new generation of systems | Beyond current science | n/a | ~1% |

TRIZ tools target levels 3–4 (the "inventive" zone). Level 1 ≈ "non-inventive"; Level 5 ≈ pure
discovery. Use this as a **depth axis**: a genuine principle-change (L4) outranks a tuned
parameter (L1) even at equal measured effect.

---

## Recommended rubric for ranking the plugin's own inventions

Score each dimension 0–5; the verification grade is a **gate/multiplier**, not just an addend —
an unverified claim cannot outrank a verified one regardless of its other scores. Suggested
weights in brackets (tune to taste); composite = weighted sum × verification multiplier.

| # | Dimension | What it measures | 0 ⟶ 5 anchor | Wt |
|---|-----------|------------------|--------------|----|
| 1 | **Problem significance** | Does solving this matter? (Dyson "weight of the problem", R&D100 significance) | trivial/niche ⟶ broad, important, real-world pain | 0.15 |
| 2 | **Measured effect size vs. tuned baseline** | Improvement over a *fairly-tuned* prior baseline, not a strawman (XPRIZE finish-line; guards against fooling-yourself) | within noise / beats only weak baseline ⟶ large, robust margin over a strong tuned baseline | 0.25 |
| 3 | **Ideality** = benefit / (cost + harm) | Net value, penalizing added cost & new harms (TRIZ) | benefit erased by cost/harm ⟶ near-IFR: big benefit, negligible cost, no new harm | 0.20 |
| 4 | **Altshuller level** (depth of change) | How fundamental: parametric tweak ⟶ new principle | L1 parametric tweak ⟶ L4–5 new principle/phenomenon | 0.15 |
| 5 | **Generality of scope** | Breadth of conditions/domains where it holds | one dataset/config ⟶ transfers across domains, robust to perturbation | 0.10 |
| 6 | **Verification grade** *(gate ×)* | Strength of evidence on the certification ladder | claim only / self-report ⟶ controlled test, recorded results, real-world or accurately-simulated demo, independently reproduced | ×0.4–1.0 |

**Scoring discipline (from the frameworks):**
- *XPRIZE rule:* if the invention does not beat its pre-registered target/baseline, it does not
  place — no participation credit. Pre-commit the target before measuring.
- *Dyson rule:* score the entry's *evidence*, not its aspiration. No recorded test ⇒ dim. 2 & 6
  are capped low.
- *TRIZ rule:* rank by the ideality *ratio* and by *depth* (level), so a high-effort parametric
  tweak can't outrank a cheaper, more general principle-change.
- *Verification as multiplier:* mirrors the plugin's certification ladder — a brilliant idea at
  "claimed-only" grade is gated below a modest idea that's been independently reproduced.

### Verification grade ↔ multiplier (map to the plugin's certification ladder)
0 claimed only (×0.4) · 1 self-tested, no controls (×0.55) · 2 controlled test, recorded
results vs. tuned baseline (×0.7) · 3 real-world or accurately-simulated demo (×0.85) ·
4 independently reproduced / blind-replicated (×1.0).
