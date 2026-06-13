# Peer review — lens: REPRODUCIBILITY + instance diversity

Blind reviewer, fair-comparison gate. Harnesses: `simx.py` (generalized sim),
`baselines.py` (golden + tuned decorrelated-jitter factories), `run_variants.py`.
All runs Python 3.14.5, Linux 6.6.141. sim.py sha256 `0f2c5dee…`, policy.py `40c4f619…`
(both == prior re-cert).

SUMMARY: The submission claims a deterministic golden-ratio (φ⁻¹ LDS) first-retry
delay policy beats immediate-retry (peak 1.0× vs 4.0×, post-p99 0 s, healthy 1.0)
and beats random jitter because LDS "eliminates clustering that caps random at 0.997"
(campaign H4/H5). Evidence is a single sim instance (30 s outage, cap 1500, load 1000,
120 s). My lens tests (a) verbatim reproduction and (b) the instance-diversity / fair-
comparison gate that both prior reports explicitly left unmet.

LENS — what I executed:
- Re-ran the original from scratch in my own harness: baseline peak **4.0**; golden
  peak **1.0** / p99 **0** / healthy **1.0**; seed-invariant over 10 seeds incl. two
  never tried (123456789, −5). Matches the claim exactly. Reproduction: PASS.
- Built 7 sim variants and ran golden AND a well-tuned decorrelated-jitter baseline
  (same [base..base+span] envelope, same 3-attempt bound — the ONLY variable is
  LDS-vs-RNG) at n=20 seeds each: short outage (5 s), long outage (120 s), tight cap
  (1100), loose cap (3000), flapping (down-up-down), thundering-herd (1 s blackout
  + tight cap), plus the original as a sanity anchor.

STRENGTHS:
- The original numbers reproduce **exactly**, deterministically, seed-invariant. The
  baseline-vs-invention delta on the immediate-retry baseline is real (4.0→1.0).
- The mechanism for the peak/p99 win (spread first retry past the outage, bound
  volume) is sound and *does* hold wherever the envelope clears the outage.

WEAKNESSES:
- **[BLOCKING] The win over a fair baseline is ≈ zero on every variant.** Wherever
  golden scores 1.0/0/1.0, tuned random jitter (n=20) scores 1.0/0/1.0 too (min=mean=max).
  Wherever golden fails, jitter fails identically: V2 long-outage golden peak 2.55 /
  healthy 0.41 / p99 85 s = FAIL, jitter 0/20 pass; V3 tight-cap golden healthy 0.847 =
  FAIL, jitter 0/20 pass. The invention's distinguishing ingredient (deterministic LDS)
  buys no measurable advantage over RNG jitter in the same envelope on any instance tested.
- **[BLOCKING] The H4/H5 "LDS beats random clustering" claim does not reproduce at a
  matched envelope.** At the campaign's OWN envelope [30..90]: golden healthy = **0.9986**
  (not 1.0), jitter mean 0.9968 (worst seed 0.9951 — still ≥0.995 criterion). At the
  submission envelope [31..101]: BOTH golden and jitter hit **1.0** (n=50). So the perfect
  1.0 is a property of the wider/shifted base=31 envelope, NOT of the golden ratio. The
  "random caps at 0.997, determinism fixes it" story is an artifact of comparing a tuned
  golden envelope against a differently-tuned random one — apples to oranges.
- **[non-blocking] Brittleness across instances**, already conceded but now quantified:
  the policy inverts from full-pass to full-fail when the outage exceeds the span window
  (V2) or cap headroom shrinks below the backlog drain rate (V3). base/span are
  hand-fit to this one instance.

QUESTIONS FOR AUTHORS:
1. Re-run golden vs random jitter in the **identical** [31..101] envelope across V0–V5
   (probe: `run_variants.py`). Show one instance where deterministic LDS beats RNG on
   any acceptance metric by more than seed noise. If none exists, the novelty element
   collapses to "pick a wide enough first-retry window."
2. The H4/H5 claim asserts random tops out at ~0.997 while golden hits 1.0. At a matched
   envelope golden is 0.9986 ([30..90]) or 1.0 ([31..101]) — same as random. Reconcile.
3. Determinism is real but is it *useful* here? Name a metric in this sim where
   seed-invariance (vs n=20 jitter seeds whose spread is ≤0.0007 healthy) changes an
   accept/reject decision.

SCORES: soundness 3/5, provenance 4/5, reproducibility 4/5 (authoritative — the
*reported* numbers reproduce exactly; but the **comparative** claim vs random does not),
significance 2/5.

RECOMMENDATION: major-revision.
Reproduction of the stated single-instance numbers is clean (would be `accept` on a
pure reproducibility lens). But the fair-comparison gate this review was charged with —
golden vs a tuned random baseline across diverse instances — shows the invention's
characteristic ingredient confers no measurable advantage, and the campaign's H4/H5
"beats random" mechanism does not survive a matched-envelope comparison. The claim must
be narrowed from "deterministic LDS beats random jitter" to "a wide first-retry window
≥ outage length solves this instance (LDS and RNG equivalently)," or it must produce an
instance where LDS actually wins.

REVIEWER CONFIDENCE: 0.88 — direct execution-grounded, n=20–50 seeds per variant, matched
envelopes. Residual: my generalized simx.py reimplements the sim (reproduces V0 exactly),
and the thundering-herd model is one of several reasonable encodings.
