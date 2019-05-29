import npc
from npc.character import Character, Changeling, Werewolf
import pytest

class TestCreation:
    """Test different instantiation behaviors"""

    def test_dict(self):
        char = Character({"name": ["hello"]})
        assert char.tags["name"] == ["hello"]

    def test_kwargs(self):
        char = Character(name=["hello"])
        assert char.tags["name"] == ["hello"]

    def test_both(self):
        char = Character({"name": ["hello"], "profession": ["tailor"]}, name=["nope"])
        assert char.tags["name"] == ["nope"]
        assert char.tags["profession"] == ["tailor"]

    def test_handles_bare_strings(self):
        char = Character({"name": "hello"})
        assert char.tags["name"] == ["hello"]

    def test_explicit_path(self):
        char = Character(path='Characters/test')
        assert char.path == 'Characters/test'

    def test_unknown_tag(self):
        char = Character(snoot=["booped"])
        assert char.tags["snoot"] == ["booped"]

class TestCopyAndAlter:
    def titleize(self, text):
        return text.title()

    def test_custom_single(self):
        char = Character()
        char.append('snoot', 'booped')
        new_char = char.copy_and_alter(self.titleize)
        assert new_char.tags.get('snoot') == ['Booped']

    def test_custom_multiple(self):
        char = Character()
        char.append('hands', 'raised')
        char.append('hands', 'jazzy')
        new_char = char.copy_and_alter(self.titleize)
        assert new_char.tags.get('hands') == ['Raised', 'Jazzy']

    def test_rank(self):
        char = Character()
        char.append_rank('restaurant', 'chef')
        char.append_rank('restaurant', 'newb')
        new_char = char.copy_and_alter(self.titleize)
        assert new_char.tags.get('rank') == {'restaurant': ['Chef', 'Newb']}

class TestChangelingDefaults:
    def test_default_type(self):
        char = Changeling()
        assert char.type_key == 'changeling'

class TestWerewolfDefaults:
    def test_default_type(self):
        char = Werewolf()
        assert char.type_key == 'werewolf'
