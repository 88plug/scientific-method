---
description: "Convene a model council: the same question answered independently across different models, dissent surfaced, cruxes routed to probes"
argument-hint: "[the question, decision, or claim to put before the council]"
disable-model-invocation: true
allowed-tools: Task, Bash(curl:*)
---

Convene a model council on: $ARGUMENTS

If no question was given, put the currently open decision or contested claim
in this conversation before the council; if there is none, ask.

A council exists to break correlated error: one model (including you) asked
twice gives the same blind spot twice. Different model tiers — and ideally a
different model family — fail differently, so agreement across them means
more and disagreement is a finding in itself. A council is for judgment
calls: design choices, interpretation of ambiguous results, risk and go/no-go
calls, "is this invention worth building". It does NOT settle empirical
questions — when seats disagree about a measurable fact, the council's output
is the probe, and the data rules.

1. **Frame the question** in one paragraph with the relevant evidence
   attached (ledger excerpts, measurements, constraints). Every seat gets the
   identical packet. Do not include your own current lean — seats must not
   anchor on the orchestrator.
2. **Seat the council** — spawn the plugin's `council-member` agent 3-5
   times IN PARALLEL (single message, multiple Agent calls), each with a
   different `model` override: at minimum one fast tier (haiku), one mid
   (sonnet), one frontier (opus or inherit). Seats are blind to each other.
3. **Out-of-family seat (strongest decorrelation).** If the
   `COUNCIL_OOF_ENDPOINT` env var is set (or the project's docs name a local
   OpenAI-compatible endpoint, e.g. an LM Studio / Ollama server), probe it
   with `curl -s --max-time 5 $COUNCIL_OOF_ENDPOINT/v1/models`; if reachable,
   POST the same packet with the council-member output contract to
   `/v1/chat/completions` and treat the response as one more seat. Note that
   this seat cannot run probes — weigh it accordingly. Skip silently if
   unset or unreachable.
4. **Aggregate by evidence, not by count.**
   - Build the agreement matrix: position × seat, with each seat's key
     evidence and confidence.
   - Weigh seats by what they actually probed (their KEY EVIDENCE refs), not
     by model size or eloquence. A seat that checked the code beats a seat
     that reasoned beautifully.
   - **Unanimity check:** if all seats agree with near-identical reasoning
     and none probed anything, treat the consensus as a shared prior, not a
     conclusion — run the cheapest probe from any seat's
     "WOULD CHANGE MY MIND" before adopting it.
   - **Dissent handling:** extract the crux of each disagreement. Factual
     crux → route to an experiment (this is the council's most valuable
     output). Values/judgment crux → decide it yourself, on the record, with
     the dissent preserved.
5. **Feed the result back as corrections.** The council's output is not just
   a verdict — apply it: counterarguments that survive become revisions to
   the design/claim under question; "would change my mind" conditions become
   ledger hypotheses with probes; if the council overturned your prior lean,
   say so explicitly and correct the artifact/ledger now, not at the end of
   the session. If corrections were substantial, you may reconvene on the
   revised version — seats get the diff and their own prior positions.

Report: the decision with calibrated confidence; the agreement matrix;
dissent on record (verbatim gist of minority positions and why overruled);
corrections applied as a result; and the unresolved empirical questions as
ledger-ready hypothesis rows with their probes.
