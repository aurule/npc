from npc.settings.types import UndefinedTypeSpec

def test_name_is_key():
    chartype = UndefinedTypeSpec("test")

    assert chartype.name == "test"
