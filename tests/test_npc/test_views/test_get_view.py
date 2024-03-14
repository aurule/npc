from npc.views import get, CharacterView, GroupView, TagView

def test_returns_character_view():
    result = get("Character")

    assert result is CharacterView

def test_returns_group_view():
    result = get("Group")

    assert result is GroupView

def test_returns_tag_view():
    result = get("Tag")

    assert result is TagView

def test_returns_unknown_none():
    result = get("nope")

    assert result is None
