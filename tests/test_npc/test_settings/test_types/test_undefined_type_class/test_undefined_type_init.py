from npc.settings.types import UndefinedType

def test_name_is_key():
    chartype = UndefinedType("test")

    assert chartype.name == "test"
