# Prior-art search via WebFetch — venue playbook + live pilot

Built for an offline-ish Claude Code agent where the `WebSearch` tool errors out and
only `WebFetch` (URL -> markdown -> small-model extraction) is available. Part 1 is the
reusable venue/query playbook. Part 2 is a live pilot run end-to-end against one
candidate invention, with the full search log and a no-prior-art-found verdict.

Date: 2026-06-12. Tooling: `WebFetch` only. `gh` CLI is unauthenticated in this env
(returns `gh auth login`), so GitHub is reached via web/HTML/raw URLs, not the API.

---

## Part 1 — Venue playbook (what actually works via WebFetch)

WebFetch upgrades HTTP->HTTPS, caches per-URL for 15 min, and returns cross-host
redirects to you instead of following them. JS-rendered SPA pages come back empty —
so the trick is to hit the JSON/HTML/API endpoint *behind* the SPA, not the SPA route.

### Tier 1 — works reliably, use these first

| Venue | Working URL pattern | Covers | Notes |
|---|---|---|---|
| **DuckDuckGo HTML** | `https://html.duckduckgo.com/html/?q=<terms>` | General web: blogs, docs, GitHub repos, papers surfaced indirectly | The workhorse. Server-rendered, no JS. Returns ~10 titles+URLs+snippets. URL-encode spaces as `+`. Beware term collisions ("jitter" -> EE clock jitter); add domain words to disambiguate. |
| **arXiv API** | `http://export.arxiv.org/api/query?search_query=all:<terms>&max_results=N` | CS/math preprints (cs.DC, cs.NI, math.NA, etc.) | Best academic venue. Returns real titles + full abstracts as clean Atom XML. Use `all:`, `ti:`, `au:`; combine with `+AND+`, quote phrases as `%22...%22`. No rate limits hit. |
| **arXiv listing** | `https://arxiv.org/list/cs.DC/recent` | Browse-by-category recent papers | Server-rendered; confirms a category's current contents. |
| **Google Patents XHR** | `https://patents.google.com/xhr/query?url=q%3D<url-encoded-query>&exp=` | US + intl patents/applications | KEY FINDING: the `/?q=` SPA route returns empty (JS-only), but the **XHR JSON endpoint** returns full structured results — titles, patent IDs, assignees, total count, CPC/assignee aggregations. Double-encode: the inner `q=` becomes `q%3D`, inner spaces become `%2B`. Rate-limits to 503 under rapid repeated calls — space requests out, rely on the 15-min cache. |
| **GitHub repo/file pages** | `https://github.com/<owner>/<repo>` ; `raw.githubusercontent.com/...` | Specific repos, READMEs, source files | Direct repo pages render server-side and extract well (READMEs, strategy lists, code). |

### Tier 2 — works, with caveats

| Venue | Pattern | Caveat |
|---|---|---|
| **AWS / vendor blogs, SRE book, vendor docs** | direct article URL | Server-rendered, extract cleanly. You need the exact URL — discover it via DuckDuckGo first. (sre.google, aws.amazon.com, *.readthedocs.io all worked.) |
| **Package registries** | npm/PyPI/crates pages, `pub.dev`, `readthedocs` | Reachable as direct pages; discover names via DuckDuckGo. crates.io's API is JSON-friendly. |

### Tier 3 — blocked / unreliable via WebFetch

| Venue | Failure | Workaround |
|---|---|---|
| **Google Patents SPA** (`/?q=`) | Renders empty — JS-only | Use the XHR JSON endpoint above. |
| **GitHub code search** (`/search?q=...&type=code`) | HTTP 429 (rate-limited/anti-bot) | Use authenticated `gh search code` (needs `GH_TOKEN`), or discover repos via DuckDuckGo `site:github.com` then fetch the repo page directly. |
| **Google Scholar** | Bot-blocked | Substitute arXiv API + DuckDuckGo + Semantic Scholar URLs surfaced indirectly. |

### Recommended search order
1. **arXiv API** — academic precedent with full abstracts.
2. **DuckDuckGo HTML** — broad web/industry/blog/GitHub discovery (run several reworded queries; add domain words to fight term collisions).
3. **Google Patents XHR** — IP precedent (space out calls to dodge 503).
4. **Direct fetches** of the strongest hits (repo page, blog post, doc) to read specifics
   and confirm how each candidate actually differs.

---

## Part 2 — LIVE PILOT (search log + verdict)

