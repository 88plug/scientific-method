test_default_mode fails in the full suite (~always) but passes alone.
Team verdict: "flaky test, add @retry". Validate that before we paper over it.
(Run order in CI is alphabetical. pytest available; clean /tmp between
experiments as needed.)
