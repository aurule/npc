import npc
import pytest

def test_find_desc():
    char = npc.Character(description='crazed moon staring guy')
    res = npc.commands.find_characters(["desc: moon"], [char])
    assert char in res

@pytest.mark.parametrize('delimeter', (':', ''))
def test_default_field(delimeter):
    char = npc.Character(name=['moon-moon'])
    res = npc.commands.find_characters(["{}moon".format(delimeter)], [char])
    assert char in res

def test_negation():
    """
    Negation should exclude characters that contain the text in their tag
    values, returning characters that either have a different value or who do
    not have the tag at all.
    """
    char1 = npc.Character(court=['winter'])
    char2 = npc.Character()
    char3 = npc.Character(court=['summer'])
    res = npc.commands.find_characters(["court~:winter"], [char1, char2, char3])
    assert char1 not in res
    assert char2 in res
    assert char3 in res
