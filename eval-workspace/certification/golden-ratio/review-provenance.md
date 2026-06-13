# Peer review — PRIOR-ART / PROVENANCE lens

Submission: deterministic golden-ratio / low-discrepancy retry timing.
Reviewer: blind, prior-art/provenance lens. Date: 2026-06-12.
Independence: I ran my own searches (exa neural web, DuckDuckGo HTML, Google
Patents page-fetch, registry queries); a no-prior-art conclusion is grounded
in MY log below, not the submitter's. Tooling available this session:
`mcp__exa__web_search_exa`, `WebFetch` (DuckDuckGo HTML + direct fetch). arXiv
API / Google-Patents XHR were reachable indirectly via these.

Claim elements (carried from the submission, unchanged):
- **E1** application-layer client **retry/backoff timing** for fault recovery
- **E2** delay source is a **deterministic low-discrepancy / golden-ratio
  (Weyl/Kronecker/van-der-Corput) sequence**, not an RNG
- **E3** goal is **outage-recovery anti-clustering** (thundering-herd avoidance)
- **E4** a **provable / analytic** (bounded-gap / bounded-discrepancy)
  uniformity guarantee, not simulation

---

## What I read first (the submitter's existing logs)

- `research/prior-art-pilot.md` — pilot: 13 queries. Closest: AWS decorrelated
  jitter (random, simulation-justified); demofox golden-ratio weighted-RR (load
  selections, not retry); QMC theory; `backofflite` (formula/seeded-PRNG
  "deterministic", not LDS); MAC-contention patents (Benveniste/ZTE).
- `eval-workspace/iteration-10/r10s07/.../search-log-extended.md` — added
  exa, crates.io API, arXiv cross-term, Weyl/Kronecker, thundering-herd, φ-
  competitive families. New closest: ICDE-2000 golden-ratio/Kronecker
  **declustering** (data across disks); AWS Builders' per-host deterministic
  *scheduled-work* jitter; Steinhaus three-distance theorem (the E4 foundation).
- `eval-workspace/iteration-12/r12s10/.../search-log-r12s10.md` — admission-
  control / load-shedding family. Closest: Kestra deterministic dispatch
  pacing (global rate limiter, not per-request LDS). Flagged that
  `research/prior-art-pilot.md` was "absent on disk" at r12s10 time — I
  confirm it **does exist now** at the repo root (the r12s10 auditor was
  looking under `eval-workspace/` only; the file lives at
  `research/prior-art-pilot.md`). So that provenance-witness gap is resolved.

Families already covered by those three logs: LDS/golden-ratio↔retry,
Weyl/Kronecker, thundering-herd/de-sync, φ-competitive/three-distance,
declustering, QMC, admission-control/load-shedding, crates registry, arXiv
cross-term, MAC-contention patents.

## NEW query families I ran (not in any prior log)

