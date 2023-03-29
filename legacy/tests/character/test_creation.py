"""Test different character instantiation behaviors"""
import npc
from npc.character import Character, Changeling, Werewolf, Spirit
import pytest

def test_dict():
    char = Character({"name": ["hello"]})
    assert char.tags("name") == ["hello"]

def test_kwargs():
    char = Character(name=["hello"])
    assert char.tags("name") == ["hello"]

def test_with_both_kwargs_wins():
    char = Character({"name": ["hello"], "profession": ["tailor"]}, name=["nope"])
    assert char.tags("name") == ["nope"]
    assert char.tags("profession") == ["tailor"]

def test_handles_bare_strings():
    char = Character({"name": "hello"})
    assert char.tags("name") == ["hello"]

def test_explicit_path():
    char = Character(path='Characters/test')
    assert char.path == 'Characters/test'

def test_unknown_tag():
    char = Character(snoot=["booped"])
    assert char.tags("snoot") == ["booped"]

class TestDefaultTypes:
    def test_default_changeling_type(self):
        char = Changeling()
        assert char.type_key == 'changeling'

    def test_default_werewolf_type(self):
        char = Werewolf()
        assert char.type_key == 'werewolf'

    def test_default_spirit_type(self):
        char = Spirit()
        assert char.type_key == 'spirit'
