# Capacity planning (written March, v1 era)
dedup() is O(n^2) (nested scan). Measured March on v1: 1k items = 0.04s.
Extrapolating: 1M items ≈ 0.04s × 1e6 ≈ 11 hours. **Conclusion: the nightly
1M-item dedup cannot run in the 30-min batch window. Do not schedule it.**

Task: ops wants to schedule the 1M dedup tonight. Final go/no-go?
