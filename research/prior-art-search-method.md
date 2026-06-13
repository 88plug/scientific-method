# Prior-Art Search Protocol (for software inventions)

Goal: produce a *defensible* "no prior art found" claim, or surface the closest art. Adapted from
academic systematic-review practice (PRISMA, Wohlin snowballing) and professional patent search
(USPTO classification + citation chaining). An agent with web access executes this directly.

## Core principle

Never assert novelty from a single query in a single venue. Novelty claims survive only when
(a) multiple **query families** (term + its synonyms/jargon variants) were run, (b) across multiple
**venue classes**, (c) until **saturation** (new queries stop surfacing new relevant results), and
(d) the **closest art found** is documented and explicitly distinguished. Every search is logged so
the claim is reproducible — this is the difference between "I looked and didn't see it" and a
methodical negative result.

---

## Step 1 — Decompose the invention into searchable concepts

Restate the invention as 2–4 orthogonal concept axes (the "what", the "how", the "domain"). Example:
"a content-addressed cache that dedupes across tenants" → axes: {content-addressing / hashing},
{cache / dedup}, {multi-tenant isolation}. You search the *intersection*, then relax one axis at a
time to broaden. This is the patent-search "brainstorm the invention's elements" step and the
systematic-review PICO decomposition, fused.

## Step 2 — Build query families (keyword expansion)

For each concept axis, enumerate term variants before searching — terminology is rarely
standardized and the canonical failure mode is missing art that used a different word (Wohlin's
"cross-continent" vs "global" example). For each axis collect:

- **Synonyms & near-synonyms**: cache / memoization / lookaside; dedup / single-instancing.
- **Jargon & academic vs. industry terms**: "content-addressed" (industry) vs "hash-based
  addressing" (academic) vs "Merkle" (crypto-adjacent).
- **Abbreviations / expansions**: CAS ↔ content-addressable storage; CDN, MRU.
- **Broader/narrower terms**: hashing → SHA-256 / fingerprinting / rolling hash.
- **Spelling/locale variants** and verb/noun forms.

A **query family** = one cross-product of variants across axes (e.g. "content-addressed cache
multi-tenant" is one family; "hash-based dedup cross-tenant" is another). Plan ≥3 families. Stop
expanding a family's terms when new synonyms stop appearing in the snippets you read (vocabulary
saturation).

## Step 3 — Search the venue classes

Software prior art lives in distinct venue classes; a credible search hits several, because each
indexes different art (patents ≠ papers ≠ shipping code ≠ standards). Minimum coverage:

| Venue class | Where | What it catches | How |
|---|---|---|---|
| Academic papers | arXiv (`arxiv.org`), ACM DL, IEEE Xplore, Google Scholar, Semantic Scholar API | published research, algorithms | run query families; Scholar avoids publisher bias |
| Patents | Google Patents (`patents.google.com`), Espacenet, WIPO Patentscope | filed/granted inventions | keyword search → then **CPC class** (see Step 4) |
| Shipping code | GitHub code search (`github.com/search?type=code`), GitLab, SourceGraph | real implementations, READMEs | search identifiers + concept terms |
| Standards / protocols | IETF RFCs (`datatracker.ietf.org`), W3C, ISO | standardized prior approaches | for protocol/format inventions |
| Practitioner web | engineering blogs, Hacker News, Stack Overflow, conf talks | unpublished-but-public techniques | catches "obscure" art (Greenhalgh: snowballing finds what databases miss) |

For patents, also pull the **CPC/IPC classification codes** from the 2–3 most on-point hits, then
re-search *within those classes* — classification catches art that uses none of your keywords. This
is the single highest-value patent-specific move.

## Step 4 — Citation chaining (snowballing) from the best hits

Pick a **start set**: the 3–8 most relevant results across venues (seminal/highly-cited preferred,
spanning different communities so independent clusters are covered). Then iterate, one round at a
time for traceability:

