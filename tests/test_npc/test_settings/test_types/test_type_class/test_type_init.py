from npc.settings.types import Type

def test_has_name():
    type_def = {"name": "Test type"}

    chartype = Type("test", type_def)

    assert chartype.name == type_def["name"]

def test_has_desc():
    type_def = {"desc": "A test type"}

    chartype = Type("test", type_def)

    assert chartype.desc == type_def["desc"]
