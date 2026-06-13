# Framework research synthesis — 11-agent wave (2026-06-12)

Eleven frameworks researched against the plugin's current state (NASA FMEA/FTA,
NASA SE/risk governance, JPL practices, STAMP/STPA, HRO/resilience engineering,
industrial RCA, systems thinking/cybernetics, intelligence tradecraft/ACH,
clinical diagnosis/OODA/AAR, TRIZ/Peircean abduction, Morin complexity,
Goertzel cognitive synergy) — plus the earlier wave (DoE/causal/provenance/
online experimentation, adaptive/Bayesian). Per-framework detail in the sibling
files. This file is the cross-cut: where independent traditions converge, the
convergence is the signal.

## Where the frameworks converge (ranked by convergence count)

### 1. The generation gap — abduction is the plugin's missing half (7 frameworks)
Peirce names it formally (abduction is the only operation that introduces a new
idea; our loop does deduction via outcome tables and induction via verdicts,
abduction only implicitly). The same gap is attacked by: FMEA (enumerate
failure modes BEFORE the incident), STAMP's four-cell unsafe-control-action
taxonomy (mechanical hypothesis generator), fishbone categories, clinical
differential-diagnosis category sweeps, Heuer's documented ACH limit ("cannot
surface an unconsidered hypothesis"), Klein's pre-mortem, TRIZ's contradiction
matrix + ideal-final-result, and Goertzel's stuck-pool mode-switching
(logical → analogical → recombinative → probabilistic before declaring dry).
**Adoption: an explicit generation step with multiple mechanical generators,
triggered at campaign start (pre-mortem/FMEA-lite for risky changes) and on
stuck pools (mode-switch escalation before any "dry" declaration).**

### 2. Loops and multi-cause structure — beyond the linear chain (6 frameworks)
STAMP (accidents as control problems; trigger = "every component met spec and
the loss still happened"), cybernetics (loop-mapping on feedback signatures;
delay-corrected temporality — the event just-before the symptom is usually the
loop feeding back, not the cause), fault trees (minimal cut sets make joint
necessity structural; size-1 cut set = single point of failure), Morin
(recursive/feedback principles, guarded), Cook/Allspaw (catastrophe requires
multiple necessary-but-insufficient failures; "root cause" is a social
construct), KT (report the causal set). **Adoption: a loop/structure layer —
when to switch from component-hunt to loop-model, the UCA taxonomy, fault-tree
representation for joint causes, delay-aware temporality, and verdicts that
attach to necessity/sufficiency claims rather than a singular "root cause".**

### 3. Structured negative evidence (4 frameworks)
KT IS/IS-NOT (the IS-NOT column is a built-in negative control: what could be
affected but is NOT, and what distinguishes it), ACH (rank hypotheses by least
evidence AGAINST, score evidence rows across all hypotheses for diagnosticity),
our existing negative controls and ruled_out list, JPL's exoneration-by-
control. **Adoption: IS/IS-NOT specification table + ACH evidence×hypothesis
matrix for ≥3-hypothesis campaigns.**

### 4. Recording discipline and institutional memory (5 frameworks)
JPL ISA culture (every surprise gets a record even when benign — MCO was lost
partly because the discrepancy went to email instead of the surprise system),
NASA LLIS (≈ our DO-NOT-RE-ATTACK), HRO weak-signal rule (silent anomaly drops
are illegal), NASA Technical Authority dissent preservation (Dissent Log),
Goertzel opened-questions (verdicts generate the next campaign), ACH
indicators/signposts (pre-committed tripwires that REOPEN a CONFIRMED).
**Adoption: ledger extensions — surprise log, dissent log, opened-questions,
reopen-tripwires.**

### 5. Environment fidelity of evidence (4 frameworks)
Test-as-you-fly (JPL: MPL died from a transient visible in test data but never
run flight-like), TRL's real lesson distilled to an `evidence_env:
lab|relevant|operational` tag (not a 9-rung scale — false precision), Safety-II
work-as-done vs work-as-imagined, our two-level replication. **Adoption: tag
every CONFIRMED with its evidence environment; a lab-only confirm cannot pose
as a production claim.**

### 6. Verdict structure upgrades (4 frameworks)
PLN (strength, confidence) two-component truth values — the lower component
drives the next action; NASA mishap taxonomy (proximate/root/contributing with
per-tier confidence); DDx posttest-odds = pretest-odds × LR as the standard
confidence derivation (matches rigor.md §5); scoped verdicts. **Adoption:
optional two-component verdicts for contested claims; per-tier causal
confidence.**

### 7. Probe-ordering unification (3 frameworks)
Peirce's economy of research (cost + caution + breadth — the 1900s original of
"cheapest falsification first", now citable), our info-gain ordering, and the
clinical override: danger×treatability÷cost wins over info-gain when a missed
hypothesis is irreversible — same Bayesian object, different loss function.
**Adoption: one paragraph unifying the rule with the rule-out-the-killers
override.**

### 8. Drift and bias guards (5 frameworks)
Vaughan's normalization of deviance → ratchet guard (pin guardrails to the
ORIGIN baseline across campaigns, not the latest), hindsight-bias guard on
human-error stopping points (Cook/Dekker), HRO reluctance-to-simplify gate
before single-cause verdicts, Feynman Appendix-F signal (large confidence gaps
between evidence-layer and summary-layer are themselves a finding), JPL
"heritage is a trap" (past success is an assumption to verify, not a
credential). **Adoption: failure-mode bullets + a ratchet rule in artifacts.**

## What NOT to adopt (explicitly rejected)
- A 9-rung TRL verdict scale (false precision; evidence_env tag captures the
  real lesson).
- RPN arithmetic as a measurement (ordinal math is broken; triage sort only).
- Morin-taken-neat ("it's all entangled" as a terminal verdict) — every
  complexity move must terminate in a probe or named-probe INCONCLUSIVE.
- 5 Whys as a method (single-path bias, knowledge-ceiling stops, no validation
  — documented failure modes); its only salvage is "ask why more than once."
- ACH as an oracle (treats evidence as independent, can't generate hypotheses)
  — scaffolding only.
- Voting on facts, in any framework's costume.

## Proposed build (next phase)
1. `references/anticipate.md` — the generation layer: pre-mortem FMEA-lite
   (S×O×D with detectability as the software axis), key-assumptions check,
   UCA/fishbone/DDx category generators, TRIZ contradiction + IFR lenses,
   stuck-pool mode-switch escalation, Peircean framing.
2. `references/structure.md` — the causal-structure layer: loop-mapping
   trigger + text-CLD notation, delay-corrected temporality, fault trees and
   minimal cut sets, proximate/root/contributing taxonomy, IS/IS-NOT table,
   ACH matrix, leverage-point ranking of fixes.
3. Ledger/artifacts extensions — surprise log, dissent log, assumptions block,
   opened-questions, reopen-tripwires, evidence_env tag, ratchet rule.
4. SKILL.md hooks — abduction step (1.5), simplification gate before
   single-cause CONFIRMED, danger-first override in step 0, AAR retro in
   step 7, the new failure-mode bullets.
5. Then the same treatment as before: eval round with anticipation/loop-flavored
   scenarios (feedback incidents, pre-mortem quality, IS/IS-NOT usage,
   ACH-matrix verdicts), fix, re-validate, version bump, reinstall.
