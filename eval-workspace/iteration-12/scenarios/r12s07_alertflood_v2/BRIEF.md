# Frontier brief: improve on our own prior invention (full pipeline)
Prior work: eval-workspace/iteration-10/r10s03/with_skill/outputs/ contains a
working alert-grouping algorithm (group_alerts.py) that passed C1-C5 on the
original flood. Treat IT as the tuned baseline. The new requirement: the
same algorithm class must ALSO handle (a) two incidents OVERLAPPING in time
(generate such cases), and (b) an incident whose symptom set drifts mid-
incident. Build the v2, show v1 fails at least one new case while v2 passes
all (plus the original C1-C5 regression), ablate the delta, provenance the
new elements, honest rung, disclosure. No criteria softening: v2 must not
regress v1's original scorecard.
