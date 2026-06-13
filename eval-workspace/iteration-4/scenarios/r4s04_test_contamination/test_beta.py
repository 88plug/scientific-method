import json, os
def test_default_mode():
    # reads optional state file; default should be "safe"
    mode="safe"
    if os.path.exists("/tmp/.app_state.json"):
        mode=json.load(open("/tmp/.app_state.json")).get("mode","safe")
    assert mode=="safe", f"expected safe, got {mode}"
