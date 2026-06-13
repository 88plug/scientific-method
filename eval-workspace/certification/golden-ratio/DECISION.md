# AREA CHAIR DECISION — deterministic golden-ratio LDS retry timing

**Submission:** `DecorrelatedSpreadPolicy` — deterministic golden-ratio (φ⁻¹ low-discrepancy)
first-retry delay timing, claimed to *provably avoid retry clustering during outage recovery,
beating random decorrelated jitter on amplification and healthy-success.*

**Round:** 4 blind reviews (soundness, reproducibility, fatal-flaw, provenance) + executable
attack/check artifacts. Area chair re-ran the fatal-flaw attack sims as required.

---

DECISION: **reject**

---

## (1) DECISIVE EVIDENCE — ranked by what was executed

I weigh by execution, not by vote. Three of four reviewers independently arrive at the **same
root cause** through different lenses; the fatal-flaw review converts it into a falsification I
re-ran and reproduced.

1. **[KILL — fatal-flaw, executed in the submission's own harness, area chair re-verified]**
   The entire low-discrepancy spread is produced by `self.ctr`, a **single module-level counter**
   incremented once per request across the whole sim. `sim.py` instantiates exactly **one** shared
   `_policy`, so all 120k requests draw distinct slots `ctr·φ mod 1` — a god's-eye sweep that no
   population of independent distributed clients can have. The claim is explicitly a *client* retry
   policy beating *per-client* random jitter, i.e. the distributed-fleet regime.

   Re-running the policy with **one instance per request** (the one-line change a real client
   forces) — byte-identical `sim.py` otherwise — **I reproduced the inversion exactly**:

   ```
   submission_shared (god's-eye global ctr): peak 1.0  p99 0  healthy 1.0   ← their result
   independent_det   (per-client by attempt): peak 1.0  p99 0  healthy 0.9091 ← FAILS (<0.995)
   independent_rand  (per-client jitter)     : peak 1.0  p99 0  healthy 1.0   ← PASSES
   ```

   And the cross-client attack, re-run: 30,000 independent clients all failing at the outage
   instant → **30000 retries in 1 one-second bin** (both phase-by-attempt and per-client-local-
   counter schemes), a **70× worse** thundering herd than the random jitter (peak 483/70 bins) the
   submission claims to beat. **The thesis inverts under the exact failure pattern the title
   invokes.** This is one failed reproduction, executed, in the submission's own sim — it outweighs
   every approving observation on the in-process numbers.

2. **[CORROBORATION — soundness, machine-checked against the byte-identical sim]** Independently
   identified the same load-bearing dependence: the anti-clustering guarantee is a property of
   *consecutive values of one shared global counter* (`check_phase.py` regime B1: 30000 requests →
   a single 1-second bin vs random's 483). Removing the shared counter in-sim collapses
   healthy_success to **0.9091** — the identical number the fatal-flaw review and I obtained by a
   different route. Soundness also killed the comparative claim at the **submitted** operating
   point: at the policy's own window `[31,101]`, plain `random.random()*span` jitter scores
   1.0/0/1.0 on every seed — identical to golden. The win is the **envelope (width + base-31)**,
   which random jitter shares; the golden sequence contributes nil.

3. **[CORROBORATION — reproducibility, fair-comparison gate, n=20–50 seeds/variant]** Across 7 sim
   variants, **LDS ≈ RNG at matched envelopes everywhere**: wherever golden passes 1.0/0/1.0 a tuned
   jitter baseline in the same envelope passes identically; wherever golden fails (V2 long-outage,
   V3 tight-cap), jitter fails identically. The H4/H5 "random caps at 0.997, determinism fixes it"
   story is an artifact of comparing a tuned golden envelope `[31..101]` (→1.0) against a
   differently-tuned random one `[30..90]` (→0.9968) — apples to oranges. At a **matched** envelope
   the perfect 1.0 belongs to the envelope, not the golden ratio.

4. **[secondary, executed]** Quantization to a real timer grid caps distinct slots at `window/grid`
   regardless of φ (5s grid → 15 slots, ≥2000 clients/slot); correlated restart re-collides
   (30000/1 bin); the only repair — a per-client random phase offset `u0~U(0,1)` — **is literally
   AWS/Brooker (2015) decorrelated jitter**, with the golden ratio rendered decorative. "Decorrelated
   jitter without an RNG" is self-contradictory: the decorrelation *is* the RNG.

## (2) HONEST RESIDUE — what survives

The reproduction is clean and three findings survive as true-but-not-novel-or-not-as-claimed:

- **The in-process, single-coordinator scope where the math holds.** For one process / one shared
  monotone counter, the three-distance theorem and equidistribution are real and survive integer-
  second quantization (soundness checked every N∈{70,…,30k}; golden max-per-second bin within +1 of
  ideal). This is a correct statement about **one ordered stream from one counter** — not a client
  retry policy. It is the QMC fact, not an invention.

- **The envelope finding (the only deployable nugget).** "A first-retry window wide enough to clear
  the outage, with base ≥ outage length, bounds the recovery herd" is real and reproduces — but it is
  **LDS-agnostic**: random jitter in the same envelope achieves it identically. The shippable lesson
  is "size the window," not "use the golden ratio."

- **Provenance is genuinely clean (minor-revision lens) but moot.** No anticipating reference;
  three new closest neighbors surfaced (Whack-a-Mole arXiv 2509.18519 — deterministic van-der-Corput
  spreading with provable O(log m) discrepancy in network recovery; Halton Scheduler 2503.17076;
  US11419038B2). Novelty of the *combination* survives a clean search. **But novelty does not rescue a
  claim that fails under its own target regime** — a non-anticipated mechanism that inverts in
  deployment is non-anticipated *and wrong*. Provenance's minor-revision is correct on its own lens and
  correctly overruled at the round level.

Net: nothing survives **as submitted**. The claim "deterministic LDS beats random jitter for outage-
recovery retry timing" is falsified; what is left is either a textbook QMC fact (in-process) or
envelope-sizing (LDS-agnostic), neither of which is the submission.

## (3) LEDGER MAPPING — kill → falsification log, DO-NOT-RE-ATTACK

```
LEDGER ENTRY (paste into EXPERIMENTS.md):
| H(golden-LDS-retry) | KILLED | reject | Deterministic φ⁻¹ LDS retry timing inverts under
independent-client outage: per-client instance → 30000/1-bin herd, healthy 0.909<0.995 (re-verified
in submission's own sim); LDS≈RNG at matched envelope (n=20–50); spread depends on a shared global
counter no distributed fleet has. Win = envelope width+base, not the golden ratio. Repair = per-client
random jitter = AWS/Brooker 2015 (prior art it claimed to beat). DO-NOT-RE-ATTACK. |
```

**kill_reason:** The anti-clustering guarantee is a property of consecutive draws from a **single
shared monotone counter**. No population of independent distributed clients possesses that counter;
each client computing a deterministic golden delay from its own attempt index produces the *identical*
value, synchronizing the fleet into a maximal herd (30000→1 bin, healthy-success 0.909) — the exact
thundering herd the submission claims to prevent, and strictly worse than the per-client random jitter
it claims to beat. The only working repair re-introduces per-client randomness, which IS decorrelated
jitter (AWS/Brooker 2015); "decorrelated jitter without an RNG" is self-contradictory. Re-verified by
the area chair in the submission's byte-identical sim.

**DO-NOT-RE-ATTACK** the family "RNG-free / deterministic LDS as the cross-client retry-delay
de-synchronizer." The decorrelation work is done by per-client entropy by construction; removing the
RNG removes the decorrelation. Re-running with retuned base/span/φ does not address the shared-counter
assumption and is explicitly out of bounds.

**Precise reopen condition (single, narrow, and currently self-contradictory):**
Reopen ONLY if a future submission exhibits a **per-client-phase** variant `delay = base + ((u0_c +
k·φ) mod 1)·span` that:
  (a) is shown to **differ from** decorrelated random jitter (i.e. the per-client phase `u0_c` is
      derived without per-client entropy — e.g. from a coordination-free, collision-free, durable
      client identifier), AND
  (b) is shown to **beat** decorrelated jitter on a stated acceptance metric across ≥5 independent-
      client variants by more than seed noise.
The fatal-flaw review argues (a)∧(b) is self-contradictory: any `u0_c` that de-synchronizes
independent clients must carry per-client entropy, at which point it *is* jitter and (a) fails; any
`u0_c` without entropy collides and (b) fails. The reopen bar therefore requires first dissolving that
contradiction with a concrete coordination-free distinct-phase source — absent that artifact, the kill
stands and the family stays closed.

## (4) WHAT THIS ROUND PROVES ABOUT THE CERTIFICATION PIPELINE

**The structural lesson: acceptance, reproduction, and provenance all PASSED a claim that peer review
KILLED — because the first three gates validate the artifact against itself, and only an adversarial
lens validated it against its own deployment regime.**

- **Acceptance** (peak 1.0 / p99 0 / healthy 1.0) passed — but it scored the *artifact's own god's-eye
  shared-counter sim*, the one instance where the trick works.
- **Reproduction** passed *verbatim* — and would have been a clean `accept` on a pure reproducibility
  lens. Reproducing the number faithfully reproduced the **wrong configuration** faithfully. Bit-exact
  reproduction certifies *the experiment was the experiment*; it cannot certify the experiment modeled
  reality.
- **Provenance** passed (no anticipation, clean search). Novelty is **orthogonal to correctness**: the
  mechanism is both non-anticipated and wrong.

All three are **self-referential gates** — they ask "does the artifact do what it says *in the
configuration the author chose*?" The kill came only from the **fatal-flaw lens changing the
configuration** (one policy instance per request) to match the regime the *claim* targets. The
single load-bearing assumption — that `self.ctr` is a shared global counter — was never stated in
the artifact, so every self-referential gate inherited it silently and the VERDICT's 0.97 confidence
named only parameter-retuning as its residual, never the cross-client assumption that governs the
result.

**Pipeline implication:** a green acceptance + clean reproduction + clean provenance is **necessary
but not sufficient** for CONFIRMED. The certification pipeline needs an **adversarial-regime gate
before the confirmation rung** — a lens charged with restating the claim's deployment regime and
re-running the artifact under it (here: "it's a *client* policy → score it with independent clients").
Three reviewers found the same defect by three routes; had the round shipped on the first-three gates
alone, a falsified claim would have been certified CONFIRMED. **Reproducibility is not validity; the
fair-comparison and target-regime baselines must be inside the gate, not optional downstream reviews.**

---

REBUTTAL ASSESSMENT: No author rebuttal was submitted for this round. The three blocking weaknesses
(shared-counter dependence; comparative claim false at matched envelope; prior-art collision /
self-contradiction) therefore carry unanswered to the decision, and a rebuttal could only answer them
with the very artifact the reopen condition demands — which the fatal-flaw review argues cannot exist.

DISSENT ON RECORD (preserved, overruled):
- **Provenance — minor-revision** (verbatim gist: "novelty survives an independent extended search;
  cite Whack-a-Mole / Halton-Scheduler / US11419038B2 and re-anchor novelty on E1+E3"). *Overruled:*
  correct on its own lens (the composition is genuinely not anticipated), but novelty cannot certify a
  claim that inverts under its target regime. Its three new-neighbor citations are preserved as useful
  prior-art record should the narrow reopen condition ever be met.
- **Reproducibility's own note** that on a *pure* reproducibility lens this is `accept`. *Overruled
  and promoted to the central lesson:* verbatim reproduction of a self-chosen configuration is exactly
  how a falsified claim reaches the confirmation rung — see §4.
