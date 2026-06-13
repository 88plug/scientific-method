# Artifact Evaluation & Reproducibility Certification

Research for the scientific-method plugin: how real CS/systems venues and benchmark
bodies grade reproducibility, so the plugin can adopt a **graded certification ladder**
for invention claims instead of binary "works / doesn't work".

Primary sources:
- ACM, *Artifact Review and Badging — Version 1.1* (Aug 24 2020):
  https://www.acm.org/publications/policies/artifact-review-and-badging-current
- sysartifacts (OSDI/SOSP/ATC/EuroSys/FAST) evaluator + packaging guides:
  https://sysartifacts.github.io/ , /evaluator-guide.html , /packaging-guide.html
- NeurIPS 2024 Call for Papers (paper checklist + code policy)
- SPEC CPU2017 Run and Reporting Rules: https://www.spec.org/cpu2017/Docs/runrules.html
- TPC audit / Full Disclosure Report model (benchmark certification)

---

## 1. The ACM badge system (the canonical model)

ACM defines **three independent badge families** (any combination can apply). The key
move is that *availability*, *artifact quality*, and *result validation* are **separate
axes** — being public says nothing about whether it runs, and running says nothing about
whether an independent team got the same answer.

### Axis A — Artifacts Available
Author artifacts placed on a **permanent, archival, public** repository (Zenodo, figshare,
Dryad, institutional, or ACM DL) with a **DOI / unique identifier**. Personal web pages are
explicitly **not acceptable** (not archival). No evaluation of quality or correctness — only
that the object is retrievable and persistent.

### Axis B — Artifacts Evaluated (independent audit; artifacts shown to reviewers, need not be public)
- **Functional** — artifacts are **documented, consistent, complete, exercisable**, with
  evidence of verification:
  - *Documented*: at minimum an inventory + enough description to exercise them.
  - *Consistent*: relevant to the paper and inherently contribute to its main results.
  - *Complete*: all relevant components included (proprietary parts may be replaced by
    proxies + instructions to obtain them).
  - *Exercisable*: the included scripts/software **actually run** and produce the results;
    included data can be accessed and manipulated.
- **Reusable** — everything in Functional **plus** carefully documented, well-structured for
  reuse/repurposing, and adhering to the community's norms/standards for artifacts of its
  type. This is the "someone else could build on it" bar, not just "it ran once."

### Axis C — Results Validated (a *different team* re-obtained the main results)
- **Reproduced** — an independent team obtained the paper's main results **using, in part,
  the authors' own artifacts**. (Different team, *same* experimental setup.)
- **Replicated** — an independent team obtained the main results **without** author-supplied
  artifacts, building their setup independently. (Different team, *different* setup.)

Critical tolerance rule (applies to both): **exact match is not required or expected.**
Results must agree "**to within a tolerance deemed acceptable for experiments of the given
type**," and crucially — *the differences must not change the main claims of the paper.*
That is the real acceptance criterion: claim-survival under independent re-run, not
bit-identity.

