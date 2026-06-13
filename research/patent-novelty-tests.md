# Patent examination's operational tests for "is this known"

Patent law has spent ~150 years building mechanical procedures for the exact
question the invention pass asks — *is this already known, or a known
combination?* — and for phrasing the answer as an evidentiary finding against a
searched corpus rather than a self-assessment. The doctrines below are
distilled into procedures an agent can run against a claim, with the deliberate
property that **every verdict is grounded in cited references or their stated
absence**, never in the examiner's sense of how clever the idea feels. The
word "novel" never appears in a well-formed verdict — only "no anticipating
reference found" and "combination (not) taught / motivated."

The unit of analysis is a **claim**: a single sentence listing the invention's
elements (limitations). Before running any test, decompose the invention into
its elements — this is the step that makes the rest mechanical.

---

## 1. Anticipation — the single-reference, every-element test (MPEP 2131 / EPC Art. 54)

This is the cheapest test and the one closest to the invention pass's
prior-art partition. It asks only: **does ONE source already contain the whole
thing?**

**Rule (US, MPEP 2131, quoting *Verdegaal Bros. v. Union Oil*, Fed. Cir.
1987):** a claim is anticipated only if "each and every element as set forth in
the claim is found, either expressly or inherently described" in a **single**
prior-art reference, with the elements **arranged as in the claim**.

**Rule (EPO, G-VI):** subject-matter lacks novelty only if all its features
are **"directly and unambiguously derivable"** from a single disclosure.

### Procedure

1. List the claim's elements E1…En.
2. For each candidate reference R in the searched corpus, check whether R
   discloses **every** Ei — expressly or **inherently** (see below) — in the
   claimed arrangement.
3. **Anticipated** iff some single R covers all of E1…En. One missing element
   defeats anticipation, full stop. A reference missing even one element is
   *not* an anticipation, however close.

### Hard constraints (these are what give the test its teeth)

- **No mosaicing for anticipation.** You may **not** combine two references to
  show every element. Combining is obviousness (test 2), a different and harder
  bar. (US single-reference rule; EPO/Canada "without making a mosaic.")
- **Inherency is inevitability, not probability.** A reference silent on Ei
  still discloses it only if Ei is **"necessarily present"** in what the
  reference describes (*Continental Can v. Monsanto*). "Could be present" or
  "usually present" is not enough. For an agent: only credit an unstated
  element as inherent if its presence is *entailed*, not merely *likely*.
- **Enabled disclosure.** The reference must enable a skilled person to make/use
  the thing. Extra references are admissible *only* to prove enablement,
  define a term, or establish inherency — **never to supply a missing element.**
- **Broadest reasonable interpretation.** Read the claim's elements broadly;
  the broader the claim, the easier it is to anticipate.

### Verdict phrasing (no "novel")

- Anticipated: *"Element-for-element match found in [ref]: every claimed
  element (E1…En) is disclosed in a single source in the claimed arrangement.
  Re-presentation of a known technique."*
- Not anticipated: *"No single reference in the searched corpus discloses all
  of E1…En; element [Ek] not found in any one source. No anticipating
  reference found (corpus: [scope]; flagged unverified if search was
  incomplete)."*

---

## 2. Obviousness — the combination test (MPEP 2141 / KSR / EPC Art. 56)

If no single reference anticipates, the invention may still be a **known
combination**. This is the test that catches "you just bolted X onto Y" — and
it is exactly the failure mode the prior-art partition is trying to catch.
Two near-equivalent formulations: the US Graham/KSR analysis and the EPO
problem-solution approach.

### 2a. US — Graham factual inquiries + KSR rationale (MPEP 2141)

Obviousness is a legal conclusion built on four factual findings (*Graham v.
John Deere*):

- **(A)** scope and content of the prior art;
- **(B)** differences between the prior art and the claimed invention;
- **(C)** level of ordinary skill in the art (the PHOSITA — see §3);
- **(D)** secondary considerations (objective evidence — see below).

**Procedure:**

1. Find the prior-art references that, between them, teach the elements (A).
2. Identify what the claim adds over the closest prior art (B).
3. Ask whether a PHOSITA (C) would have been led to combine/modify those
   references to reach the claim, with a **reasonable expectation of success.**
4. The combination is **obvious** iff step 3 is satisfied under at least one
   articulated **rationale**; per *KSR*, a combination of "familiar elements
   according to known methods is likely obvious when it does no more than yield
   predictable results."

**KSR rationales** (pick and *articulate* at least one — non-exhaustive):

- (A) combining prior-art elements by known methods → predictable result;
- (B) simple substitution of one known element for another → predictable result;
- (C) use of a known technique to improve a similar device the same way;
- (D) applying a known technique to a device ripe for improvement;
- (E) **obvious to try** — choosing from a **finite number of identified,
  predictable solutions** with a reasonable expectation of success;
- (F) known work in one field prompting predictable variation in another, on
  market/design incentives;
