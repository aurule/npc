"""
Test all getters and setters in the Character class

Includes all methods that set and retrieve data
"""

import npc
import pytest

class TestAppend:
    def test_normal(self):
        char = npc.Character()
        char.append("title", "The Stern")
        assert char["title"] == ["The Stern"]

    @pytest.mark.parametrize('field', npc.Character.STRING_FIELDS)
    def test_string_fields(self, field):
        char = npc.Character()
        char.append(field, "Hello hello")
        char.append(field, " baby, you called")
        assert char[field] == "Hello hello baby, you called"

    def test_append_rank(self):
        char = npc.Character()
        char.append_rank("Knights of the Round Table", "Dancer")
        assert char["rank"]["Knights of the Round Table"] == ["Dancer"]

    def test_append_list(self):
        char = npc.Character()
        char.append("title", "The Stern")
        char.append("title", ["The Drunk", "The Wise"])
        assert char["title"] == ["The Stern", "The Drunk", "The Wise"]
class TestGetFirst:
    def test_normal(self):
        char = npc.Character(name=["hello", "goodbye"])
        assert char.get_first('name') == 'hello'

    @pytest.mark.parametrize('keyname', npc.Character.STRING_FIELDS)
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

    @pytest.mark.parametrize('keyname', npc.Character.STRING_FIELDS)
    def test_string_tags(self, keyname):
        char = npc.Character()
        char.append(keyname, "hello")
        char.append(keyname, " friend")
        assert char.get_remaining(keyname) == "hello friend"

    def test_missing(self):
        char = npc.Character()
        assert char.get_remaining('nope') == []

class TestTypeKey:
    def test_casing(self):
        """Type key should always be lower case"""
        char = npc.Character(type=['Fish', 'Great Ape'])
        assert char.type_key == 'fish'

    def test_empty(self):
        char = npc.Character()
        assert char.type_key is None

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

class TestTagContains:
    def test_no_tag(self):
        char = npc.Character()
        assert not char.tag_contains('status', 'baller')

    @pytest.mark.parametrize('keyname', npc.Character.STRING_FIELDS)
    def test_string_tags(self, keyname):
        char = npc.Character()
        char.append(keyname, "hello friend")
        assert char.tag_contains(keyname, 'friend')

    def test_rank(self):
        char = npc.Character()
        char.append_rank('fools', 'juggler')
        char.append_rank('fools', 'tumbler')
        char.append_rank('mafia', 'juggular')
        assert char.tag_contains('rank', 'tumbler')

    def test_tag(self):
        char = npc.Character()
        char.append('status', 'alive')
        char.append('status', 'happy')
        char.append('status', 'secretly plotting the downfall of his enemies')
        assert char.tag_contains('status', 'downfall')

class TestLocations:
    def test_foreign(self):
        char = npc.Character()
        char.append('foreign', 'Mars')
        assert 'Mars' in char.locations

    def test_location(self):
        char = npc.Character()
        char.append('location', 'Mars')
        assert 'Mars' in char.locations

    def test_both(self):
        char = npc.Character()
        char.append('location', 'Mars')
        char.append('foreign', 'Mercury')
        assert 'Mars' in char.locations
        assert 'Mercury' in char.locations

    def test_removes_empties(self):
        char = npc.Character()
        char.append('location', 'Mars')
        char.append('foreign', '')
        assert len(list(char.locations)) == 1

class TestHasLocations:
    def test_foreign(self):
        char = npc.Character()
        char.append('foreign', 'Mars')
        assert char.has_locations

    def test_location(self):
        char = npc.Character()
        char.append('location', 'Mars')
        assert char.has_locations

    def test_both(self):
        char = npc.Character()
        char.append('location', 'Mars')
        char.append('foreign', 'Mercury')
        assert char.has_locations

    def test_empty(self):
        char = npc.Character()
        char.append('foreign', '')
        assert not char.has_locations
