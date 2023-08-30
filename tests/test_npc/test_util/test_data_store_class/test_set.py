import pytest

from npc.util import DataStore

def test_overwrites_old_simple_value():
    store = DataStore({"test": "yes"})

    store.set("test", "very yes")

    assert store.get("test") == "very yes"

def test_overwrites_old_nested_value():
    store = DataStore({"test": {"rightnow": "yes"}})

    store.set("test.rightnow", "very yes")

    assert store.get("test.rightnow") == "very yes"

def test_sets_new_value():
    store = DataStore({"test": {}})

    store.set("test.rightnow", "very yes")

    assert store.get("test.rightnow") == "very yes"

def test_creates_missing_keys():
    store = DataStore()

    store.set("test.rightnow", "very yes")

    assert store.get("test.rightnow") == "very yes"

def test_bad_list_write_error():
    store = DataStore({"test": {"rightnow": [1, 2, 3]}})

    with pytest.raises(TypeError):
        store.set("test.rightnow.generic", "extremely")

def test_bad_list_access_error():
    store = DataStore({"test": {"rightnow": [1, 2, 3]}})

    with pytest.raises(TypeError):
        store.set("test.rightnow.generic.five", "extremely")
