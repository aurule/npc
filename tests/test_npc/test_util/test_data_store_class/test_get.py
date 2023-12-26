from npc.util import DataStore

def test_returns_simple_key_value():
    store = DataStore({"valid": True})

    result = store.get("valid", "fail")

    assert result != "fail"

def test_returns_nested_key_value():
    store = DataStore({"npc": {"version": "test"}})

    result = store.get("npc.version")

    assert result == "test"

def test_returns_default_with_missing_key():
    store = DataStore({"npc": {"version": "test"}})

    result = store.get("npc.nopealope", "missing")

    assert result == "missing"
