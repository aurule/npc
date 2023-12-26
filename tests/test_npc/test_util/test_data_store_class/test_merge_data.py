from npc.util import DataStore

def test_adds_new_values():
    store = DataStore()
    new_vars = {"npc": {"editor": "hello"}}

    store.merge_data(new_vars)

    assert store.get("npc.editor") == "hello"

def test_merges_into_namespace():
    store = DataStore()
    new_vars = {"editor": "hello"}

    store.merge_data(new_vars, namespace = "npc")

    assert store.get("npc.editor") == "hello"

def test_merges_datastore():
    store = DataStore()
    new_vars = {"npc": {"editor": "hello"}}
    new_store = DataStore(new_vars)

    store.merge_data(new_store)

    assert store.get("npc.editor") == "hello"
