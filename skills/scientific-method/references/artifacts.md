# Artifact templates

Three proven artifact shapes. Pick by campaign type, adapt headings to the
project's conventions. All of them share the skeleton:
**Hypothesis → Probe/Method → Measurement → Verdict (status marker) → Reproduce**,
plus an append-only dated log and explicit scope corrections.

Status-marker vocabulary (use these, bold, in tables and headings):
`CONFIRMED`, `FALSIFIED`, `INCONCLUSIVE`, `Disproved`, `Dropped`, `Dead`,
`WITHDRAWN AS NOT-A-BUG`, `REGRESSES`, `not the path`, `filed, not shipped`,
`DO-NOT-RE-ATTACK`.

---

## 1. Hypothesis ledger (`EXPERIMENTS.md`) — default for any campaign

```markdown
# <Campaign name> — hypothesis ledger (<date started>)

Goal: <one sentence — the falsifiable target, with a number if possible>
Baseline: <the sacred starting measurement, with how it was produced>

Provenance: commit <git SHA> | machine <probed identity, not spec sheet> |
env <toolchain/driver versions> | inputs <files + hashes or workload spec> |
date <ISO date>

## Hypotheses

| #  | Hypothesis (falsifiable claim)            | Prediction            | Probe                       | Verdict |
|----|-------------------------------------------|-----------------------|-----------------------------|---------|
| H1 | <claim with numbers>                      | <expected observation>| <command/file>              | OPEN    |
| H2 | ...                                       | ...                   | ...                         | **FALSIFIED** — <evidence, one line> |

## Outcome tables (written BEFORE running)

### H1
| Outcome | What it proves | Next action |
|---------|----------------|-------------|
| A: ...  | ...            | ...         |
| B: ...  | ...            | ...         |

## Assumptions (key-assumptions check — classify before probing)

| assumption | status (solid / caveated / unsupported) | if unsupported → hypothesis # |
|---|---|---|

## Ruled out

| Candidate | Ruled out by (evidence) |
|-----------|-------------------------|
| <cause>   | <control case / zero hits in window / probe output> |

## Surprise log (every surprise gets a record, even benign — ISA discipline)

| date | what surprised us | disposition (explained / hypothesis # / use-as-is) |
|---|---|---|

## Dissent log (overruled objections survive, with their evidence)

- <date> <who/which seat> objected: <claim> — overruled because <evidence>.
  Reopen if: <observable condition>.

## Reopen tripwires (pre-committed indicators that reopen a CONFIRMED)

| verdict | tripwire (observable) | check cadence |
|---|---|---|

## Opened questions (what these verdicts made newly askable)

- <question> — discovery claim; next probe: <exact command/query>.

## Disclosure (for invention campaigns — see references/invent.md)

| field | value |
|---|---|
| claim (template grammar) | [M] achieves [E] vs [B] on [S] |
| conception | <what + when> |
| reduced to practice | <the run/evidence ref> — or NOT-YET-WORKING / KILLED |
| certification rung | asserted / available / functional / reproduced / certified |
| provenance | closest found: <X>, differing in <Y> (search log: <ref>) |
| witnessed by | <independent party + PATH to their harness/output artifact — prose attestation is not a witness> |

## Falsification log (append-only — DO-NOT-RE-ATTACK)

- **<Dead idea>:** <what was assumed> — **Disproved** (<probe/file>):
  <evidence + the number that killed it>. DO-NOT-RE-ATTACK.

## Scope corrections

- <date>: previously claimed <X>. After <better attribution/probe>, actually
  <Y>. Original text retained above as historical record.

## Reproduce

```bash
# exact commands that regenerate every headline number
```
```

Rules for the ledger:
- Append, don't rewrite. Wrong claims get a scope-correction entry, not
  deletion — the audit trail is what makes the verdicts trustworthy.
- Every verdict cell carries its one-line evidence inline. A verdict without
  evidence is OPEN, whatever you believe.
- Update the ledger the moment a verdict lands, not at the end of the
  session. Compaction eats conversations; the ledger survives.
