# Problem
The baseline global token bucket starves light bursty clients (run sim.py to
see). INVENT and IMPLEMENT a limiter that meets the acceptance criteria in
sim.py's docstring (Jain >= 0.90 over admit ratios, aggregate throughput >=
95% of baseline's). Use the Pattern B discipline: ideate alternatives, refute,
implement the survivor, MEASURE with run(). Report baseline + invention
numbers and your repro.
