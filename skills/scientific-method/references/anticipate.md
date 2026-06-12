# Anticipation & hypothesis generation: the abductive front half

The campaign loop is a strong falsification engine and, by itself, a weak
generation engine — step 1 *sweeps existing assertions* into hypotheses, which
presupposes the hypotheses exist. Peirce named the missing operation: the loop
already does deduction (the outcome table) and induction (the verdict), but
**abduction — the only operation that introduces a new idea — is left
implicit**. This reference makes it explicit: mechanical generators so the
hypothesis pool is built by procedure, not by whatever came to mind first.
Everything generated here still terminates in the gate — a ledger row with a
probe — or it isn't a hypothesis. And every invention pass ends with an
**explicit provenance partition** — every mechanism tagged "known technique
(named)", "no prior art found (with the documented search log)", or
"unsearched" — not as an afterthought but as a required output; implicit
familiarity is how known structures get re-presented as inventions, and an
unsearched mechanism is never presented as new.

(Provenance note: "cheapest falsification first" is Peirce's *economy of
research* — rank inquiries by cost, caution, and breadth — a century before
this plugin. The full rule: probe rank ≈ expected information ÷ cost, with the
danger override below.)

## 1. Pre-mortem FMEA — before risky or irreversible changes

Klein's pre-mortem framing plus a lightweight FMEA: assume the change shipped
and failed; enumerate how. For each plausible failure mode, score 1–5:

| failure mode | Severity | Occurrence | **Detectability** | probe/mitigation |
|---|---|---|---|---|

- **Detectability is the software-critical axis.** A failure mode that is
  silent until users hit it (D ≥ 4) is a finding *by itself*; the mitigation
  is "add the test/alert/assert," shipped with the change.
- The output is an **ordered probe queue** feeding the existing halving
  ladder, not a risk score. Do not do arithmetic on S×O×D (RPN rank-reversals
  are a known defect) — it is a triage sort only.
- JPL's institutional lesson on why this is worth 20 minutes: Mars Polar
  Lander died from a sensor transient that was *visible in test data* but
  never run under flight-like conditions. The pre-mortem is where "what
  haven't we run under real conditions?" gets asked while it's still cheap.

## 2. Key-assumptions check — step 1.5 of any campaign

Before designing probes, list the assumptions the problem statement rests on
and classify each: **solid** (evidence in hand), **caveated** (holds within
stated limits), **unsupported** (load-bearing but unverified). Every
unsupported load-bearing assumption is promoted to a numbered hypothesis.
Record them in the ledger's Assumptions block (artifacts.md) — most
confidently-wrong verdicts trace back to an assumption nobody wrote down.
JPL's version: **heritage is a trap, not a credential** — "it worked last
mission/quarter" is an assumption to verify, not a reason to skip verifying.

## 3. Coverage generators — building the differential

When the stakes justify breadth, run the hypothesis sweep against checklists
instead of intuition (the cure for premature closure — clinicians call the
result a differential, and anchoring on the first plausible diagnosis is a
*named* error there):

- **Category sweep (fishbone, software-tuned):** code change · config/flag ·
  data/input shape · dependency/version · infrastructure/hardware · timing/
  concurrency · external actor/traffic · measurement/instrumentation. One
  candidate per category or an explicit "none plausible because…".
- **Unsafe-control-action taxonomy (STAMP):** for any system where a
  controller acts on a process — autoscaler, retry logic, scheduler, operator
  — generate four hypotheses mechanically: the needed action was **not
  provided** / was **provided but unsafe** / came at the **wrong time or
  order** / lasted the **wrong duration**. Exhaustive by construction.
- **Contradiction lenses (TRIZ), for ceiling campaigns:** state the wall as a
  contradiction ("we need X fast AND X correct") and require all four
  separations to have recorded outcomes before filing it as a trade-off:
  separation in **time**, in **space**, by **condition**, and between
  **system levels** (component vs whole). Then ask the **ideal final result**
  — "the function delivers itself at zero cost" — and treat the gap between
  IFR and baseline as the headroom estimate. Walls survive this rarely.

## 4. Stuck-pool escalation — before declaring a pass "dry"

A dry pass is only meaningful if the generator was varied (Goertzel's
cognitive synergy: when one reasoning process hits a wall, a *different*
process supplies the move). Before declaring dry, cycle modes:

1. **Logical** — re-derive from the evidence table; what do the anomalies
   jointly entail?
2. **Analogical** — what known incident/system does this resemble, and what
   was true there? (Then verify the analogy's load-bearing parts — analogies
   generate, they never confirm.)
3. **Recombinative** — combine surviving partial hypotheses; the jointly-
   necessary-cause pattern means two weak candidates may be one true pair.
4. **Probabilistic** — rank residual anomalies by surprise under the current
   best model; the most surprising one seeds the next hypothesis (Peirce's
   abduction schema: a surprising fact is the trigger — Twyman's law is the
   same instinct).

Only after all four modes return nothing new is the pass dry.

## 5. Probe-ordering: the danger override

Information-gain ordering (rigor.md §1) assumes probe outcomes are reversible
and comparably priced. Clinical practice adds the override: **when a
hypothesis's miss is irreversible, rule out the catastrophic-but-improbable
first**, ordering by danger × treatability ÷ probe-cost, and demand a
*stricter* threshold to dismiss it. Same Bayesian object, different loss
function — minimum expected probes vs minimum expected catastrophic loss. In
engineering terms: before optimizing the investigation, confirm the building
isn't on fire (data loss, security exposure, corruption-in-progress).
