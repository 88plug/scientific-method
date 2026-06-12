---
description: "Create or update the persistent hypothesis ledger (EXPERIMENTS.md) for this project"
argument-hint: "[optional: campaign name or 'sync' to backfill from this conversation]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit
---

Maintain the hypothesis ledger for this project: $ARGUMENTS

The ledger is the campaign's memory across sessions and compactions — killed
hypotheses stay killed (DO-NOT-RE-ATTACK), open ones keep their pre-committed
predictions, and every retraction stays visible as a dated scope correction.

1. Locate the existing ledger: `EXPERIMENTS.md` at the project root, or the
   project's own convention (`docs/`, `incidents/`, `test/*.md` walls docs).
   If none exists, create `EXPERIMENTS.md` from the ledger template in the
   scientific-method skill's references/artifacts.md.
2. If the argument is "sync" (or a ledger already exists and this
   conversation contains untracked findings): backfill every hypothesis,
   verdict, ruled-out candidate, and dead end discussed in this conversation
   into the ledger. Each verdict needs its one-line evidence reference; each
   kill goes to the falsification log with DO-NOT-RE-ATTACK; each open
   hypothesis gets its prediction and outcome table recorded as stated
   (do not retro-fit predictions to known results — if the prediction was
   never stated before the measurement, mark it "post-hoc").
3. Verify ledger integrity while you're there: verdicts without evidence get
   demoted to OPEN; claims of 100% confidence with named unknowns get
   recalibrated; the Reproduce block's commands still work (spot-check the
   cheapest one).
4. Report: ledger path, open hypotheses with their next probes, and anything
   demoted or corrected.

Keep it append-only. The audit trail — including the wrong turns — is what
makes the verdicts trustworthy and prevents future sessions from re-fighting
settled questions.
