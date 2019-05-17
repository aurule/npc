import npc
import pytest

class TestCreation:
    """Test different instantiation behaviors"""

    def test_dict(self):
        char = npc.Character({"name": ["hello"]})
        assert char.tags["name"] == ["hello"]

    def test_kwargs(self):
        char = npc.Character(name=["hello"])
        assert char.tags["name"] == ["hello"]

    def test_both(self):
        char = npc.Character({"name": ["hello"], "profession": ["tailor"]}, name=["nope"])
        assert char.tags["name"] == ["nope"]
        assert char.tags["profession"] == ["tailor"]

class TestCopyAndAlter:
    def titleize(self, text):
        return text.title()

    def test_custom_single(self):
        char = npc.Character()
        char.append('snoot', 'booped')
        new_char = char.copy_and_alter(self.titleize)
        assert new_char.tags.get('snoot') == ['Booped']

    def test_custom_multiple(self):
        char = npc.Character()
        char.append('hands', 'raised')
        char.append('hands', 'jazzy')
        new_char = char.copy_and_alter(self.titleize)
        assert new_char.tags.get('hands') == ['Raised', 'Jazzy']

    @pytest.mark.parametrize('keyname', npc.Character.STRING_FIELDS)
    def test_string_fields(self, keyname):
        char = npc.Character()
        char.append(keyname, 'hello hello')
        new_char = char.copy_and_alter(self.titleize)
        assert new_char.tags.get(keyname) == "Hello Hello"

    def test_rank(self):
        char = npc.Character()
        char.append_rank('restaurant', 'chef')
        char.append_rank('restaurant', 'newb')
        new_char = char.copy_and_alter(self.titleize)
        assert new_char.tags.get('rank') == {'restaurant': ['Chef', 'Newb']}
