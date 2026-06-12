# Invention: the default continuation, with provable claims

Verification is half the method; the other half is what it exists for —
**inventing past what survived.** A confirmed limit is the entry criterion for
an invention campaign, and every machine-discovery engine that has produced
verified new results (FunSearch, AlphaDev-class systems, genetic-programming
patents) reduces to the same architecture the campaign loop already has:
a **generator** (Pattern B ideation), a **mechanical verifier** (acceptance
probes the candidate must pass — execution, not persuasion), and **selection**
(survivors to the frontier, kills to the DO-NOT-RE-ATTACK log). The edge
scales with how mechanical the verifier is: wherever possible, the refute
gate *runs an acceptance probe* instead of adjudicating prose.

Invention mode is the campaign loop with the verdict polarity flipped:
**REDUCED-TO-PRACTICE / NOT-YET-WORKING / KILLED.** "Reduced to practice"
carries patent law's meaning — built and shown to work for its intended
purpose, not conceived and described.

## 1. The pipeline

1. **Frame** — acceptance criteria pre-registered as falsifiable numbers:
   quantified effect, vs a named baseline, on a stated scope. Measure the
   baseline first. If the target smells infeasible, say so early — proving a
   target impossible (§5) is a first-class deliverable, worth more than a
   forged pass.
2. **Ideate with quotas and forced diversity** — a breadth target (Edison's
   discipline: systematic variation, not waiting for lightning), distinct
   lenses per Pattern B, the anticipate.md generators (TRIZ separations,
   ideal final result, recombination of surviving partials). Diversity is
   anti-collapse: identical lenses converge on the same candidate.
3. **Refute, then build** — fresh-context refutation per idea; survivors get
   built. Honest iteration is expected; adjusting the acceptance criteria to
   fit a result is not (deviations are dated scope corrections).
4. **Measure under the fair-comparison gates** (§3) and grade the evidence
   on the provability hierarchy (§4).
5. **Provenance-search** every surviving mechanism (§2). No unsearched
   mechanism is presented as new — ever.
6. **Certify and disclose** (§6, §7): certification ladder, claim chart,
   disclosure block in the ledger, then peer review for high-stakes claims.

## 2. Provenance: search, then say exactly what you found

The word for what you built is never an unsearched superlative. The protocol:

- **Decompose the claim into elements** E1..En (mechanism, application,
  guarantee, context). Search the elements and their combinations.
- **Query families** (≥3): synonyms, domain jargon, abbreviations,
  broader/narrower terms. Terminology drift is the classic miss.
- **Venues** (software inventions): arXiv (`export.arxiv.org/api/query`),
  general web (`html.duckduckgo.com/html/?q=`), Google Patents (the
  `/xhr/query` JSON endpoint; the SPA route renders empty), GitHub repos and
  package registries, RFCs, the canonical engineering-blog corpus for the
  domain. Log what was unreachable — coverage gaps are part of the verdict.
- **Citation chase** backward and forward from the closest hits; **stop** at
  saturation (a full backward+forward iteration finds nothing new — Wohlin's
  rule).
- **Search log** (ledger artifact): date, venue, query, hits reviewed,
  closest findings. A no-prior-art conclusion without the log scores 1 in
  peer review. Absence claims obey the same rule as presence claims: "X is
  missing/was never done" requires the failed lookup shown (the command, the
  path, the empty result) — an unchecked gap assertion is itself a
  fabrication risk, in the deflationary direction.
- **The two mechanical tests** (patent examination, corpus-relative):
  *Anticipated* — one source teaches every element in the claimed
  arrangement (one missing element defeats it). *Taught-as-combination* — a
  competent engineer facing this problem **would** (not merely could) combine
  the found references with reasonable expectation of success. Honor
  teaching-away; beware hindsight.
- **Verdict grammar:** "closest found: X, differing in Y; no anticipating
  reference in the searched corpus (venues + dates listed; gaps: Z)." Always
  relative to a stated corpus. Never an absolute newness claim.
- **Name the canonical solution, especially when you re-derive it.** Most
  well-posed engineering problems have an industry-standard answer (capped
  exponential backoff + jitter for retry storms; CRDTs for offline merge;
  consistent hashing for shard balancing). Find it, name it as prior art, and
  make it the tuned baseline (§3) — not a strawman like "3 immediate retries."
  When your invented mechanism shares the canonical's ingredients (it almost
  always does), say so plainly and scope the contribution to the *measured
  delta* against the canonical, not against the strawman. "Strictly better than
  exponential backoff" is a provenance failure when your mechanism *is* a
  backoff variant: the honest claim is "matches the AWS-canon backoff+jitter on
  criteria A/B and improves C by N% on this scope." Beating a weak baseline
  while ignoring the strong incumbent is the most common way an invention
  over-claims.

## 3. Fair-comparison gates (a win must be a fair win)

