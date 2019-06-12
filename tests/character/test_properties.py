"""
Test all getters and setters in the Character class

Includes all methods that set and retrieve data
"""

import npc
from npc.character import Character
import pytest

class TestTypeKey:
    def test_casing(self):
        """Type key should always be lower case"""
        char = Character(type=['Fish', 'Great Ape'])
        assert char.type_key == 'fish'

    def test_empty(self):
        char = Character()
        assert char.type_key is None

class TestLocations:
    def test_foreign(self):
        char = Character()
        char.tags('foreign').append('Mars')
        assert 'Mars' in char.locations

    def test_location(self):
        char = Character()
        char.tags('location').append('Mars')
        assert 'Mars' in char.locations

    def test_both(self):
        char = Character()
        char.tags('location').append('Mars')
        char.tags('foreign').append('Mercury')
        assert 'Mars' in char.locations
        assert 'Mercury' in char.locations

    def test_removes_empties(self):
        char = Character()
        char.tags('location').append('Mars')
        char.tags('foreign').append('')
        assert len(list(char.locations)) == 1

class TestHasLocations:
    def test_foreign(self):
        char = Character()
        char.tags('foreign').append('Mars')
        assert char.has_locations

    def test_location(self):
        char = Character()
        char.tags('location').append('Mars')
        assert char.has_locations

    def test_both(self):
        char = Character()
        char.tags('location').append('Mars')
        char.tags('foreign').append('Mercury')
        assert char.has_locations

    def test_empty(self):
        char = Character()
        char.tags('foreign').append('')
        assert not char.has_locations
