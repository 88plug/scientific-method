# Method-audit brief (rigor.md §5 made real)
verdicts.csv is a ledger's verdict history: stated confidence vs eventual
outcome (1=held, 0=overturned). Audit the calibration: compute the Brier
score and its reliability decomposition (or a binned calibration table),
determine WHERE the ladder is miscalibrated, and produce the corrected
confidence mapping the method should use going forward. Quantify the
evidence honestly (n=30 is small — say what that limits). This is the
plugin's own discipline applied to itself.
