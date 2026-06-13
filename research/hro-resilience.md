# HRO & Resilience Engineering → scientific-method adoptions

Research note for the `scientific-method` plugin. Sources are safety-science
primary/authoritative: Weick & Sutcliffe *Managing the Unexpected*; Hollnagel
*Safety-I and Safety-II* / FRAM (functionalresonance.com); Dekker *Drift into
Failure* / *Just Culture*; Vaughan *The Challenger Launch Decision*. Fetched
via Wikipedia + functionalresonance.com (skybrary/PDF mirrors were 403/404).

The plugin already encodes much of this implicitly (falsification-first,
controls, INCONCLUSIVE as first-class, jointly-necessary-cause warning). This
note names the source disciplines and pulls out adoptions that are *not* yet
in SKILL.md.

---

## Part 1 — Distilled principles

### Weick & Sutcliffe: five HRO principles (collective mindfulness)
HROs sustain "collective mindfulness" — attention quality high enough to catch
subtle ways a context varies and demands a contingent response. Split into
**anticipation** (1-3, forestall the unexpected) and **containment** (4-5,
cope once it arrives).

1. **Preoccupation with failure** — treat every anomaly as a symptom of a
   latent system problem, not noise. Reward reporting of small errors and
   near-misses; an org-wide sense of vulnerability; pessimism as a discipline.
   Success breeds complacency, so chronic unease is cultivated deliberately.
2. **Reluctance to simplify** — resist easy/convenient explanations; the
   operating world is complex, so comprehension must be earned. Look across
   boundaries for where a problem originated and where it leads. Actively
   value diverse experience and dissenting opinion (divergent interpretation
   is a feature, not friction).
3. **Sensitivity to operations** — continuous real-time situational awareness
   of the *actual* state of the system (work-as-done), not the planned state.
   Monitor that barriers/controls are still in place and functioning.
4. **Commitment to resilience** — assume errors are inevitable; build capacity
   to **detect, contain, and recover** rather than only to prevent. Improvise
   and re-organize on the fly (the incident-command team that realizes the
   "garage fire" is a hazmat event and restructures mid-response).
5. **Deference to expertise** — in an upset, decision authority migrates to
   whoever has the relevant expertise, *regardless of rank*; hierarchy applies
   in routine ops only. Decisions made at the front line during a crisis.

### Hollnagel: Safety-I vs Safety-II + FRAM
- **Safety-I**: safety = absence of adverse outcomes (as few things go wrong as
  possible). Reactive: wait for failure, find the cause, fix/eliminate it.
  Bimodal world — the system either works or it fails — so analysis hunts the
  broken component. Humans are a hazard/liability to be constrained.
- **Safety-II**: safety = the **ability to succeed under varying conditions**,
  so the number of acceptable outcomes is as high as possible. Proactive:
  **study why everyday work usually goes RIGHT**, not only the rare cases it
  goes wrong. Humans are a *resource* whose flexible adjustment creates safety.
- **Equivalence thesis**: things go right and wrong **for the same reasons** —
  both flow from ordinary performance variability. So studying only failures is
  a *biased sample* (small, selected-on-the-outcome numerator); the many
  successes carry the information about how the system actually copes.
- **Four potentials** of resilient performance: respond, monitor, learn,
  anticipate.
- **FRAM** (Functional Resonance Analysis Method), four principles:
  (a) equivalence of failures and successes; (b) **approximate adjustments** —
  people trade off efficiency vs thoroughness (ETTO) to fit real conditions,
  ubiquitous and usually useful but never exact; (c) **emergence** — bad
  outcomes aren't discrete breakdowns, they emerge when everyday variability
  aggregates unexpectedly; (d) **functional resonance** — coupled functions'
  small benign variabilities combine and amplify into outcomes no single
  function would predict. Each function has six aspects (Input, Output,
  Preconditions, Resources, Time, Control); coupling happens through these.

