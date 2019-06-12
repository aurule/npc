import npc
from npc.character import Character
import pytest

def test_find_desc():
    char = Character(description=['crazed moon staring guy'])
    res = npc.commands.find_characters(["desc: moon"], [char])
    assert char in res

@pytest.mark.parametrize('delimeter', (':', ''))
def test_default_field(delimeter):
    char = Character(name=['moon-moon'])
    res = npc.commands.find_characters(["{}moon".format(delimeter)], [char])
    assert char in res

def test_negation():
    """
    Negation should exclude characters that contain the text in their tag
    values, returning characters that either have a different value or who do
    not have the tag at all.
    """
    char1 = Character(court=['winter'])
    char2 = Character()
    char3 = Character(court=['summer'])
    res = npc.commands.find_characters(["court~:winter"], [char1, char2, char3])
    assert char1 not in res
    assert char2 in res
    assert char3 in res

class TestWildcard:
    def test_simple_tag(self):
        char1 = Character(name=["char1"], court=['winter'])
        char2 = Character(name=["char2"], )
        char3 = Character(name=["char3"], court=['summer'])
        raw_res = npc.commands.find_characters(["court: *"], [char1, char2, char3])
        res = list(map(lambda x: x.tags('name').first_value(), raw_res))
        assert 'char1' in res
        assert 'char2' not in res
        assert 'char3' in res

    def test_rank_tag(self):
        char1 = Character(name=["char1"], group=['winter'], rank={'winter': ['hobnob']})
        char2 = Character(name=["char2"])
        char3 = Character(name=["char3"], group=['summer'], rank={'summer': ['hobnob']})
        raw_res = npc.commands.find_characters(["rank: *"], [char1, char2, char3])
        res = list(map(lambda x: x.tags('name').first_value(), raw_res))
        assert 'char1' in res
        assert 'char2' not in res
        assert 'char3' in res

    def test_text_tag(self):
        char1 = Character(name=["char1"], description=["hello"])
        char2 = Character(name=["char2"], description=["x"])
        char3 = Character(name=["char3"])
        raw_res = npc.commands.find_characters(["description: *"], [char1, char2, char3])
        res = list(map(lambda x: x.tags('name').first_value(), raw_res))
        assert 'char1' in res
        assert 'char2' in res
        assert 'char3' not in res