| # | Venue | Query family | Closest hits | Anticipates? |
|---|---|---|---|---|
| P1 | exa | **phase dithering / phase-offset** applied to retry timers to spread clients | All hits = the canonical **random**-jitter corpus (AWS Full/Decorrelated, Google Cloud, Stripe-style, linera-io PR#5440 replacing linear→full-jitter, MortalApps/OneNoughtOne). "Deterministic = synchronized = bad" is the stated framing; remedy is always randomness. | **No.** No phase-dithering-as-LDS source; "deterministic" appears only as the *anti-pattern* to be removed. |
| P2 | exa | **Halton / Sobol sequence for scheduling network/distributed events** instead of random | **Halton Scheduler for MaskGIT** (arXiv 2503.17076) — a *deterministic Halton low-discrepancy scheduler* that "spreads out tokens to achieve uniform coverage… minimal clustering," explicitly **replacing** a confidence/stochastic scheduler. Also MANET topology-transparent **deterministic sequence** TDMA scheduling (arXiv 2006.07668); Halton/Sobol QMC + hardware LDS generators (background). | **No** — but P2 is the **closest-on-mechanism+intent NEW neighbor**: same move (swap a random/greedy scheduler for a deterministic LDS to get uniform spread with minimal clustering). Differs in domain: it schedules **image-token unmasking positions**, not **retry delays in time**, and has no fault/outage/retry framing or a thundering-herd target. |
| P3 | exa + direct | **deterministic backoff / jitter patent** for retransmission timing | **US11419038B2 "Deterministic backoff with collision avoidance"** (Intel) — a genuinely **deterministic (non-random) backoff** scheme. Plus US8422450B2 (R-DEB), US20110007656A1, AT&T US7245604 "Fixed Deterministic Post-Backoff", US7664132B2, US20020026523A1. | **No.** I fetched US11419038B2 in full: it is **MAC-layer 802.11 / 6 GHz channel access** (CSMA-CA, H04W74), backoff = `10+i` with i = observed CCA-busy interruptions, newcomers join an empty **round-robin slot** — **not** a low-discrepancy/golden-ratio sequence, **not** application-layer client retry, target is **medium contention** not outage retry-storm. The whole family is MAC-layer round-robin/slot determinism (same domain as the pilot's Benveniste/ZTE patents); one missing element (E2 LDS) + wrong domain (E1) defeats anticipation. |
| P4 | exa | **binary-exponential-backoff stability / throughput academic literature**, deterministic alternatives | Aldous-conjecture instability proof (arXiv 2203.17144); Goldberg/Lapinskas; Bender "How to Scale Exponential Backoff"/Re-Backoff & sawtooth; Kwak "On the Stability of EB" (PMC); SICOMP "Analysis of Backoff Protocols"; Decodable Backoff (arXiv 2207.11824). | **No.** This is the formal backoff-theory corpus the pilot named; every protocol is **randomized** (or *polynomial/sawtooth* deterministic *schedules*, never an LDS *jitter source*). Re-Backoff even has an **outage/resource-unavailable** robustness result — but via randomized exponential search, not an LDS. Confirms E2 is unoccupied in the theory literature. |
| P5 | exa | **LDS / quasi-random sequence to schedule packet-transmission times or congestion-control timing** | **Whack-a-Mole: Deterministic Packet Spraying** (arXiv 2509.18519, Sep 2025) — "deterministic packet spraying… with **provably tight discrepancy bounds**," uses a **bit-reversal counter** (van der Corput / LDS) to choose a path per packet, discrepancy **O(log m)** over any contiguous sequence, **responds to congestion feedback** by shifting load off degraded paths. Also Smoothed/Stratified Round Robin (Weight-Spread Sequence to de-burst), RED (even-spaced marking to avoid global sync). | **No** — but P5 is the **closest-on-mechanism+guarantee NEW neighbor overall**: deterministic LDS-style (bit-reversal) source + **provable discrepancy bound** + a **degraded→healthy recovery/congestion** context, in **networking**. Differs in the spread *dimension*: it allocates packets across **spatial paths** (path index), not **retry delays across time**, and "recovery" = path-degradation rerouting, not service-outage client retry. E1 (retry timing) and E3 (outage-recovery retry storm) are not taught. |
| P6 | DDG HTML | **npm / PyPI / Go retry libraries** with deterministic-jitter option | npm: p-retry, exponential-backoff, nano-retry, async/promise-retry, retry-axios. PyPI: tenacity, backoff. All random "full jitter"; `backoff`/tenacity allow a *custom* jitter fn but ship none that is LDS. | **No.** No registry library offers golden-ratio/Halton/Sobol/LDS jitter. Confirms the pilot's crates.io `total:0` extends to npm/PyPI/Go. The nearest deterministic *schedule* anyone ships is **Fibonacci** (botneve.com table), which is not an LDS. |

Saturation: P1 and P6 returned only the already-mapped randomized-jitter
corpus; a final golden-ratio/bit-reversal↔retry-timing query (re-run of the
E2×E1 cross-term) surfaced nothing past P1/P5. A full new-family sweep found
two genuinely new neighbors (P2 Halton-scheduler, P5 Whack-a-Mole) and one new
patent (P3 US11419038B2); none anticipates. I call saturation.

---

SUMMARY: The submission claims deterministic low-discrepancy (golden-ratio /
Weyl-Kronecker / van-der-Corput) retry-delay timing (E2) for application-layer
client retries (E1) to provably (E4, bounded-gap / three-distance) avoid
retry-clustering during outage recovery (E3), contrasted with AWS-style random
decorrelated jitter. The evidence base is three search logs plus the
mathematical three-distance/QMC foundation.

LENS: prior-art / provenance. I ran 6 NEW query families (phase-dithering;
Halton/Sobol-for-scheduling; deterministic-backoff patents; BEB-stability
theory; LDS-for-packet/congestion-timing; npm/PyPI/Go registries) across exa,
DuckDuckGo HTML, and direct Google-Patents fetch, beyond the three prior logs.
I fully fetched US11419038B2 and arXiv 2509.18519 / 2503.17076 to confirm how
each differs. Log above.

STRENGTHS:
- The four-element composition (E1∧E2∧E3∧E4) survives an independent extended
  search. No single reference teaches all four in the claimed arrangement.
- The submission's verdict grammar is correct: it names closest-found
  neighbors and how each differs, never an unsearched superlative, and lists
  coverage gaps — exactly the invent.md §2 protocol.
- The provenance trail is real and now witnessed: all three logs exist on disk
  (I resolved the r12s10 "pilot absent" flag — wrong directory, file is at
  `research/prior-art-pilot.md`).
- The field demonstrably **teaches away**: every retry source (AWS/Google/
  Stripe/Finagle, the BEB-stability theory corpus, every registry library)
  reaches for **randomness**; the one place it uses determinism (no-jitter) is
  branded an anti-pattern. This strengthens the combination-test verdict.

WEAKNESSES:
- [non-blocking] **Whack-a-Mole (arXiv 2509.18519, Sep 2025)** is a tighter
  mechanism+guarantee neighbor than anything in the prior logs: deterministic
  bit-reversal (van der Corput = LDS) spreading WITH a provable O(log m)
  discrepancy bound, in a networking recovery/congestion context. It is NOT
  anticipation (it spreads packets across *paths*, not retries across *time*;
  no retry/outage-storm framing), but the disclosure MUST cite it as the
  closest-on-mechanism+guarantee art and articulate the time-vs-path-dimension
  and retry-vs-spray distinction, or a reviewer/examiner will raise it first.
- [non-blocking] **Halton Scheduler (arXiv 2503.17076)** is direct precedent
  for the *generic move* "replace a random/greedy scheduler with a deterministic
  LDS to spread events and minimize clustering." Combined with Whack-a-Mole, an
  obviousness/taught-as-combination challenge becomes plausible: the ingredients
  (LDS-as-deterministic-spreader; the retry-storm problem; the three-distance
  bound) are each now well documented. The claim's novelty rests on E1+E3
  (retry-timing + outage-recovery) specifically — the disclosure should foreground
  that, not the LDS mechanism (which is increasingly occupied across domains).
- [non-blocking] **US11419038B2** is a new deterministic-*backoff* patent (vs the
  pilot's contention patents). It does not read on the claim (MAC-layer, round-
  robin slot, no LDS) but the disclosure should name it so the "deterministic
  backoff" keyword space is shown searched.
- [non-blocking] Residual gaps persist: Google Patents XHR/full patent search
  was reached only by per-page fetch (no bulk XHR this session); Semantic
  Scholar and GitHub code-search remain auth-gated. A buried patent or code
  impl is still possible. Verdict stays "no anticipating reference in the
  searched corpus," never absolute.

QUESTIONS FOR AUTHORS:
1. How does the claim distinguish over **Whack-a-Mole (arXiv 2509.18519)** —
   deterministic bit-reversal/van-der-Corput spreading with a provable O(log m)
   discrepancy bound in a network-recovery context? Name the load-bearing
   difference (spread dimension = time-delay vs path-index; trigger = client
   retry vs per-packet spray) in the disclosure.
2. Given the **Halton Scheduler (2503.17076)** establishes "swap random
   scheduler → deterministic LDS for uniform spread" as a known move, what makes
   applying it to *retry-delay timing* non-obvious (taught-away evidence:
   the entire retry corpus reaches for randomness)?
3. Confirm the E4 guarantee is anchored to the **Steinhaus three-distance
   theorem** for {nα} with α=φ (cited, not claimed as novel), and state the exact
   bounded-gap inequality you prove — so soundness can check it against P5's
   O(log m) discrepancy framing.

SCORES: soundness 4/5, **provenance 4/5 (authoritative)**, reproducibility 4/5,
significance 3/5.
  (Provenance 4 not 5: the composition genuinely survives an independent
  extended search and the verdict grammar is correct, but two new same-domain-
  adjacent neighbors — Whack-a-Mole's deterministic-LDS-with-provable-discrepancy
  and the Halton-scheduler's "LDS-replaces-random-scheduler" move — are close
  enough on mechanism+guarantee that the novelty now rests narrowly on E1+E3
  (retry-timing + outage-recovery), and the patent/Scholar/code-search gaps keep
  it below a perfect score / below an external-filing rung.)

ANTICIPATION VERDICT: **Not anticipated.** No single reference teaches E1∧E2∧E3∧E4
in the claimed arrangement. Closest found: Whack-a-Mole (E2+E4 + network-recovery,
missing E1 retry-timing and E3 retry-storm — spreads packets across paths, not
retries across time); US11419038B2 (deterministic backoff but MAC-layer slot, no
E2 LDS, no E1 app-layer retry); Halton Scheduler (E2 LDS-as-deterministic-
scheduler but image-token domain, no E1/E3/E4-as-retry); AWS decorrelated jitter
(E1+E3 but random, simulation-justified, missing E2+E4).

COMBINATION VERDICT: **Not taught-as-combination — teaching-away dominates.** The
ingredients (LDS even-spread; its three-distance/discrepancy bound; the retry-
storm problem) are each well established and now MORE thoroughly documented as
known (P2, P5 add fresh LDS-spreader precedent). But no source *motivates* a
competent engineer to swap the RNG in decorrelated jitter for an LDS as the
retry-delay source: the retry corpus (AWS/Google/Stripe/Finagle, the BEB-
stability theory line, every registry lib) uniformly reaches for **randomness**
as the de-synchronizer, and the one deterministic retry idiom (no-jitter) is
branded an anti-pattern. The composition is taught-away-from, not taught-as-
combination — though the rising LDS-as-spreader precedent (P2/P5) means an
obviousness challenge is no longer trivial and the disclosure must pre-empt it.

RECOMMENDATION: **minor-revision** — the novelty survives, but the disclosure
must cite and distinguish Whack-a-Mole (2509.18519), the Halton Scheduler
(2503.17076), and US11419038B2, and re-anchor the stated novelty on E1+E3
(retry-timing + outage-recovery) rather than the LDS mechanism alone.

REVIEWER CONFIDENCE: 0.8 — broad independent multi-venue search with the two
strongest new neighbors fetched in full; held below 0.9 by the un-closable
gaps this session (no bulk patent XHR, Semantic Scholar + GitHub code search
auth-gated), behind which a buried patent or implementation could still sit.
