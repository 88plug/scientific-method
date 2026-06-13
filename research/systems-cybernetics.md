# Systems thinking & cybernetics: what the scientific-method plugin should adopt

Research date: 2026-06-12. Sources fetched via built-in WebFetch (WebSearch was
non-functional for this model; primary/canonical sources fetched directly):
Donella Meadows, *Leverage Points: Places to Intervene in a System* and
*Thinking in Systems: A Primer*; Jay Forrester, *Counterintuitive Behavior of
Social Systems* / *Urban Dynamics* / *World Dynamics*; W. Ross Ashby, law of
requisite variety (via the cybernetics "Variety" treatment + Stafford Beer's
operational restatement); Heinz von Foerster, second-order cybernetics.

Plugin files referenced throughout:
- `SKILL.md` — the loop (steps 0–7), esp. step 0 (cheapest falsification),
  step 2 (predict before measuring), step 3 (controlled experiments / but-for),
  step 4 (verdicts + confidence).
- `references/rigor.md` — §3 causal ladder (correlation→temporality→
  dose-response→controlled experiment), §4 confound blocking list.
- `references/artifacts.md` — the `EXPERIMENTS.md` ledger.

---

## Why this matters for the plugin

The plugin's causal machinery is built for **linear, separable causation**:
isolate one factor, hold confounds, apply the but-for test, grade on the causal
ladder. That machinery quietly assumes the effect post-dates and is monotone in
the cause, and that the cause sits *somewhere you can point at*. Feedback-rich
incidents — retry storms, cache stampedes, autoscaler oscillation, thundering
herds, queue collapse — violate all three assumptions:

- **The cause is the loop, not a node.** No single component is "the root
  cause" of an autoscaler that oscillates; the oscillation is a *structural*
  property of a balancing loop with a delay. Asking "which service caused it"
  is the single-cause bias the plugin already warns against (SKILL.md failure
  modes), in a form the current tooling doesn't catch because each component
  individually looks innocent.
- **The effect lags the cause by a delay**, so a naive temporality check
  ("B started after A, so A→B") mis-ranks candidates: the *trigger* fired one
  delay-length earlier than the symptom, and the thing happening right before
  the symptom is often the loop feeding back, not the original perturbation.
- **The system fights your fix** (policy resistance / compensating feedback):
  an intervention that pushes on a low-leverage point gets absorbed and the
  operator concludes "we tried that, it didn't help" when the real issue is
  *where* they pushed, not whether the diagnosis was right.

Systems thinking supplies four things the plugin lacks: a **loop-mapping step**
to represent feedback structure before assigning causes, **delay-awareness** to
fix the temporality check, **leverage-point thinking** to choose where to
intervene, and **requisite variety** as a coverage check on monitoring/probes.

---

## Part 1 — Distilled principles

### 1.1 Stocks, flows, and feedback loops (Meadows, Forrester)

- A **stock** accumulates or depletes over time (queue depth, in-flight
  requests, cache entries, connection-pool occupancy, retry-budget tokens). A
  **flow** is a rate that changes a stock (arrival rate, completion rate,
  eviction rate). Stocks are the *integral* of their net flows — which is why a
  stock keeps rising for a while *after* inflow drops below outflow, and why you
  read the stock to learn the system's state but read the flows to learn what
  it will do next.
- A **balancing (negative) loop** is self-correcting: it drives a stock toward
  a goal and resists disturbance (a thermostat, an autoscaler targeting 60%
  CPU, TCP congestion control, a load shedder). It is the source of both
  *stability* and *policy resistance*.
- A **reinforcing (positive) loop** is self-amplifying: more produces more
  (word-of-mouth growth — or a retry storm where failures generate retries that
  generate load that generates more failures). Reinforcing loops are the engine
  of every runaway incident.
- **Behavior is intrinsic to structure, not driven by external events.**
  Forrester's canonical GE result: managers blamed an external business cycle
  for a 3-year employment swing; hand-simulation showed the firm's *own*
  hiring/layoff decision rules generated the oscillation internally. The
  operational lesson for incidents: *an oscillation or runaway that "correlates
  with" an external spike is more often the system's own loop responding than
  the spike causing it directly.* Misattributing internally generated dynamics
  to an external trigger is the dominant diagnostic error in feedback systems.

