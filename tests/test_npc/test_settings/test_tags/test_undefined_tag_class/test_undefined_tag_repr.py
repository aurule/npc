from npc.settings.tags import UndefinedTagSpec

def test_includes_tag_name():
    tag = UndefinedTagSpec("test")

    assert "test" in repr(tag)