### Dekker: drift into failure + just culture
- **Drift into failure**: complex systems migrate *incrementally* toward the
  safety boundary under chronic pressure of scarcity and competition
  (cost/efficiency). Each step is **locally rational and looks normal** —
  decrementalism — so there is no broken part to find; the system fails while
  every component "works." Hunting broken components (Safety-I) is the wrong
  lens; you need systems/complexity thinking. Sensitive dependence on history:
  where it started shapes where it drifts.
- **New View vs Old View of human error**: error is a *symptom* of deeper
  systemic trouble (the New View), not the cause. People aren't the problem to
  control; they're the resource to harness. Safety is the *presence* of
  positive capacity, not merely the absence of negatives.
- **Just culture**: balance accountability and learning. A blame reflex
  destroys the reporting on which preoccupation-with-failure depends. The line
  is between acceptable variability and genuinely reckless behavior — drawn so
  that honest accounts of work-as-done stay safe to give.

### Vaughan: normalization of deviance
A deviation from the rule, once it fails to produce an immediate bad outcome,
gets **culturally normalized** — the new baseline of "acceptable" quietly
ratchets outward, repeat by repeat. Disasters have a *long incubation* with
early warning signs that were misinterpreted, ignored, or explained away
(Challenger O-rings). **Structural secrecy** and a culture of silence keep the
ratchet invisible. The danger is not one bad decision but the slow drift of the
acceptable-risk baseline until catastrophe.

---

## Part 2 — Concrete plugin adoptions

Ordered by leverage. Each names the source principle, the gap in current
SKILL.md, and a concrete mechanism.

