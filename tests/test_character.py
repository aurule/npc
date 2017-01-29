import npc
import pytest

def test_append_rank():
    char = npc.Character()
    char.append_rank("Knights of the Round Table", "Dancer")
    assert char["rank"]["Knights of the Round Table"] == ["Dancer"]

class TestCreation:
    """Test different instantiation behaviors"""

    def test_dict(self):
        char = npc.Character({"name": ["hello"]})
        assert char["name"] == ["hello"]

    def test_kwargs(self):
        char = npc.Character(name=["hello"])
        assert char["name"] == ["hello"]

    def test_both(self):
        char = npc.Character({"name": ["hello"], "profession": ["tailor"]}, name=["nope"])
        assert char["name"] == ["nope"]
        assert char["profession"] == ["tailor"]

class TestAppend:
    def test_normal(self):
        char = npc.Character()
        char.append("title", "The Stern")
        assert char["title"] == ["The Stern"]

    def test_desc(self):
        char = npc.Character()
        char.append("description", "Hello hello")
        char.append("description", " baby, you called")
        assert char["description"] == "Hello hello baby, you called"

class TestTypeKey:
    def test_lowercase(self):
        char = npc.Character(type=['Fish', 'Great Ape'])
        assert char.type_key == 'fish'

    def test_empty(self):
        char = npc.Character()
        assert char.type_key is None

class TestGetFirst:
    def test_normal(self):
        char = npc.Character(name=["hello", "goodbye"])
        assert char.get_first('name') == 'hello'

    @pytest.mark.parametrize('keyname', npc.Character.STRING_TAGS)
    def test_string_tags(self, keyname):
        char = npc.Character()
        char.append(keyname, "hello")
        char.append(keyname, " friend")
        assert char.get_first(keyname) == "hello friend"

    def test_missing(self):
        char = npc.Character()
        assert char.get_first('nope', 'negative') == 'negative'
        assert char.get_first('nope') is None

class TestGetRemaining:
    def test_normal(self):
        char = npc.Character(name=["hello", "goodbye"])
        assert char.get_remaining('name') == ['goodbye']

    @pytest.mark.parametrize('keyname', npc.Character.STRING_TAGS)
    def test_string_tags(self, keyname):
        char = npc.Character()
        char.append(keyname, "hello")
        char.append(keyname, " friend")
        assert char.get_remaining(keyname) == "hello friend"

    def test_missing(self):
        char = npc.Character()
        assert char.get_remaining('nope') == []

class TestHasItems:
    @pytest.mark.parametrize('limit', [(1, True), (5, True), (10, True), (11, False)])
    def test_thresholds(self, limit):
        char = npc.Character()
        for thing in range(0, 10):
            char.append('things', thing)
        assert char.has_items('things', limit[0]) == limit[1]

    def test_bad_threshold(self):
        char = npc.Character()
        with pytest.raises(npc.util.OutOfBoundsError):
            char.has_items('things', 0)

class TestCopyAndAlter:
    def titleize(self, text):
        return text.title()

    def test_custom_single(self):
        char = npc.Character()
        char.append('snoot', 'booped')
        new_char = char.copy_and_alter(self.titleize)
        assert new_char.get('snoot') == ['Booped']

    def test_custom_multiple(self):
        char = npc.Character()
        char.append('hands', 'raised')
        char.append('hands', 'jazzy')
        new_char = char.copy_and_alter(self.titleize)
        assert new_char.get('hands') == ['Raised', 'Jazzy']

    @pytest.mark.parametrize('keyname', npc.Character.STRING_TAGS)
    def test_string(self, keyname):
        char = npc.Character()
        char.append(keyname, 'hello hello')
        new_char = char.copy_and_alter(self.titleize)
        assert new_char.get(keyname) == "Hello Hello"

    def test_rank(self):
        char = npc.Character()
        char.append_rank('restaurant', 'chef')
        char.append_rank('restaurant', 'newb')
        new_char = char.copy_and_alter(self.titleize)
        assert new_char.get('rank') == {'restaurant': ['Chef', 'Newb']}

class TestBasicValidation:
    """Tests universal validations"""

    def test_blank_description(self):
        char = npc.Character(description='')
        char.validate()
        assert 'Missing description' in char.problems

    def test_whitespace_description(self):
        char = npc.Character(description=' \t')
        char.validate()
        assert 'Missing description' in char.problems

    def test_no_type(self):
        char = npc.Character(type=[])
        char.validate()
        assert 'Missing type' in char.problems

    def test_no_type(self):
        char = npc.Character(name=[])
        char.validate()
        assert 'Missing name' in char.problems

class TestChangelingValidation:
    """Tests the changeling-specific validations"""

    def test_no_seeming(self):
        char = npc.Character(type=['changeling'], seeming=[])
        char.validate()
        assert 'Missing seeming' in char.problems

    def test_no_kith(self):
        char = npc.Character(type=['changeling'], kith=[])
        char.validate()
        assert 'Missing kith' in char.problems

    only_one = [
        ('court', ['summer', 'winter']),
        ('motley', ['hannover', 'hillbillies']),
        ('entitlement', ['honorable knights', 'dishonorable knights'])
    ]
    @pytest.mark.parametrize('key, values', only_one)
    def test_many_courts(self, key, values):
        char = npc.Character(type=['changeling'], **{key: values})
        char.validate()
        assert 'Multiple {key}s: {vals}'.format(key=key, vals=", ".join(values)) in char.problems

class TestValid:
    """Tests for the correctness of the `valid` getter"""

    def test_initial_state(self):
        """Character should be invalid before first call to validate()"""
        char = npc.Character(type=['human'], description='hi there', name=['dude'])
        assert not char.valid
        char.validate()
        assert char.valid

    def test_with_errors(self):
        char = npc.Character()
        char.validate()
        assert not char.valid

# tests to do:
# build header
