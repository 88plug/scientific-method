# Problem
This harness (loadtest.sh) has an order/warm-state bias AND one of the two
servers is genuinely faster. INVENT and IMPLEMENT a corrected measurement
harness such that: (1) an A/A run (same server twice) reports a difference
<2%; (2) the real A/B difference is still detected and quantified correctly
(state the true value with n>=5 and spread). Diagnose the bias mechanism
first. Numbers + repro.
