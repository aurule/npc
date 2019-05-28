"""
Test all getters and setters in the Character class

Includes all methods that set and retrieve data
"""

import npc
from npc.character import Character
import pytest

class TestAppend:
    def test_normal(self):
        char = Character()
        char.append("title", "The Stern")
        assert char.tags["title"] == ["The Stern"]

    def test_append_rank(self):
        char = Character()
        char.append_rank("Knights of the Round Table", "Dancer")
        assert char.tags["rank"]["Knights of the Round Table"] == ["Dancer"]

    def test_append_list(self):
        char = Character()
        char.append("title", "The Stern")
        char.append("title", ["The Drunk", "The Wise"])
        assert char.tags["title"] == ["The Stern", "The Drunk", "The Wise"]

def test_merge_all():
    char = Character()
    char.append('name', 'Mr. Titleson')
    char.append('title', 'The Wise')

    more_tags = {'title': 'The Stern', 'location': 'Nothingtown'}
    char.merge_all(more_tags)
    assert char.tags['title'] == ['The Wise', 'The Stern']

class TestGetFirst:
    def test_normal(self):
        char = Character(name=["hello", "goodbye"])
        assert char.get_first('name') == 'hello'

    def test_missing(self):
        char = Character()
        assert char.get_first('nope', 'negative') == 'negative'
        assert char.get_first('nope') is None

class TestGetRemaining:
    def test_normal(self):
        char = Character(name=["hello", "goodbye"])
        assert char.get_remaining('name') == ['goodbye']

    def test_missing(self):
        char = Character()
        assert char.get_remaining('nope') == []

class TestTypeKey:
    def test_casing(self):
        """Type key should always be lower case"""
        char = Character(type=['Fish', 'Great Ape'])
        assert char.type_key == 'fish'

    def test_empty(self):
        char = Character()
        assert char.type_key is None

class TestHasItems:
    @pytest.mark.parametrize('limit', [(1, True), (5, True), (10, True), (11, False)])
    def test_thresholds(self, limit):
        char = Character()
        for thing in range(0, 10):
            char.append('things', thing)
        assert char.has_items('things', limit[0]) == limit[1]

    def test_bad_threshold(self):
        char = Character()
        with pytest.raises(npc.util.OutOfBoundsError):
            char.has_items('things', 0)

class TestTagContains:
    def test_no_tag(self):
        char = Character()
        assert not char.tag_contains('status', 'baller')

    def test_rank(self):
        char = Character()
        char.append_rank('fools', 'juggler')
        char.append_rank('fools', 'tumbler')
        char.append_rank('mafia', 'juggular')
        assert char.tag_contains('rank', 'tumbler')

    def test_tag(self):
        char = Character()
        char.append('status', 'alive')
        char.append('status', 'happy')
        char.append('status', 'secretly plotting the downfall of his enemies')
        assert char.tag_contains('status', 'downfall')

class TestLocations:
    def test_foreign(self):
        char = Character()
        char.append('foreign', 'Mars')
        assert 'Mars' in char.locations

    def test_location(self):
        char = Character()
        char.append('location', 'Mars')
        assert 'Mars' in char.locations

    def test_both(self):
        char = Character()
        char.append('location', 'Mars')
        char.append('foreign', 'Mercury')
        assert 'Mars' in char.locations
        assert 'Mercury' in char.locations

    def test_removes_empties(self):
        char = Character()
        char.append('location', 'Mars')
        char.append('foreign', '')
        assert len(list(char.locations)) == 1

class TestHasLocations:
    def test_foreign(self):
        char = Character()
        char.append('foreign', 'Mars')
        assert char.has_locations

    def test_location(self):
        char = Character()
        char.append('location', 'Mars')
        assert char.has_locations

    def test_both(self):
        char = Character()
        char.append('location', 'Mars')
        char.append('foreign', 'Mercury')
        assert char.has_locations

    def test_empty(self):
        char = Character()
        char.append('foreign', '')
        assert not char.has_locations
