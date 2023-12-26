from npc.settings.tags import UndefinedTagSpec

def test_name_is_key():
    tag = UndefinedTagSpec("test")

    assert tag.name == "test"
