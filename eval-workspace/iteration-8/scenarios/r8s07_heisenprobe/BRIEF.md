# Invention brief
From our earlier campaign: instrumenting a racy worker (logging/sleeps) masks
its race. Invent at least 4 PROBE techniques that localize a data race with
minimal perturbation of the timing it depends on. For each: mechanism, what
it perturbs (be precise), what it can and cannot conclude. Refute each. You
may demo any of them on worker_sim.py (a 4-thread racy counter) but design
quality is the deliverable.
