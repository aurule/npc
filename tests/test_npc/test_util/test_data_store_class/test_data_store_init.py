from npc.util import DataStore

def test_defaulst_to_empty_dict():
    store = DataStore()

    assert store.data == {}

def test_loads_given_data():
    store = DataStore({"test": "yes"})

    assert store.get("test") == "yes"
