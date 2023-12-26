from npc.settings import MetatagSpec

def test_has_name():
    metatag_def = {"desc": "A testing tag"}

    meta = MetatagSpec("test", metatag_def)

    assert meta.name == "test"

def test_has_desc():
    metatag_def = {"desc": "A testing tag"}

    metatag = MetatagSpec("test", metatag_def)

    assert metatag.desc == metatag_def["desc"]
