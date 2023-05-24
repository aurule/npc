from npc.settings import MetatagSpec

from npc.characters.writer.metatag_class import Metatag

def make_spec() -> MetatagSpec:
    metatag_def = {
        "desc": "A testing tag",
        "static": {
            "test": "yes"
        },
        "match": ["brains", "brawn"],
        "separator": " :: "
    }
    return MetatagSpec("monster", metatag_def)

def test_true_with_all_names():
    metatag = Metatag(make_spec())
    metatag.open_names = []

    assert metatag.satisfied()

def test_false_without_static():
    metatag = Metatag(make_spec())
    metatag.open_names = ["test"]

    assert not metatag.satisfied()

def test_false_without_match():
    metatag = Metatag(make_spec())
    metatag.open_names = ["brawn"]

    assert not metatag.satisfied()
