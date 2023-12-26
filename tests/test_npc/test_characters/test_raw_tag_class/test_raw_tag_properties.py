from npc.characters import RawTag

def test_has_name():
    tag = RawTag("name", "value")

    assert tag.name == "name"

def test_has_value():
    tag = RawTag("name", "value")

    assert tag.value == "value"
