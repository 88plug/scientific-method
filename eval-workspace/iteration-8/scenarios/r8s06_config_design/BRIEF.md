# Invention brief (design only)
Fleet of 800 stateless API pods reads a 2MB config blob at boot. Today config
changes require a rolling restart (~25 min, risky). Invent at least 4 schemes
for live config rollout with: <60s fleet-wide propagation, instant (<5s)
rollback, gradual percentage rollout, and protection against a bad config
taking down the fleet (the last one is the hard part — design the blast-radius
control explicitly). Refute each, rank survivors, pre-commit validation
experiments. Design only.