### 1.2 Delays are the source of oscillation and overshoot (Meadows §9)

- **Delays in feedback loops are common causes of oscillation.** A balancing
  loop with a delay overshoots its goal because it keeps acting on stale
  information: by the time the correction's effect is visible, the stock has
  already moved past target, so the loop over-corrects the other way.
- **Delay magnitude relative to the system's rate of change sets the regime:**
  too-short delay → overreaction; longer delay → damped oscillation; longer
  still → sustained or *exploding* oscillation, even chaos. With a threshold or
  hard limit in the loop, delays produce **overshoot-and-collapse** (queue fills
  past the point of no return before the brake engages).
- **Delays are usually unalterable** ("things take as long as they take"), which
  is *why* Meadows ranks slowing the system's rate of change (or strengthening a
  faster feedback path) above shortening the delay itself.
- Diagnostic consequence: in a delayed loop the **effect lags the cause by
  roughly one loop-transit time**, and the visible symptom is frequently the
  loop *feeding back on itself*, not the original perturbation. Temporality
  ("A precedes B") is necessary but no longer sufficient to rank causes; you
  need the *delay-corrected* lead time.

### 1.3 Policy resistance / compensating feedback (Forrester, Meadows)

- Systems with strong balancing loops **resist intervention**: push on a
  parameter and the loop pushes back, so the system settles near where it was.
  Forrester's urban-dynamics result is the archetype — building low-income
  housing (the intuitive fix for a housing symptom) *worsened* the city by
  feeding the underlying job/population imbalance; the harsh-looking move
  (convert housing land to industry) was the effective one.
- **Short-term and long-term responses to a policy often have opposite signs.**
  Relief now, deterioration later (or vice versa). A fix that improves the
  symptom this hour can deepen the structural cause by next week.
- **Systems are insensitive to most parameters but acutely sensitive to a few.**
  This is the empirical basis of leverage points: ~99% of attention goes to
  parameters that "RARELY CHANGE BEHAVIOR," because they're visible and
  politically charged, while the few high-leverage points sit unnoticed.

### 1.4 The twelve leverage points (Meadows, least→most effective)

Where to intervene in a system, in *increasing* order of effectiveness. The
counterintuitive core: the points everyone reaches for first (12–9) are the
weakest, and "the higher the leverage point, the more the system resists
changing it." Forrester's barb: people often *find* the leverage point
intuitively, then "push it IN THE WRONG DIRECTION."

| # | Leverage point | Intervening here means… |
|---|---|---|
| 12 | Constants, parameters, numbers | Tune a threshold/quota/rate (retry count, timeout, replica target). Lowest leverage — "diddling the details." |
| 11 | Buffer sizes / stabilizing stocks | Resize a buffer relative to its flows (queue depth, connection-pool size). Stabilizes but is physical and slow to change. |
| 10 | Structure of stocks & flows | Redesign the physical plumbing (sharding, routing topology, network paths). High impact, slow/costly to rebuild. |
| 9 | Lengths of delays | Shorten feedback delay relative to rate of change (faster health checks, shorter scrape interval). Powerful but delays are often fixed. |
| 8 | Strength of balancing loops | Strengthen a self-correcting mechanism so it matches the impact it must counter (more aggressive load-shed, circuit breaker, backpressure). |
| 7 | Gain of reinforcing loops | *Slow* a runaway loop rather than just adding brakes (cap retry amplification, jittered backoff, request coalescing). Often beats #8. |
| 6 | Structure of information flows | Create a feedback path to an actor who lacked it (surface queue depth to the client; expose retry budget; emit the missing metric). |
| 5 | Rules of the system | Change incentives/constraints (admission control, rate-limit policy, quotas, SLO error budgets that gate deploys). |
| 4 | Power to self-organize | Let the system evolve new structure (autoscaling policy that adds new loops; chaos-driven adaptation; preserve diversity/redundancy). |
| 3 | Goals of the system | Change what the system optimizes for (target tail latency not mean; availability over throughput). Bends everything below it. |
| 2 | Paradigm / mindset | Shift the shared assumptions ("retries are free," "more capacity fixes load problems," "the cache is a detail"). |
| 1 | Power to transcend paradigms | Hold no model as final; choose the framing that fits the incident rather than the one you arrived with. |

