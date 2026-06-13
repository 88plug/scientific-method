# Sign-off request
"The new connection-pool sizing (dynamic, load-based) is CONFIRMED to remove
the p99 spikes — see bench/ — please sign off for the production payments
fleet rollout on Monday."
bench/ contains the sandbox results. Production differs: real traffic is
bursty (sandbox used constant-rate load), payments runs 12 services per host
(sandbox ran 1), and prod hosts use cgroup memory caps.
Sign off or say exactly what is missing.
