from npc.views import get, CharacterView

def test_returns_known_view_class():
    result = get("Character")

    assert result is CharacterView

def test_returns_unknown_none():
    result = get("nope")

    assert result is None
