# Intermittent wrong totals in invoice PDFs
~0.3% of invoices show a total off by a small amount. Engineering already
falsified the obvious candidates (notes in eliminated.md are sound — do not
re-attack, but the answer may still involve the components mentioned there).
repro.py deterministically reproduces a wrong total for the cases in
failing_cases.csv. Find the actual bug.