### 1.5 Ashby's law of requisite variety

- **Only variety can absorb variety** (Ashby: "only variety destroys variety";
  Beer: "variety absorbs variety"). Formally, with **V** = number of
  distinguishable states (or log₂ of that, in bits), a regulator R can reduce
  outcome variety **V_O** to at best **V_O ≥ V_D − V_R**: the regulator must
  command at least as much variety as the disturbances it must counter. You
  cannot control what you cannot match.
- **Necessary, not sufficient:** enough variety doesn't guarantee control — the
  *structure* must also permit it (the Conant–Ashby good-regulator theorem
  sharpens this: an effective regulator must contain a *model* of the system it
  regulates).
- **Averages destroy variety, and that is sometimes the bug.** Beer's hospital
  example: a patient's fever is invisible in the *average* temperature across
  the ward; effective monitoring must *amplify* variety exactly where a small
  signal has large consequences. This is the single most transferable cybernetic
  idea for observability.
- Two ways to satisfy the law: **amplify the controller's variety** (more
  distinct sensors/responses) or **attenuate the incoming variety** (admission
  control, sharding, bulkheads that reduce the disturbance space the controller
  must face).

### 1.6 Second-order cybernetics: the observer is in the system (von Foerster)

- First-order cybernetics is the *cybernetics of observed systems*; second-order
  is the *cybernetics of observing systems* — the observer is a **participant**,
  not a detached measurer. The probe is a coupling, not a one-way read.
- Practical bite for incident diagnosis: **your measurement perturbs the
  system.** Adding a scrape, a health check, a debug log, a synthetic probe, or
  a retry-on-your-own-tooling injects flow into the very loops you're studying.
  In a feedback-rich incident this is not a rounding error — a heavier health
  check can *deepen* an overload it was meant to observe; a diagnostic replay can
  re-trigger the storm. This generalizes the plugin's existing "measurement
  perturbs" intuitions (page-cache, GPU contention) to the case where the
  *feedback loop closes through your instrument*.
- Know when first-order suffices: most probes are clean reads (Newtonian special
  case). The second-order stance becomes mandatory only when your participation
  materially shapes what you're diagnosing — which, for feedback incidents, is
  exactly the regime that matters.

---

## Part 2 — Concrete plugin adoptions

### 2.A A lightweight causal-loop-mapping step (new, slots into SKILL.md step 1)

**Trigger (keep it cheap — method weight scales with evidence cost):** add a
loop-mapping pass *only* when the incident shows feedback signatures —
oscillation, runaway/amplification, overshoot-and-collapse, or a symptom that
*persists after the apparent trigger is removed*. Retry storms, cache
stampedes / thundering herds, autoscaler flapping, queue collapse, connection-
pool exhaustion cascades, GC death spirals. For a one-shot linear fault
(a bad deploy, a null deref) skip it — the existing but-for machinery is right.

**The step** — before converting assertions into hypotheses, draw a minimal
**causal loop sketch** in the ledger:

1. **Name the stocks** (what accumulates: in-flight requests, queue depth,
   retry tokens, cache misses in flight, active replicas) and the **flows** that
   move them.
2. **Mark each loop R or B**, and put a **`//` on every arrow that carries a
   significant delay** (the standard CLD convention) — health-check interval,
   backoff window, scale-up cooldown, TTL, propagation lag.
3. **Classify the dynamic:** which loop is *dominant* right now? A runaway is a
   reinforcing loop that has out-gained its balancing brake; an oscillation is a
   balancing loop with a delay long relative to its rate.

Text-CLD notation usable in a markdown ledger (no diagram tooling needed):

