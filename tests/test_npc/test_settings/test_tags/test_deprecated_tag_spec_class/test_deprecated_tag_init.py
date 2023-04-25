from npc.settings import DeprecatedTagSpec

def test_has_name():
    tag_def = {"desc": "A testing tag"}

    tag = DeprecatedTagSpec("test", tag_def)

    assert tag.name == "test"

def test_has_desc():
    tag_def = {"desc": "A testing tag"}

    tag = DeprecatedTagSpec("test", tag_def)

    assert tag.desc == tag_def["desc"]
