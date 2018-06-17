import npc
import pytest

def test_find_desc():
    char = npc.Character(description=['crazed moon staring guy'])
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

class TestWildcard:
    def test_simple_tag(self):
        char1 = npc.Character(name=["char1"], court=['winter'])
        char2 = npc.Character(name=["char2"], )
        char3 = npc.Character(name=["char3"], court=['summer'])
        raw_res = npc.commands.find_characters(["court: *"], [char1, char2, char3])
        res = list(map(lambda x: x.get_first('name'), raw_res))
        assert 'char1' in res
        assert 'char2' not in res
        assert 'char3' in res

    def test_rank_tag(self):
        char1 = npc.Character(name=["char1"], group=['winter'], rank={'winter': ['hobnob']})
        char2 = npc.Character(name=["char2"])
        char3 = npc.Character(name=["char3"], group=['summer'], rank={'summer': ['hobnob']})
        raw_res = npc.commands.find_characters(["rank: *"], [char1, char2, char3])
        res = list(map(lambda x: x.get_first('name'), raw_res))
        assert 'char1' in res
        assert 'char2' not in res
        assert 'char3' in res

    def test_text_tag(self):
        char1 = npc.Character(name=["char1"], description=["hello"])
        char2 = npc.Character(name=["char2"], description=[""])
        char3 = npc.Character(name=["char3"])
        raw_res = npc.commands.find_characters(["description: *"], [char1, char2, char3])
        res = list(map(lambda x: x.get_first('name'), raw_res))
        assert 'char1' in res
        assert 'char2' in res
        assert 'char3' not in res