### Candidate invention under examination
> Client retry timing chosen from a **deterministic low-discrepancy** (golden-ratio /
> quasi-random) sequence instead of random jitter, to **provably** avoid retry
> clustering during outage recovery — contrasted with AWS-style **decorrelated random
> jitter**.

Decomposed claim elements: (a) retry/backoff timing for fault recovery; (b) source of
the delay is a *deterministic* low-discrepancy / golden-ratio / quasi-random sequence,
not an RNG; (c) goal is anti-clustering / thundering-herd avoidance during outage
recovery; (d) a *provable* (analytic, not simulation) uniformity guarantee.

### Search log

| # | Venue | Query | Result |
|---|---|---|---|
| 1 | DuckDuckGo | `low-discrepancy sequence retry jitter scheduling` | LDS hits are all graphics/QMC sampling (pbr-book, Halton, demofox); none on retry timing. Confirms term + topic both resolve, no retry crossover. |
| 2 | arXiv API | `all:low-discrepancy retry backoff` | Returned backoff-theory papers (Bender "How to Scale Exponential Backoff"; Goldberg/Lapinskas "Instability of all Backoff Protocols"; "RetryGuard"), but **none use low-discrepancy sequences** — all are randomized/contention-window backoff. |
| 3 | arXiv API | `"golden ratio" AND scheduling AND load` | Golden ratio appears only as a **load *threshold*** phi-1~=0.618 (Guiraud/Strozecki periodic-message scheduling; Van Houdt work-stealing-vs-sharing), NOT as a timing *generator*. Different role for the same constant. |
| 4 | DuckDuckGo | `AWS exponential backoff jitter decorrelated retry architecture blog` | Found canonical Marc Brooker post + AWS CRT `JitterMode.Decorrelated` docs. (Baseline located.) |
| 5 | Direct | aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/ | Decorrelated jitter = `sleep = min(cap, random_between(base, prev_sleep*3))` — **explicitly random**, "adding randomness." No clustering *proof*; conclusions rest on an **open-source simulator** (awslabs/aws-arch-backoff-simulator). Admits it doesn't change the N^2 nature. |
| 6 | Direct | sre.google/sre-book/handling-overload/ | Google SRE defends against retry storms with **retry budgets, layered retries, and "don't-retry" server signals** — and randomness only in retry *destination* (likely different backend), **not** in retry *timing*. No deterministic timing sequence. |
| 7 | DuckDuckGo | `golden ratio sequence spreading timers avoid synchronization deterministic jitter` | Collided with EE clock-jitter; no software-timer-spreading hits. (Term-collision case; reworded next.) |
| 8 | DuckDuckGo | `"golden ratio" hashing load balancing weighted round robin spreading` | **Closest conceptual match:** demofox "Weighted Round Robin Using the Golden Ratio Low-Discrepancy Sequence" + `Atrix256/WeightedRR`. Uses golden-ratio LDS to evenly spread **weighted selections / load**, NOT retry timing during recovery. |
| 9 | DuckDuckGo | `deterministic jitter retry backoff golden ratio OR low-discrepancy github` | **Closest implementation:** `tachyurgy/backofflite`. Mentions "deterministic" backoff strategies alongside the AWS jitter family. |
| 10 | Direct | github.com/tachyurgy/backofflite | Its "deterministic" modes are `constant/linear/exponential/fibonacci` and *seeded* PRNG jitter — reproducible, but **plain formulas / seeded pseudo-randomness, NOT a golden-ratio or low-discrepancy spacing scheme**. |
| 11 | DuckDuckGo | `quasi-Monte Carlo load spreading scheduling events avoid clustering distributed systems` | QMC even-spreading is well established (Sobol/Halton tutorials), but applied to **integration/sampling/hyperparameter search** (optuna QMCSampler, chaospy) — **no application to spreading scheduled events / retries** in distributed systems. |
| 12 | Patents (XHR) | `golden ratio load spreading scheduling retry` | 1,355 hits, all unrelated (storage, gaming, video QoE). No golden-ratio retry-timing patent surfaced. |
| 13 | Patents (XHR) | `quasi-random backoff retry timing collision avoidance` | 3,046 hits; strongest are Benveniste/AT&T **tiered contention** (US9668276B2, US9420611B2) and ZTE contention-arbitration (US9693367B2) — **priority/MAC-layer deterministic channel access**, a different domain (802.11 medium access, not client-side outage-recovery retry), and not low-discrepancy-sequence based. |

