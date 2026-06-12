---
description: "True peer review of an invention/finding/design: blind lensed reviewers, rebuttal, revision, area-chair decision"
argument-hint: "[the invention, finding, design, or document to review]"
disable-model-invocation: true
allowed-tools: Task
---

Run a full peer-review round on: $ARGUMENTS

If no argument: review the most significant unreviewed finding/invention in
this conversation or the project ledger's most recent CONFIRMED-but-unreviewed
entry; if neither exists, ask what to review.

Peer review is the correction engine after the refute gate: refutation asks
"is this wrong?", peer review asks "what must change before anyone builds on
it?" — and then the changes actually get made. Run it before building,
merging, publishing, or sending an invention/finding externally.

1. **Assemble the submission packet.** The claim/design/writeup, ALL its
   evidence (ledger rows, probe files, measurements, claimed-vs-observed
   data), and a working Reproduce block. Strip author confidence language —
   reviewers judge evidence, not enthusiasm. If there is no Reproduce block,
   build one first; a submission that can't state how to reproduce its
   numbers is not reviewable.
2. **Round 1 — independent blind reviews.** Spawn the plugin's
   `peer-reviewer` agent 3-5 times IN PARALLEL, identical packet, one lens
   each: `soundness`, `prior-art/provenance`, `reproducibility`, `significance`,
   and always `fatal-flaw`. Vary models across reviewers when stakes are
   high (same rationale as the council: decorrelated blind spots). Reviewers
   are blind to each other.
3. **Rebuttal — answer with evidence, not prose.** Collect every weakness
   tagged `blocking` and every QUESTION FOR AUTHORS. For each, the rebuttal
   is one of: (a) new evidence — run the missing probe/control NOW and
   attach the result; (b) a concrete revision to the artifact — make the
   correction NOW and reference the diff; (c) a documented concession — the
   limitation goes into the writeup verbatim. "We respectfully disagree"
   without a measurement is not a rebuttal. This step is where review
   becomes correction: the feedback is applied to the work during the round,
   not filed for later.
4. **Re-score.** Send each reviewer (via SendMessage, so they keep context)
   the rebuttal items addressed to their review plus the diffs/new evidence.
   They update scores and recommendation. A reviewer whose blocking weakness
   was answered with evidence should move; one whose weakness was answered
   with words should not.
5. **Meta-review.** Spawn one `meta-reviewer` (area chair) with the packet,
   all reviews, the rebuttal, and re-scores. It weighs evidence over votes
   and returns the decision with verifiable requirements.
6. **Close the loop into the ledger and the artifact.**
   - `accept` → ledger verdict CONFIRMED (review round as evidence ref);
     proceed to build/publish.
   - `minor-revision` → apply the listed revisions now, verify each, then
     record as accepted; ledger status prototype until done.
   - `major-revision` → blocking weaknesses become new ledger hypotheses
     with probes; the work returns to the investigate/falsify loop, and a
     NEW review round (fresh reviewers) runs on the revised submission.
   - `reject` → falsification log, DO-NOT-RE-ATTACK, with the kill_reason
     and the condition (if any) that would reopen it.

Report: the decision; what each reviewer executed and found; which
corrections were applied during the round (with diffs/refs); dissent on
record; the ledger entry; and — for anything short of accept — the exact
next probes. The measure of a good round is not the score, it's the delta:
say plainly how the work is different/better than before review.
