from npc.characters import Character

def test_delist_false():
    char = Character()

    assert not char.delist

def test_nolint_false():
    char = Character()

    assert not char.nolint

def test_sticky_false():
    char = Character()

    assert not char.sticky
