# Changelog

All notable changes to the scientific-method plugin. Versions follow calver
(`YEAR.MONTH.BUILD`) and match the `plugin.json` `version` field; users receive
an update when it is bumped.

## 2026.6.23

### Changed
- Compliance pass to the 88plug scaffold: added `version` (calver) and an explicit
  `hooks` pointer to `plugin.json`, set keywords to exactly 20, refreshed CI action
  versions, added a smoke test, fixed the MkDocs config and docs landing page, and
  extended `.gitignore` data-hygiene patterns.

## 2026.6.12

### Changed
- **License: MIT → FSL-1.1-ALv2** (`LICENSE.md`, `Copyright 2026 88plug`) to match
  the house standard for original 88plug plugins. The Functional Source License is
  source-available and converts to Apache 2.0 two years after each release.
- Aligned naming + metadata to 88plug conventions for publication: repo
  `88plug/scientific-method` (no `-plugin` suffix), `author`/`owner` `88plug`
  (`claude@cryptoandcoffee.com`), marketplace `$schema`/`category: productivity`/
  `tags: ["type:plugin", …]`, and `repository` `.git` suffix. Added
  `marketplace-entry.json` (github-source entry for the central marketplace).

### Fixed (found by real interactive tmux evals, re-verified)
- **Auto-triggering on incident framing**: broadened the SKILL.md description to
  cover outage/brownout/latency-spike/retry-storm/cascading-failure/regression
  phrasing and softer "root cause and fix" asks — the skill now auto-loads on
  implicit-incident prompts that previously slipped through.
- **Numeric confidence mandatory**: every verdict (including weak-support /
  inconclusive) must emit an actual confidence number, not a verbal hedge.

### Added
- **SessionStart hook** (`hooks/surface-ledger.sh`): when an `EXPERIMENTS.md`
  hypothesis ledger exists for the project, its contents are surfaced
  automatically at session start (and after compaction) so killed hypotheses
  stay DO-NOT-RE-ATTACK and open predictions survive across sessions. Read-only,
  silent no-op when no ledger exists, truncates large ledgers.
- Manifest completeness: `$schema`, `displayName`, `keywords`, `homepage`,
  `repository`, and full `author`/`owner` fields in `plugin.json` and
  `marketplace.json`.

### Changed (workflow)
- All commands now set `disable-model-invocation: true` (user-triggered only —
  Claude won't auto-fire a heavyweight council/falsification/invention campaign
  mid-conversation) and carry scoped `allowed-tools`.
- Agents gain scoped `tools`/`disallowedTools` (e.g. `experiment-designer` and
  `refuter` are now read-only, enforcing "design, don't run" and "read-only
  probes") and display `color`s. `refuter` is marked for proactive use.
- Eval iteration-14 fixes: the invention pipeline now names the canonical
  known-good as prior art and scopes novelty to the measured delta; calibration
  guidance distinguishes a weak directional lean from a flat INCONCLUSIVE.
- WS-template campaign: a gated, validated SAT apparatus and a worked
  certificate-verifiable result, folded into `references/open-records.md`.
- `references/open-records.md`: certificate-verifiable discovery playbook with a
  worked case study.
- Open-records attack capability: methodology for world-record attempts on
  certificate-verifiable open problems.
- Certification close: peak invention discipline; peer-review correction loops.
- Provability hierarchy, impossibility toolkit, campaign capstone.
- Invention established as the default continuation, with provable claims.
- Acceptance-gated invention campaigns.
- Anticipation (abduction) and causal-structure layers added.

## 2026.6.11

- Initial release: falsification-first investigation workflow — hypotheses,
  prediction-before-measurement, controlled experiments, REFUTE-first
  verification, and the persistent hypothesis ledger.