### Closest findings and how they differ

1. **AWS decorrelated jitter** (Brooker, 2015; AWS CRT `JitterMode.Decorrelated`) — the
   explicit baseline. *Differs in:* it is **random** (RNG-driven) and its anti-clustering
   behavior is argued by **simulation**, not proved. The candidate replaces the RNG with a
   deterministic low-discrepancy sequence and targets an **analytic** uniformity guarantee.
   This is the candidate's intended point of novelty and it is **unoccupied**.

2. **Golden-ratio low-discrepancy weighted round-robin** (demofox blog; `Atrix256/WeightedRR`)
   — uses the *same generator* (golden-ratio LDS, the "most irrational" number) for even
   spreading. *Differs in:* it spreads **weighted selections / load-balancing picks**, not
   **retry delays over time during outage recovery**. Same mathematical tool, different
   target quantity; no retry/backoff/recovery framing.

3. **Quasi-Monte Carlo low-discrepancy sampling** (Sobol/Halton; optuna QMCSampler, chaospy)
   — establishes the provable low-discrepancy / even-fill property the candidate leans on.
   *Differs in:* applied to **numerical integration and hyperparameter search**, with **no
   application to scheduling/spreading events or retries** in distributed systems.

4. **backofflite** (`tachyurgy/backofflite`) — closest *library* with "deterministic"
   retry modes. *Differs in:* deterministic here means `constant/linear/exponential/
   fibonacci` formulas plus *seeded* PRNG jitter — **not** a golden-ratio/low-discrepancy
   spacing sequence. (Fibonacci is the nearest neighbor and still not an LDS.)

5. **Backoff theory** (Bender et al. "How to Scale Exponential Backoff"; Goldberg/Lapinskas;
   RetryGuard) — formal results on backoff throughput/stability. *Differs in:* analyzes
   **randomized / contention-window** backoff; none substitutes a deterministic
   low-discrepancy sequence as the delay source.

6. **Golden ratio as a load *threshold*** (Guiraud/Strozecki; Van Houdt) — phi-1~=0.618 as a
   critical load constant. *Differs in:* the golden ratio is a **regime boundary**, not a
   **timing generator** — same constant, unrelated role.

7. **MAC-layer tiered/deterministic contention patents** (Benveniste/AT&T US9668276B2,
   US9420611B2; ZTE US9693367B2) — deterministic, priority-based channel-access timing to
   avoid collisions. *Differs in:* operate at the **802.11 medium-access layer** (slot/
   contention-window assignment), not **application-layer client retry during service
   outage recovery**, and are not low-discrepancy-sequence based.

### Verdict (no-prior-art-found grammar)

No prior art was found that combines all four claim elements — application-layer client
**retry timing** + a **deterministic low-discrepancy / golden-ratio sequence** as the delay
source + **outage-recovery anti-clustering** + a **provable** (analytic, not simulated)
uniformity guarantee.

- **Closest on intent:** AWS decorrelated jitter — **differs in** being random and
  simulation-justified rather than deterministic-LDS and provable.
- **Closest on mechanism:** golden-ratio low-discrepancy weighted round-robin
  (demofox / `Atrix256/WeightedRR`) — **differs in** spreading load-balancing selections,
  not retry delays during recovery.
- **Closest on guarantee:** quasi-Monte Carlo low-discrepancy theory — **differs in** being
  applied to integration/sampling, with no scheduling/retry application.
- **Closest implementation:** `backofflite` — **differs in** offering only
  formula/seeded-PRNG "deterministic" modes, not an LDS spacing scheme.

The specific composition — **swapping the RNG in decorrelated jitter for a low-discrepancy
sequence to get a provable anti-clustering bound for client retries during outage
recovery** — sits in the gap between these neighbors. The mathematical ingredients
(golden-ratio LDS, QMC even-fill) are well established but have not been assembled for this
purpose; the retry-timing baselines (AWS jitter, SRE budgets, backoff theory) remain
randomized or non-timing-based.

**Caveats / residual search risk:** GitHub *code* search (429) and Google Scholar (bot-
blocked) were not directly queryable via WebFetch, so a buried code implementation or a
paywalled paper could exist; the Patents XHR endpoint was rate-limited (503) on later
calls, so patent coverage rests on three successful queries. A follow-up with an
authenticated `gh search code` run and a Scholar/Semantic-Scholar pass would tighten the
floor before any external/filing use.