- **Backward** (references / "cited by this"): walk each start-set item's bibliography and the
  patent's cited references. Filter by basic criteria first (date, type), drop already-seen items,
  judge each candidate from the *citing context* before opening it.
- **Forward** (who cites this): Google Scholar "Cited by", Google Patents "Cited By", GitHub
  dependents. Catches *later* art the start set couldn't reference.

Include/exclude each candidate (read abstract → relevant section → full text only if needed) **before**
using it as a new snowball seed. New included items seed the next iteration.

## Step 5 — Saturation / stopping rule

Stop when **a full backward+forward iteration over all current seeds yields no new relevant items**
(Wohlin's explicit termination). In practice the search is sufficient when *all* hold:

1. **≥3 query families × ≥3 venue classes** have been run (patents include a CPC-class pass).
2. The **last new query family surfaced zero new relevant art** (query saturation).
3. A **snowball iteration added no new included items** (citation saturation).
4. The **same few items keep reappearing** across independent venues/queries (convergence).

If the area is broad or terminology unstable, raise the family/venue minimums rather than stopping
early. Saturation is the only honest basis for "no prior art" — running out of patience is not.

## Step 6 — Log every query (PRISMA-style, reproducible)

Maintain a search log so the negative result is auditable and repeatable. One row per query:

```
| date       | venue        | query string                              | hits | reviewed | relevant | notes                    |
|------------|--------------|-------------------------------------------|------|----------|----------|--------------------------|
| 2026-06-12 | Google Patents | content-addressed cache multi-tenant    | 41   | 15       | 2        | US1234567 closest; CPC G06F12 |
| 2026-06-12 | arXiv        | hash-based dedup cross-tenant isolation   | 8    | 8        | 0        | none on multi-tenant axis |
| 2026-06-12 | GitHub code  | "content addressed" cache tenant          | 120  | 20       | 1        | repo X: single-tenant only |
```

Record the **date** (indices change over time — Wohlin), exact query, hits returned, how many were
actually reviewed, how many judged relevant, and a one-line note flagging the closest item. Also log
CPC classes examined and snowball iterations run.

---

## Claim grammar (honest reporting of results)

State scope, effort, and the closest art — never bare "novel". Templates:

- **Negative result**: "Searched **N venue classes** (arXiv, ACM/IEEE, Google Patents incl. CPC class
  `<codes>`, GitHub, RFCs) with **M query families** on **DATE**, run to saturation (last family and
  last snowball iteration surfaced no new relevant art). **Closest found: `<item + id/url>`**, which
  differs in **`<specific distinguishing element>`**. No art combining `<axis A>` with `<axis B>` was
  found."
- **Positive result**: "Prior art exists: `<item>` (DATE, venue) already teaches `<overlapping
  elements>`; the invention differs only in `<delta>`." (If the delta is the whole novelty, say so.)
- **Inconclusive**: "Searched `<venues>` with `<families>` on DATE but did **not** reach saturation
  (`<which axis/venue is uncovered>`); cannot support a no-prior-art claim — `<what remains to search>`."

Forbidden: "I couldn't find anything" without venues, families, date, and the closest item.
A novelty claim with no stated closest art is a red flag — *something* adjacent always exists; if you
found nothing even adjacent, your query families are probably too narrow (re-expand Step 2).

## Sources

- Wohlin, *Guidelines for Snowballing in Systematic Literature Studies* (EASE '14) — start set,
  backward/forward procedure, "no new papers → stop" termination, terminology-drift example.
- PRISMA 2020 / PRISMA-S — documented, reproducible search strategies; database + supplementary
  (citation, grey-literature, hand-search) coverage.
- USPTO patent search guidance — element brainstorming, CPC classification searching, citation/family
  tracing (Common Citation Document, Global Dossier).
- Greenhalgh & Peacock (2005) — snowballing best for sources in obscure venues that protocol-driven
  database search misses.
