# Open invention brief (full pipeline + §8)
Invent a DETERMINISTIC race demonstrator: a harness that, given worker.py's
bump logic (import it, do not edit it), makes the lost-update race fire
reproducibly — same loss pattern every run (>=99/100 identical outcomes) —
and localizes the racy line pair, with a control showing a locked version
passes under the same harness. The native scheduler makes it flaky;
determinism is the invention target. Quota/refute/build/measure; LIVE
provenance (deterministic concurrency testing has art — find it); claim
chart; honest rung; disclosure; §8 ranking.
