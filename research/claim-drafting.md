# Precision claim language → scientific-method plugin

Research notes + plugin adoptions. Sources: USPTO **MPEP** §§2111, 2111.01,
2111.03 (claim interpretation, every-word-limiting, transitional phrases,
antecedent basis); Wikipedia *Claim chart* (element→evidence mapping, all-
elements test); Wikipedia *Falsifiability* (Popper, *Logic of Scientific
Discovery* 1934: risky predictions, bounded scope, named detection method).

---

## 1. Distilled principles

### From patent claim drafting (MPEP)

- **Every word is limiting.** Each term in a claim is a *limitation* that must be
  independently satisfied; examiners "may not disregard" any of them. A claim is
  only as strong as its narrowest word. Corollary for us: every adjective in an
  invention claim is a promise you must evidence — drop the ones you can't back.
- **Broadest *reasonable* interpretation, not broadest possible.** Terms take
  their ordinary meaning to a skilled reader *consistent with the spec*. Ambiguity
  is read against the drafter. → If your claim can be read two ways, the
  unfavorable reading is the one that gets tested. Disambiguate up front.
- **Be your own lexicographer — "with reasonable clarity, deliberateness, and
  precision."** You may redefine a term, but only by stating the definition
  explicitly. "About"/"substantially"/"fast" without a defined bound default to a
  reading you don't control (*Merck*: "about" ≠ "exactly").
- **Independent vs. dependent claims.** The independent claim states the
  *self-contained* core (mechanism + effect). Dependent claims *inherit every
  limitation* of the parent and add one more — they can only narrow, never
  broaden. → Structure findings the same way: one standalone headline claim, then
  sub-claims that add scope/conditions, each strictly inside the parent.
- **Transitional phrase = scope contract.** "Comprising" is open (effect holds
  *among other things*); "consisting of" is closed (effect holds *from exactly
  these elements*). Pick deliberately — an open claim is harder to falsify but
  also weaker/less corroborable.
- **Antecedent basis.** "Said X" must point to exactly one earlier "a X." No
  dangling referents. → Every "the improvement", "the speedup", "the baseline"
  must have been concretely introduced earlier with one unambiguous referent.
- **Preamble / intended-use language is *capability*, not proof.** "Adapted to
  reduce latency" is met by anything merely *capable* of it (*In re Schreiber*).
  Recite the *structural/manipulative difference* that actually produces the
  effect, not the hoped-for result.

### From claim charts (litigation discipline)

- **All-elements test.** Infringement (or invalidity) requires that *every*
  element find a one-to-one match in the evidence. A single unmatched row defeats
  the whole showing. → A finding is only proven if every clause maps to evidence;
  one un-evidenced clause = unproven finding, not a "mostly-proven" one.
- **Parse claim into discrete limitations, then map each.** Two columns: claim
  language (left) ‖ pinpoint evidence (right, with column/line-level citations —
  no hand-waving to "the codebase").