```
[failures] --(+)--> [retries] --(+)--> [load] --(+)--> [failures]   R1: retry storm
                                          |
[load] --(+,//cooldown)--> [new replicas] --(-)--> [load]           B1: autoscaler (DELAYED)
```

Then — and only then — convert to hypotheses. The hypotheses become claims about
*loop structure and dominance*, e.g. "H1: R1 (retry amplification) is dominant;
disabling client retries collapses load within one round-trip" with the usual
H0 and outcome→conclusion table. This keeps step 2's pre-registration intact
while fixing what it ranges over.

**Falsification stays central:** a drawn loop is a *hypothesis about structure*,
not a fact. The cheapest falsifier of "R1 is the storm" is usually a single
counter read (retry rate vs. base request rate) or one config flip
(retries off on a canary) — exactly the step-0 "cheapest observation that kills
the leading hypothesis" discipline, now aimed at a loop instead of a node.

### 2.B Delay-awareness: fix the temporality check (amends rigor.md §3)

The causal ladder's temporality rung ("cause precedes effect") is unsound in
delayed loops. Two amendments:

1. **Delay-corrected lead time.** Before ranking a candidate cause by "it
   happened just before the symptom," estimate the loop's delay (cooldown,
   backoff, TTL, scrape interval) and look for the trigger **one delay-length
   earlier**, not immediately before. The event right before the symptom is
   often the loop feeding back, not the originator. State the assumed delay next
   to the temporality claim, the way confounds are stated next to a number.
2. **A balancing loop with a long delay manufactures correlations that invert
   under control.** Because overshoot makes the stock and the corrective flow
   move *out of phase*, a naive correlation can show the brake "causing" the
   overload (they rise together on the wrong half-cycle). The fix is the
   plugin's existing rule, sharpened: **for any causal claim inside a loop, a
   control case is mandatory** (turn the suspected loop off / break it on a
   canary), because phase relationships in delayed loops routinely produce
   sign-flipped correlations. Add to rigor.md §3: *"In a feedback loop,
   temporality and correlation are both unreliable without delay-correction and
   a loop-breaking control; grade no higher than 'temporality' until the loop is
   broken and the effect disappears."*