- Headline numbers carry **n + spread** (e.g. "median 117.8, n=5,
  117.5–118.1"), never a bare point. Say which replication level n refers
  to: re-running the same binary, or rebuilding/rebooting the whole setup.
- Every CONFIRMED carries an **evidence_env tag**: `lab` (synthetic/sandbox),
  `relevant` (realistic conditions), or `operational` (the real system under
  real load). A lab-only confirm cannot pose as a production claim — "test as
  you fly"; where operational evidence is impossible, say so and substitute
  independent analysis, never assumption.
- **Ratchet rule:** guardrail baselines pin to the *origin* measurement, not
  the latest campaign's. Per-campaign deltas can each look acceptable while
  the baseline quietly walks (normalization of deviance) — the ledger must
  make cumulative drift visible.
- For contested claims, split the verdict into **(strength, confidence)** —
  how true vs how much evidence — and let the *lower* component drive the
  next action: high strength + low confidence → replicate before acting.
- Causal verdicts may be tiered **proximate / root / contributing** with
  per-tier confidence (see references/structure.md §3).
- **Repro-completeness gate for CONFIRMED:** config + how it was chosen,
  number of runs, central tendency + spread, metric definition, exact
  command, machine/env (the provenance header). A verdict missing one of
  these is INCONCLUSIVE with the missing item named — same rule as the
  missing-probe convention.

---

## 2. Walls document — for performance-ceiling campaigns

Modeled on a real campaign that falsified four asserted "physical" limits.
Use when the question is "are we actually at the hardware/system limit?"

```markdown
# <System> walls — why these numbers are credible (scientific campaign, <date>)

Method: falsify assumed limits with isolated microbenchmarks, then read the
hardware/platform directly (probes, not derived formulas).

## The machine
| | |
|---|---|
| CPU/GPU/NIC/etc | <probed values, with probe command> |

## The hypotheses
| # | Hypothesis | Probe | Verdict |
|---|-----------|-------|---------|
| H1 | <asserted limit is wrong because...> | <bench file> | **FALSIFIED — real ceiling is X** |
| H2 | ... | ... | **CONFIRMED — bandwidth-bound, N% of measured spec** |

## Conclusion
<every claim stated as % of a MEASURED ceiling, never a spec-sheet number>

## Reproduce
```bash
<probe commands>
```

## Appended findings
### W<n>: <title> — <result> (<date>)
Method / Problem / Verdict, with before/after table.
```

Key discipline: report every throughput/latency claim as a percentage of a
*measured* ceiling. "85% of achievable GDDR6 bandwidth (266 GB/s measured,
280 spec)" is credible; "fast" is not.

---

## 3. Investigation post-mortem — for root-cause / incident campaigns

Modeled on a fleet investigation that survived vendor scrutiny.

```markdown
# <Incident title>

**Date:** / **Author:** / **Severity:** / **Status:**

## Scope correction (if any — added later, dated)
<explicit retraction of earlier overclaims; keep the original below as record>

## Executive summary
- <cause 1> — **confirmed** (<evidence ref>)
- <cause 2> — **WITHDRAWN AS NOT-A-BUG** (<what disproved it>)
- <cause 3> — still unexplained, next probe: <exact query>

## Discovery path
1. <numbered chain of observations — how the evidence actually unfolded>

## Hypothesis elimination
| Hypothesis | Status |
|------------|--------|
| <candidate> | FALSIFIED — <control case / probe result> |
| <candidate> | CONFIRMED — <evidence> |

## Impact data (validated)
<tables, each row traceable to a query>

## What we did to confirm
<the controls: negative controls, replication across samples, ground-truth
escalation (e.g. binary disassembly) — why this is proof, not correlation>

## Action items
### Vendor-side / ### Our side / ### Documentation

## Lessons
```

The load-bearing sections are **Scope correction** (retractions stay visible)
and **What we did to confirm** (controls named explicitly). A synchronized
multi-host burst, a control group that took the same treatment without the
symptom, replication on N independent samples — say which you have.

---

## Claimed-vs-observed matrix — for "is the documentation/metadata lying?"

```markdown
## <Capability> matrix — fleet-wide empirical test

| Device/Item | Metadata claims | Empirical result | Evidence |
|-------------|-----------------|------------------|----------|
| <item>      | YES (default)   | silent-fail      | <probe output path> |
```

Probe passes that contradict each other mean a confound (cross-contamination,
caching, state leakage) — tighten isolation and re-run until two consecutive
passes agree, and say how many passes it took.