- **Charts have a declared purpose.** Infringement (effect present), invalidity
  (prior art / already-known), eligibility (it's just X-with-a-computer). → Tag
  each finding's chart purpose: *novel mechanism* vs. *known baseline* vs. *trivial
  restatement*.

### From falsifiability (Popper)

- **A claim must prohibit something.** If it's compatible with every possible
  observation, it predicts nothing and is unprovable *because* it's unfalsifiable.
  "Our method is better" excludes no result. "≥15% lower p99 latency on workload W
  vs baseline B" excludes the result where it isn't.
- **Bound your quantities.** "Eventually fast"/"scales" are open-ended escape
  hatches. "Melts below X°C" / "completes in <Ns at N=10⁶" can be refuted.
- **Name the detection method + initial conditions.** Testable form: *given
  condition C, observation P must follow; C-true-with-P-false refutes.* State how
  you'd measure P and under what C — otherwise "failure" is undefined.
- **No rescue clauses.** Don't build in reinterpretations ("it's faster except
  when it isn't") that immunize the claim against any contrary evidence.
- **Stronger (more-prohibiting) claims are more useful *and* more corroborable.**
  Risk is a feature: a claim that survives a test it *could* have failed earns
  belief; one that couldn't fail earns none.

---

## 2. Plugin adoption — the CLAIM GRAMMAR

Every invention/finding claim the plugin emits MUST instantiate this template.
Each slot is a *limitation* (MPEP: every word limiting); an empty or vague slot =
an unprovable claim, flagged by `/verdict`.

> **TEMPLATE**
> "**[mechanism M]** achieves **[quantified effect E vs baseline B]** on
> **[scope S]**, as demonstrated by **[evidence ref]**, with **[provenance
> status from search log]**."

| Slot | Must be | Falsifiability role | Failure if omitted |
|---|---|---|---|
| **M — mechanism** | The concrete structural/manipulative cause (not the hoped result). | Names the "initial condition C". | Intended-use claim — capability, not proof. |
| **E — effect, quantified** | A number + direction + unit (≥X%, <N ms, ±σ). | The risky prediction P. | Unfalsifiable benefit ("better", "faster"). |
| **B — baseline** | The explicit thing E is measured *against* + how. | Defines what "no effect" looks like. | E is meaningless (faster than *what*?). |
| **S — scope** | Inputs/workload/regime where the claim holds (and, ideally, where it doesn't). | Bounds the quantifier; prevents open-ended rescue. | Unscoped superlative — over-broad, dies to one counterexample. |
| **evidence ref** | Pinpoint citation: file:line, run id, table/figure. | Satisfies all-elements test, one row per clause. | Unproven — assertion without a chart row. |
| **provenance** | From the search/run log: verified / measured / cited / assumed. | Separates demonstrated from inherited/assumed. | Conflates "I measured" with "I assumed". |

**Worked example.** ✗ "The new cache makes the API faster." →
✓ "**Per-key LRU eviction with a 4 KB bucket size (M)** achieves **≥22% lower
p99 read latency (E)** vs **the prior global-LRU cache, measured on the same 8-core
host (B)** on **the read-heavy `bench/api-read` workload at ≥10⁵ keys; no gain
under write-heavy load (S)**, as demonstrated by **`bench/results/2026-06-run3.json`
rows 11–14 (evidence ref)**, status: **measured, n=5, 95% CI ±3% (provenance)**."

---

## 3. The claim-chart pattern

Decompose each headline claim into clauses; one row per clause; complete coverage
required (a gap = unproven). Three columns, not two — we add *how verified* so the
chart is self-auditing.

| Claim element (limitation) | Evidence (pinpoint) | How verified |
|---|---|---|
| M: per-key LRU, 4 KB buckets | `src/cache/lru.rs:88–120` | code read + unit test `lru_evicts_per_key` |
| E: ≥22% lower p99 | `results/2026-06-run3.json:11` | re-ran bench, 5 trials, CI computed |
| B: vs global-LRU, same host | `bench/baseline.toml`, `run3` host meta | same-host diff, controlled |
| S: read-heavy ≥10⁵ keys only | `bench/api-read.yaml` | tested in-scope + 1 out-of-scope (write) negative |
| provenance | `search-log.md:#run3` | measured (not assumed/cited) |

Rules: (1) every clause of the headline appears as a row; (2) every row cites a
*locatable* artifact; (3) "How verified" names the act (measured / re-ran / read /
cited / **assumed** — and "assumed" rows are red flags); (4) one unmatched or
"assumed" row downgrades the whole claim from *proven* to *candidate*.

---

## 4. Common claim-drafting failures (the lint list)

`/falsify` and `/verdict` should reject or downgrade claims hitting any of these:

1. **Unscoped superlative** — "fastest / best / always / fully" with no S. Dies to a
   single counterexample (Popper: "all men are mortal" is unfalsifiable; *die
   before 150* is). Fix: bound the scope and the quantity.
2. **Unfalsifiable benefit** — E with no number, baseline, or prohibited outcome
   ("improves performance", "more robust"). Excludes no observation → proves
   nothing. Fix: ≥X% vs B, state what result would refute it.
3. **Conflated elements** — M, E, and B mashed into one phrase so no single part is
   independently checkable ("our optimized pipeline is efficient"). Fix: split into
   separate limitations, one chart row each (MPEP antecedent/all-elements).
4. **Capability-as-proof** — "designed to / adapted to / should reduce" (intended
   use). Met by mere capability, not demonstrated (*Schreiber*). Fix: cite a run
   where it *did*.
5. **Missing baseline** — "30% faster" with no "than what, measured how". Fix: name B
   and the controlled comparison.
6. **Dangling antecedent** — "the speedup", "the improvement" never concretely
   introduced. Fix: one unambiguous prior referent.
7. **Rescue clause / provenance laundering** — "faster (except edge cases)" or citing
   an *assumed* value as if measured. Fix: no immunizing caveats; tag provenance
   honestly (measured/cited/assumed) from the search log.
8. **Open-vs-closed mismatch** — claiming "consisting of these factors" (closed)
   while the effect actually needs un-recited helpers, or claiming broadly
   ("comprising") then citing a single narrow run as proof. Fix: match the
   transitional scope to what the evidence supports.