(Terminology note: ACM aligned with NISO/VIM and **swapped** the old meanings — today
*Reproduced = same artifacts, different team*; *Replicated = independent artifacts*. Many
older papers use the reverse. Repeatability = same team, same setup, and is **not** badged —
it's the floor, not a credential.)

---

## 2. How AE committees actually verify (OSDI/SOSP/ATC/EuroSys process)

The systems-venue process is the most operationally detailed and is what the plugin should
mimic for "how do you actually grant a rung." Two phases:

**Phase 1 — "Kick the tires."** Reviewers do a fast pass to confirm the artifact is
evaluable *before* the real review, giving authors time to fix blockers. They build an
**evaluation plan** answering: (Q1) what are the paper's central claims? (Q2) how does the
artifact map to *each* claim? Do I have the right hardware (declared RAM/CPU/accelerators)?
Does it install and does one simple experiment run end-to-end? **What results should I
expect?**

**Phase 2 — Full audit.** Governing principles, quoted from the evaluator guide:
- **"Merely running the code is not enough."** Reviewers **read the code** to confirm the
  artifact does what the paper *describes* — not just that some numbers come out similar.
  Provenance/identity of the result matters, not only its value.
- **"Most of your time should be spent auditing artifacts, not debugging them."** Fixing
  hard bugs is the authors' job; an artifact that needs unreasonable effort can be **denied
  a badge** (e.g. excessive manual steps that should have been automated).
- Single-blind, cooperative author dialogue; each badge decision needs a written
  justification.

Hardware-access ladder (preference order, useful as a cost/realism model): own machine
(Docker/VM) → beefy local box → research clouds (Chameleon, CloudLab) → authors' machine
over SSH → commercial cloud only as last resort.

**Packaging discipline authors must supply:** a README inventory + how-to-exercise;
**containers/VMs for nontrivial dependencies, AND the Dockerfile/build recipe itself**
(an archived image is "**not a substitute for sharing the recipe**" — provenance over
snapshot); measured resource/time expectations (`/usr/bin/time -v`, `mpstat`/`iostat`);
clean-environment testing; **logging of both successes and failures**; dangerous artifacts
flagged explicitly.

**NeurIPS contrast (lighter touch):** a mandatory authored **paper checklist** prompting
reflection on reproducibility/ethics, code "encouraged but not required," reviewers *may*
consult code at discretion. Useful as the low-friction self-attestation rung.

---

## 3. Benchmark certification — full-disclosure-report discipline (SPEC / TPC)

This is the gold standard for "a number you can trust," and is the model for the plugin's
top rung on **performance/quantitative** invention claims.

**SPEC CPU2017 run rules** — the operative principle:
> "For results that are used in public, SPEC requires a full disclosure of results and
> configuration details **sufficient to independently reproduce the results**."

What a **Full Disclosure** must carry: the SPEC-tool result page; the **config file** +
supplemental build/run files; a **flag-definition file** (a result is *invalid* without it);
a complete description of **hardware, firmware/BIOS, and software**; and **all configuration
choices that differ from default** (for energy results, even performance-neutral power
settings). The tester must document **every performance-relevant step an ordinary customer
would take** — responsibility doesn't transfer to whoever set up the box. If a
performance-relevant detail is discovered *after* publication, **the publication must be
updated.**

Reproducibility expectations baked into method: components must be **generally available,
documented, supported, production-quality**, named recognizably; later testers must be able
to obtain them and **reproduce within run-to-run variation**; each benchmark run **3× (median)
or 2× (slower)** for repeatability; **base** (one common optimization set, no FDO, no unsafe
flags) vs **peak** (per-benchmark tuning) separates honest-baseline from best-case. Notably
SPEC CPU uses **peer review, not an independent auditor**, and lets testers self-publish
compliant results — but non-compliant or unreproducible results get marked Non-Compliant.

**TPC model (stricter):** results require an **independent certified auditor** to verify
the run against the spec *before* publication, plus a **Full Disclosure Report (FDR)**
detailed enough for a third party to rebuild the configuration. This is the
"adversarial-review + certified-provenance" extreme.

Takeaway for the plugin: a top-tier quantitative claim isn't "I measured X" — it's
"**here is the config, the environment, the off-default settings, the variance over N runs,
and the recipe, such that an adversary could re-run it and would have to agree.**"

---

## 4. Proposed certification ladder for the plugin

A monotonic ladder for any **invention / capability / performance claim**. Each rung adds a
*kind of evidence*, mirroring the ACM axes + systems-AE rigor + SPEC/TPC disclosure. A claim
sits at the **highest rung whose evidence is on file**; rungs cannot be skipped.

| Rung | Name | Meaning | Required evidence (gate to enter) |
|---|---|---|---|
| 0 | **Asserted** | Author states it works. | Claim text + the specific, falsifiable prediction it makes. No execution yet. *(≈ NeurIPS self-checklist; "Repeatability" floor.)* |
| 1 | **Available** | The artifact exists and is retrievable. | Code/data/script pinned at a **content-addressed / archival** location (commit SHA, DOI, tag) — not a mutable path. Inventory README. *(≈ ACM Artifacts Available.)* |
| 2 | **Functional (runs)** | It executes end-to-end and produces *a* result, here. | Clean-environment run (container + **the build recipe, not just the image**); documented deps/resources; a getting-started command that completes; logs of success **and** observed failures. *(≈ ACM Functional / AE "kick-the-tires".)* |
| 3 | **Reproduced** | An **independent re-run** (fresh agent/seat, author's artifacts) gets results that **agree within tolerance and don't change the claim**. | Pre-registered **acceptance criteria + tolerance** *before* the re-run; the re-run executed by a party that did not author the artifact; **code read**, not just output compared ("merely running is not enough"); claim-to-experiment mapping showing this experiment backs *this* claim. *(≈ ACM Results Reproduced + AE audit.)* |
| 4 | **Certified** | The claim survives **independent setup + full disclosure + adversarial review**. | Independent **re-implementation or independent setup** (≈ ACM Replicated); **Full-Disclosure Report**: env, all off-default settings, variance over N runs, provenance/recipe sufficient for a third party to rebuild; a **prior-art / provenance search** (is this novel / not already known to fail?); an **adversarial reviewer** (the plugin's refuter / peer-review seats) who tried to break it and could not. *(≈ ACM Replicated + Reusable + SPEC/TPC FDR & audit.)* |

### Design rules carried over from the sources
1. **Separate the axes.** "Available," "runs," and "an independent party agrees" are
   orthogonal — never collapse them into one yes/no. A claim can be Available but not
   Functional, or Functional but not Reproduced.
2. **Provenance over snapshot.** Require the *recipe* (Dockerfile/script/seed/config), not
   just a frozen binary or a logged number. SPEC and sysartifacts both insist on this.
3. **Tolerance, pre-committed, claim-anchored.** Acceptance = "agrees within a stated
   tolerance **and the differences don't overturn the claim**," fixed *before* the re-run —
   not bit-identity, not post-hoc goalposts.
4. **Read the artifact, don't just run it.** Rung 3+ requires confirming the mechanism
   matches the asserted mechanism (the AE "audit, don't debug" principle) — this is exactly
   the plugin's refuter/peer-review role.
5. **Independence is a credential.** The re-runner / reviewer at rungs 3–4 must not be the
   author of the claim — directly maps to spawning a fresh refuter or council seat.
6. **Full Disclosure is the top gate.** Certified claims ship with a report an adversary
   could use to rebuild and re-run; if a relevant detail surfaces later, the record is
   updated (SPEC rule 4.1.3).
