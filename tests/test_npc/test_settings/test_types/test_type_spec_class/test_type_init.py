from npc.settings.types import TypeSpec

def test_has_name():
    type_def = {"name": "Test type"}

    chartype = TypeSpec("test", type_def)

    assert chartype.name == type_def["name"]

def test_has_desc():
    type_def = {"desc": "A test type"}

    chartype = TypeSpec("test", type_def)

    assert chartype.desc == type_def["desc"]
