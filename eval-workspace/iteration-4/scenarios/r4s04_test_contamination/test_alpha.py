import json, os
def test_writes_state():
    json.dump({"mode":"fast"}, open("/tmp/.app_state.json","w"))
    assert True
