# anomaly-detector v3
Detection rate (true positive): 99% of real incidents trigger the alert.
False-positive rate: 5% of clean 5-min windows also trigger.
Incident base rate: ~1 in 1000 windows (hist_stats.csv backs this).
On-call doctrine being proposed: "if the alert fires, an incident is almost
certainly underway — page the whole team immediately."
Evaluate the doctrine quantitatively.