- (G) explicit **teaching, suggestion, or motivation** (TSM) to combine.

**Articulation requirement (critical for an agent):** a conclusion of
obviousness "cannot be sustained by mere conclusory statements; there must be
some articulated reasoning with some rational underpinning" (*In re Kahn*).
Common sense may supply a missing piece only if **"supported by evidence and a
reasoned explanation"** (*Arendi v. Apple*). I.e., the agent must *name the
references and state the motivation* — "it's obvious" alone is not a verdict.

**Guards against false positives (hindsight is the enemy):**

- Evaluate the claim **"as a whole,"** not element-by-element in isolation.
- **Reasonable expectation of success** is required — if the combination's
  result was unpredictable, it is not obvious-to-try.
- **Teaching away:** if the prior art discourages the combination, that cuts
  against obviousness.
- **Analogous art only:** references count only if in the same field or
  "reasonably pertinent to the problem faced by the inventor."
- **Secondary considerations** can rebut obviousness: long-felt unmet need,
  failure of others, unexpected results, commercial success tied to the claim.

### 2b. EPO — problem-solution approach (could-would)

A more rigidly staged version of the same question:

1. **Closest prior art** — pick the single most promising starting point (one
   realistic springboard).
2. **Objective technical problem** — identify the features of the claim **not**
   disclosed by the closest prior art, determine their **technical effect**,
   and frame the problem as "how to achieve that effect." (Formulated from the
   distinguishing features, *post hoc*, in objective terms — not the inventor's
   subjective problem.)
3. **Could-would** — ask whether the prior art **as a whole** would have
   prompted the PHOSITA, faced with that objective problem, to modify the
   closest prior art and arrive at the claim. The decisive distinction: not
   whether the skilled person **could** have done it, but whether they
   **would** have — "in the hope of solving the objective technical problem or
   in expectation of some improvement or advantage." Mere possibility is not
   obviousness; there must be a *prompt*.

### Verdict phrasing (no "novel")

- Obvious combination: *"Closest source [ref-1] teaches E1…Ek; remaining
  elements [Ek+1…En] taught by [ref-2]. A skilled engineer faced with [problem]
  would combine them via [named rationale, e.g. simple substitution] with a
  reasonable expectation of success → known combination, not an invention."*
- Not obvious: *"Combination not taught: no reference supplies [Ek], and no
  motivation in the searched corpus would prompt a skilled engineer to reach it
  (result unpredictable / prior art teaches away / no finite predictable set).
  Combination not taught or motivated in searched corpus."*

---

## 3. The PHOSITA standard — who is asking

Both tests are run from the viewpoint of the **person having ordinary skill in
the art** (PHOSITA): a hypothetical practitioner who **knows all the prior
art** in the field and is "a person of ordinary creativity, not an automaton"
(*KSR*) — able to "fit the teachings of multiple patents together like pieces
of a puzzle," but who does **not** exercise inventive genius. For an agent, this
is the calibration knob: judge obviousness as a competent domain engineer who
has read the corpus would, neither a novice (everything looks new) nor a genius
(everything looks obvious). Define the PHOSITA's level explicitly before
ruling — it is Graham factor (C) for a reason.

---

## 4. Mapping to the invention pass

The plugin's prior-art partition ("known technique (named)" vs "possibly novel
(flagged unverified)") **is** the patent examination workflow, minus the word
"novel." Operationally:

| invention-pass step | patent test |
|---|---|
| decompose the claimed invention into elements | claim element listing (pre-req for all tests) |
| search corpus for one source covering all elements | anticipation (test 1) |
| if none, search for a taught/motivated combination | obviousness (test 2) |
| state who would find it obvious | PHOSITA calibration (§3) |
| flag "unverified" when search was incomplete | examiner's "no reference found *in searched corpus*" — never absolute |

The load-bearing discipline carried over: **a "not anticipated / not obvious"
finding is always relative to a stated corpus and is never a positive claim of
novelty** — it is "no anticipating reference found; combination not taught,"
with search scope named and gaps flagged. Anticipation is cheap (run first);
obviousness is the harder combination test (run second); both demand *named
references or their explicit absence*, never a feeling of inventiveness.

---

### Sources (primary)

- MPEP 2131 (Anticipation, 35 U.S.C. 102) — uspto.gov; *Verdegaal Bros. v.
  Union Oil*, 814 F.2d 628 (Fed. Cir. 1987); *Continental Can v. Monsanto*.
- MPEP 2141 (Obviousness, 35 U.S.C. 103) — uspto.gov; *Graham v. John Deere*,
  383 U.S. 1 (1966); *KSR v. Teleflex*, 550 U.S. 398 (2007); *In re Kahn*;
  *Arendi v. Apple*.
- EPO Guidelines G-VII §5 (problem-solution / could-would) and G-VI §1
  (novelty, "directly and unambiguously derivable") — epo.org; EPC Arts. 54, 56.