- **The verifier is part of the claim.** Before crediting the mechanism,
  audit what the acceptance sim secretly grants: shared state acting as a
  god's-eye coordinator (a module-level counter is a *coordination channel*
  real fleets don't have), a fixed parameter envelope the win actually rides
  on, simplified arrival/failure patterns that hide the adversarial regime
  the claim names. Two mandatory probes: (a) re-run the winner and the tuned
  baseline at a *matched envelope* — if both pass, the envelope is the
  mechanism; (b) break the sim's hidden affordance (instantiate real
  independent actors, perturb the envelope) and see if the claim survives.
  A mechanism that exploits sim structure has been tested against the sim,
  not the claim. This rule has a body behind it: our own flagship candidate
  passed acceptance, independent reproduction, and three provenance waves,
  then died in peer review when the spread turned out to come from the
  harness's shared counter and the window width — not the mechanism.

- **Tuned baseline** — compare against the incumbent's *best* configuration,
  not its defaults. Beating a strawman is the #1 invalid-superiority pattern.
- **Instance diversity** — multiple workloads/seeds/scales; one instance is
  an anecdote with a confound. Report where the win does NOT hold.
- **Ablation** — which element carries the win? An invention whose effect
  vanishes when one incidental detail is removed is that detail, renamed.
- **Test hygiene** — anything tuned on the test instance is flagged overfit;
  hold out seeds/corpora the design never saw.

## 4. Provability hierarchy (grade every claim's evidence)

`measured (n, spread)` < `property-tested (generated cases + shrinking)` <
`exhaustively checked in scope` < `proven`. Pick the upgrade by claim type:
correctness → property test against an oracle (or enumerate if finite);
never-violates-bound → invariant + model-check the design; equivalence →
differential test against the incumbent as oracle; termination/fairness →
analytic argument or model checking (testing can only falsify these). State
the rung; a pass at a lower rung is not a claim at a higher one.

## 5. Impossibility toolkit (proving the target unachievable)

Five proof shapes, cheapest first: **oracle ceiling** (even a clairvoyant
policy can't reach it), **conservation/arithmetic bound** (ρ>1 backlog,
Little's law, budget accounting), **adversary construction** (an input family
defeating every algorithm of the class), **information bound** (the answer
space exceeds what the probes can distinguish), **reduction** to a known
impossibility (FLP/CAP — verify the model matches, name the escape hatch).
The standard: "ruled out the entire class" earns PROVEN-INFEASIBLE; "we
didn't find a way" never does. Every impossibility verdict names its escape
hatches (which assumption, relaxed, reopens the target) and passes a refuter.

## 6. Certification ladder (what the claim may call itself)

`asserted` → `available` (artifact + exact repro recipe) → `functional`
(independently runs) → `reproduced` (independent re-run matches within a
pre-committed tolerance — and the differences must not change the claim) →
`certified` (independent setup + full-disclosure report + provenance search
+ adversarial review). **Reproducibility is not validity**: acceptance,
reproduction, and provenance are self-referential gates — they test the
artifact against its author-chosen configuration. Before `certified` (and
before any deployment-scoped CONFIRMED), an adversarial **target-regime
gate** must run the claim in the regime the claim actually names (independent
actors instead of shared state, the adversarial arrival pattern, the
deployment's real envelope) — our flagship candidate passed the first three
gates and died at this one. Independence is the credential: the builder's own
re-run never grants `reproduced`. The plugin's refuter/peer-review seats are
the independent parties — and **a witness is an artifact, not a sentence**:
the independent party's harness, output, and identity must exist on disk and
be re-runnable. A rung claim whose witness exists only as prose in the
verdict is not an honest mistake — it is fabricated verification, the
cardinal sin: it invalidates the entire claim (not just the rung), goes to
the falsification log, and every other rung claim from the same campaign
gets re-audited. When no independent party is available, the honest forms
are "functional, independent re-run pending" or "builder-verified only,
≤ functional" — both score better in review than an inflated rung.

## 7. Claims: drafting and disclosure

**Claim template:** `[mechanism M] achieves [quantified effect E] vs
[tuned baseline B] on [scope S], evidence [ref], provenance [status + log]`.
Every word is limiting — every adjective is an evidenced promise.

**Claim chart** (one row per element): `element | evidence pinpoint | how
verified (rung)`. It is a single named table in the verdict — not facts
scattered through prose; reviewers check rows, not narratives. The
all-elements rule: one un-evidenced row downgrades the whole claim to
candidate — there is no "mostly proven."

**Lint (downgrade triggers):** unscoped superlative · unfalsifiable benefit ·
conflated elements · capability-as-proof ("can achieve") · missing baseline ·
provenance laundering (recasting a found reference as confirmation) ·
criteria adjusted post-hoc.

**Disclosure block** (ledger): conception (what + when), reduction-to-practice
evidence (the run), inventors/agents, witnessed by (the refuter that
independently re-ran it). This is what makes the invention defensible later.

## 8. Ranking inventions (when there are several)

Score: problem significance · measured effect vs tuned baseline · ideality
(Σbenefit / (Σcost + Σharm) — a ratio, so added cost sinks real benefit) ·
depth (parametric tweak → new mechanism → new principle) · generality of
scope · and **verification grade as a gate, not an addend** — an unverified
high-scorer ranks below a certified modest one. The Koza test for calling it
a real invention: it stands on its own merits against the prior art, with
the machine-made romance stripped away.