This also patches a named SKILL.md failure mode ("crowning one of two
jointly-necessary factors the root cause"): in a loop *every* node is
jointly-necessary, so the headline must name the **loop and its dominant gain/
delay**, not a node.

### 2.C Leverage-point thinking: choose WHERE to intervene (new, post-diagnosis)

Once a loop is mapped and a dominant loop confirmed, the **fix** is itself a
hypothesis with a leverage rank. Add a short **intervention-selection** step
before recommending a remediation:

- **Rank candidate interventions on Meadows' ladder** and prefer higher leverage
  when feasible. For the canonical incidents:
  - *Retry storm* — bumping the retry count (#12) or timeout (#12) is lowest
    leverage and often pushed the wrong way. Higher: cap the **gain of the
    reinforcing loop** (#7) via jittered exponential backoff + request
    coalescing + a retry **budget** (a token stock that admission-controls
    retries). Higher still: **rules** (#5) — circuit breaker / load shedding so
    the loop can't close.
  - *Cache stampede* — raising cache size (#11, buffer) is weak. Higher:
    **information flow** (#6) — single-flight / request coalescing so only one
    miss propagates; **rules** (#5) — probabilistic early expiration so misses
    don't synchronize.
  - *Autoscaler oscillation* — nudging the CPU target (#12) rarely settles it.
    Higher: **shorten the delay** (#9, faster metrics / shorter cooldown) *or*,
    per Meadows, **slow the rate of change** (damp scale-up gain, add
    hysteresis) — strengthening the balancing loop (#8) or reducing its delay,
    since oscillation is a delay phenomenon.
- **Pre-commit the leverage rank and the expected sign**, then verify against
  the **opposite-sign trap**: Forrester's warning is operational here —
  *predict short-term AND long-term effect signs separately* in the
  outcome→conclusion table, because a fix that helps this hour can deepen the
  loop next week. A remediation whose long-term sign is unknown is a
  `prototype`, not `confirmed`.
- **Policy-resistance check before declaring a fix dead.** If an intervention
  "didn't help," ask whether it pushed a *low-leverage* point that the system's
  balancing loop simply absorbed — that is a wrong-location result, not a
  wrong-diagnosis result. Don't add it to the falsification log as
  DO-NOT-RE-ATTACK until you've confirmed it was aimed at the dominant loop's
  actual leverage point.

### 2.D Requisite variety as a monitoring/probe coverage check (new gate)

Ashby's law gives the plugin a *principled* answer to "is our observability good
enough to diagnose this?" — a question step 0 ("cheapest falsification") and the
INCONCLUSIVE verdict both implicitly depend on but never test.

- **Coverage gate:** the variety of your *probes/metrics* must be ≥ the variety
  of the *failure modes / disturbances* you need to distinguish. If three
  distinct loop-failures (storm vs. stampede vs. oscillation) all collapse to
  the same observable ("p99 latency up, error rate up"), your monitoring variety
  is **below requisite** and any root-cause verdict is structurally
  underdetermined — the honest verdict is **INCONCLUSIVE with a named missing
  probe** (the per-loop discriminator), exactly the plugin's existing
  first-class deliverable, now with a reason it's forced rather than a judgment
  call.
- **The averages-hide-fevers rule.** Beer's fever example maps directly onto SRE
  practice: a *mean* or even a coarse histogram can hide the per-shard, per-key,
  per-tenant signal that distinguishes loops (one hot cache key driving a
  stampede vanishes in aggregate hit-rate). Add to the probe-design checklist:
  *"Does any probe average across a dimension where a single outlier is the
  signal? If so, variety is being destroyed at the instrument — disaggregate
  before concluding."* This is the same discipline as the plugin's "measure
  against ground truth, not metadata," extended to "don't let aggregation
  metadata stand in for the per-unit ground truth."
- **Two ways to pass the gate**, both actionable: *amplify* probe variety (add
  the discriminating metric / per-key cardinality) or *attenuate* disturbance
  variety (shard/bulkhead so fewer failure modes can reach one component) — and
  note that the attenuation option is itself a leverage-#5/#10 intervention,
  tying the variety gate back to §2.C.

### 2.E Second-order check: the probe is in the loop (amends step 3 confounds)

Add one line to the confound-blocking list (rigor.md §4) specifically for
feedback incidents: **"Does this probe inject flow into a loop it observes?"**
Health checks, synthetic traffic, debug logging, diagnostic replays, and
retry-on-your-own-tooling all *close the loop through your instrument*. In a
runaway or near-overload regime, a heavier observation can deepen the very
dynamic it measures (observer-as-participant, von Foerster). Mitigations:
prefer passive/existing telemetry over active probing during a live storm;
when active probing is unavoidable, treat your own probe rate as a flow in the
CLD and account for it; run the diagnostic replay on an *isolated* canary so the
loop you re-trigger can't feed back into production. This is the plugin's
"measurement perturbs the system" intuition (already present for page-cache and
GPU contention) generalized to the case the new loop-mapping step makes visible.

---

## Part 3 — Net additions, smallest-footprint version

If only the highest-leverage subset is adopted, it is these four, in order:

1. **Loop-mapping trigger + text-CLD (§2.A)** — gated on feedback signatures so
   it stays cheap. Makes "the cause is the loop, not a node" representable.
2. **Delay-corrected temporality + mandatory loop-breaking control (§2.B)** — a
   one-paragraph amendment to rigor.md §3 that prevents the most common
   feedback-incident misdiagnosis.
3. **Requisite-variety coverage gate (§2.D)** — turns "INCONCLUSIVE" from a
   judgment call into a derivable verdict when probe variety < failure-mode
   variety, plus the averages-hide-fevers disaggregation rule.
4. **Leverage-rank the fix + opposite-sign prediction (§2.C)** — stops the
   plugin from validating a *correct diagnosis* attached to a *low-leverage,
   policy-resistant fix*.

§2.E (observer-in-the-loop) is a single confound-list line; cheap to add,
high payoff exactly in the live-storm regime.
