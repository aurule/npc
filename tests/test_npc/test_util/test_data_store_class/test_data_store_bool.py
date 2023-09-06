from npc.util import DataStore

def test_true_when_dict_filled():
    store = DataStore({"valid": True})

    assert store

def test_false_when_dict_empty():
    store = DataStore()

    assert not store
