from npc.characters import Character

def test_shows_id():
    char = Character(id=5, name="Test Mann", type_key="generic")

    result = repr(char)

    assert str(char.id) in result

def test_shows_name():
    char = Character(id=5, name="Test Mann", type_key="generic")

    result = repr(char)

    assert char.name in result
