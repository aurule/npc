from npc.characters import Character

from npc.characters.writer.helpers import viable_character

def test_requires_id():
    character = Character(realname="Test Mann", file_loc="/dev/null")

    result = viable_character(character)

    assert result is False

def test_requires_name():
    character = Character(id=5, file_loc="/dev/null")

    result = viable_character(character)

    assert result is False

def test_requires_path():
    character = Character(id=5, realname="test mann")

    result = viable_character(character)

    assert result is False

def test_allows_with_required_attrs():
    character = Character(id=5, realname="Test Mann", file_loc="/dev/null")

    result = viable_character(character)

    assert result is True
