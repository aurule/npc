from npc.settings import Metatag

def test_has_name():
    metatag_def = {"desc": "A testing tag"}

    meta = Metatag("test", metatag_def)

    assert meta.name == "test"

def test_has_desc():
    metatag_def = {"desc": "A testing tag"}

    metatag = Metatag("test", metatag_def)

    assert metatag.desc == metatag_def["desc"]
