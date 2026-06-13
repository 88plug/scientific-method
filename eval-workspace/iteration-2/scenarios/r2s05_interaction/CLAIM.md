# Perf review claim
"--parallel makes the pipeline ~45% faster. Enable it everywhere, including
the compressed-payload fleet (which runs --compress)." Validate before the
fleet-wide rollout. runner.py reproduces production timing behavior exactly.