### A. Positive-case analysis — invert the failure-only investigation
**Source:** Safety-II equivalence thesis; FRAM principle (a). **Gap:** the whole
method is failure/anomaly-triggered — every example is a wall to break, a
regression to root-cause, a number to refute. We *only* sample the cases that
went wrong, which Hollnagel names as a biased sample.
**Adoption:** add a **"Why does it usually work?"** probe to causal
investigations. Before/alongside root-causing the failure, characterize the
baseline of success: pull the many runs/hosts/requests where the same code path
*succeeded* under the same conditions and ask what made them go right. Two
concrete payoffs that fit the existing ladder:
- It supplies the **negative control** the method already demands ("hosts where
  the playbook ran and nothing broke") — Safety-II reframes that control as the
  *primary* object of study, not an afterthought.
- It separates "the failure has a special cause" from "the system normally
  rides this close to the edge and variability tipped it" (drift/resonance),
  which changes the fix from "remove the broken part" to "widen the margin."
Add a verdict-adjacent note: *what distinguished the success cases from the
failure case?* If nothing did, the cause is resonance/drift, not a component.

### B. Reluctance to simplify — a named gate against premature single-cause
**Source:** Weick reluctance to simplify; Dekker drift (no broken part);
Vaughan. **Gap:** SKILL.md has the jointly-necessary-factors warning in
"Failure modes," but no *active gate*. Make it a step.
**Adoption:** before any CONFIRMED single-cause verdict, run a **simplification
check**: (1) Did we stop at the first sufficient-looking cause, or enumerate
co-necessary factors? (2) Is this a *component* failure or a *drift/resonance*
failure where every part worked? (3) Did we seek a diverse/dissenting
interpretation (a council seat, a reversed hypothesis) before closing? A
single-cause verdict must explicitly clear all three. This operationalizes the
existing anti-pattern as a checklist with teeth, and pairs naturally with the
already-present "reversed hypothesis" and model-council mechanisms.

### C. Drift detection — baselines that can ratchet
**Source:** Vaughan normalization of deviance; Dekker decrementalism. **Gap:**
the method records baselines and signed deltas *within* a campaign, but the
ledger is per-investigation. Across campaigns, an "acceptable" number can creep
— each individual regression rationalized ("only +0.3pp"), the sum catastrophic.
**Adoption:** make the persistent ledger carry a **ratchet guard**: pin
guardrail metrics to their *original* committed baseline (with commit hash, per
the existing provenance header), not to last campaign's value. Flag when the
cumulative drift from the original baseline crosses a threshold even though each
step passed — "each step looked locally rational" is exactly the failure
signature. Concretely: a guardrail table column `baseline_origin` vs
`current`, and a rule that the *origin* never silently advances. This turns the
ledger into the structural-secrecy antidote: the ratchet stays visible.

### D. Weak-signal preoccupation — anomalies are symptoms, not noise
**Source:** preoccupation with failure; Vaughan's "explained-away early
warnings." **Gap:** the method is strong once a hypothesis exists, but says
little about *not discarding* the small anomaly that should have spawned one.
Twyman's law ("a surprisingly good number is a measurement bug") is the
positive-direction version; the negative-direction version is missing.
**Adoption:** a **weak-signal rule**: a small unexplained anomaly (a flaky test,
a 1% outlier, an off-by-a-bit count) is a *symptom* and earns at minimum a
logged hypothesis with a named cheapest-probe — it may be downgraded but not
silently dropped. "Explained away without a probe" is the normalization-of-
deviance move; require the probe or an explicit `ruled_out` entry. This extends
the existing `ruled_out` discipline to cover anomalies nobody asked about.

### E. Just culture in the ledger — protect the honest account
**Source:** Dekker just culture; New View. **Gap:** the falsification log marks
dead ends DO-NOT-RE-ATTACK but is framed around *claims*, not the *agent/author*
who made the wrong call. **Adoption (light):** frame scope corrections and
killed hypotheses as **system learning, not author error** — the wrong version
stays struck-through and dated (already required) *because* visible honest
retraction is what keeps future agents reporting work-as-done. One line in the
ledger template: retractions record what the *evidence* did, never who was
"wrong." Keeps the audit trail blameless so the reporting pipeline stays open.

### F. Deference to expertise — already partly present, sharpen it
**Source:** deference to expertise. **Gap:** the model council "aggregates by
evidence not votes," which is the right instinct, but framed as decorrelating
blind spots. **Adoption:** name the HRO rule explicitly — in an upset, authority
follows *expertise*, not seat count or model prestige. A single seat that *ran
the probe* outweighs three that argued from priors. (The meta-reviewer already
does "one failed reproduction outweighs three approving skims" — this is the
same principle; cross-reference it so the council inherits it too.)

### G. Work-as-Imagined vs Work-as-Done — measure the silicon, generalized
**Source:** Hollnagel WAI/WAD; sensitivity to operations. **Gap:** SKILL.md
already says "measure against ground truth, not metadata… read the silicon, not
the derived formula" — this *is* WAD vs WAI. **Adoption:** none needed beyond a
one-line citation; worth noting the existing rule has a 30-year safety-science
pedigree, which strengthens it. The generalization: docs/specs/flags are
work-as-imagined; the running system is work-as-done; the empirical column
always wins.

---

## Summary table

| Adoption | Source principle | Mechanism | New step or sharpen existing? |
|---|---|---|---|
| A. Positive-case analysis | Safety-II equivalence | "Why does it usually work?" probe; success cases as primary control | New |
| B. Simplification gate | Reluctance to simplify / drift | 3-question gate before single-cause CONFIRMED | Promote anti-pattern to step |
| C. Ratchet guard | Normalization of deviance | Guardrails pinned to *origin* baseline across campaigns | New ledger column + rule |
| D. Weak-signal rule | Preoccupation with failure | Anomaly → logged hypothesis + probe, never silently dropped | Extend `ruled_out` |
| E. Blameless ledger | Just culture | Retractions record evidence not author | Light template note |
| F. Deference to expertise | HRO #5 | Probe-runner outweighs prior-arguer in council | Sharpen council |
| G. WAI vs WAD | Hollnagel WAD | Cite existing "read the silicon" rule's pedigree | Already present |

**Highest leverage:** A (positive-case inversion) is the genuinely new
capability — it flips the plugin from failure-only to success+failure and
supplies controls for free. C (ratchet guard) is the one structural gap the
current per-campaign ledger cannot catch.
