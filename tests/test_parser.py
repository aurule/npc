import npc
import pytest
import os
from tests.util import fixture_dir

def test_remove_filename_comments():
    parseables = fixture_dir(['parsing', 'characters', 'Fetches'])
    characters = list(npc.parser.get_characters(search_paths=[parseables]))
    assert characters[0]['name'][0] == 'macho mannersson'

class TestInclusion:
    """Tests which files are included in the parsed data"""

    def test_ignore_dir(self):
        parseables = fixture_dir(['parsing', 'characters'])
        ignore_me = fixture_dir(['parsing', 'characters', 'Fetches'])
        characters = npc.parser.get_characters(search_paths=[parseables], ignore_paths=[ignore_me])
        for c in characters:
            assert c.get_first('type') != 'Fetch'

    def test_ignore_file(self):
        parseables = fixture_dir(['parsing', 'characters'])
        ignore_me = fixture_dir(['parsing', 'characters', 'Changelings', 'Kabana Matansa.nwod'])
        characters = npc.parser.get_characters(search_paths=[parseables], ignore_paths=[ignore_me])
        for c in characters:
            assert 'Kabana Matansa' not in c['name']

    def test_conflict_dir(self):
        """Ignore a directory when it is in both the search and ignore lists"""
        parseables = fixture_dir(['parsing', 'characters'])
        ignore_me = fixture_dir(['parsing', 'characters'])
        characters = npc.parser.get_characters(search_paths=[parseables], ignore_paths=[ignore_me])
        assert not len(list(characters))

    def test_conflict_file(self, ):
        """Always parse a file when it is in the search and ignore lists"""
        parseables = fixture_dir(['parsing', 'characters', 'Changelings', 'Kabana Matansa.nwod'])
        ignore_me = fixture_dir(['parsing', 'characters', 'Changelings', 'Kabana Matansa.nwod'])
        characters = npc.parser.get_characters(search_paths=[parseables], ignore_paths=[ignore_me])
        assert len(list(characters)) == 1

class TestTags:
    """Tests the behavior of specific tags.

    Basic tag inclusion is handled above.
    """

    @pytest.fixture
    def character(self):
        def make_character(filename):
            parseables = fixture_dir(['parsing', 'tags', filename])
            characters = list(npc.parser.get_characters(search_paths=[parseables]))
            return characters[0]
        return make_character

    @pytest.fixture
    def basic_character(self, character):
        return character('Basic.nwod')

    def test_simple_tag(self, basic_character):
        """Tags should be added by name"""
        assert 'appearance' in basic_character

    def test_unknown_tag(self, basic_character):
        """Unknown tags should be added"""
        assert 'unrecognized' in basic_character

    def test_bare_tag(self, basic_character):
        """Tags with no data should be added"""
        assert 'skip' in basic_character

    def test_changeling_shortcut(self, character):
        """@changeling should set type, seeming, and kith"""
        c = character('Changeling Tag.nwod')
        assert c['type'][0] == 'Changeling'
        assert c['seeming'][0] == 'Beast'
        assert c['kith'][0] == 'Hunterheart'

    def test_realname(self, character):
        """@realname should overwrite the first name entry"""
        c = character('File Name.nwod')
        assert c['name'][0] == 'Real Name'

    def test_group_rank(self, character):
        """@rank should scope its value to the most recent @group"""
        c = character('Group Rank.nwod')
        assert c['rank'] == {'Frat': ['Brother']}

    def test_bare_rank(self, character):
        """@rank should not be added without a prior @group"""
        c = character('Bare Rank.nwod')
        assert not c['rank']

class TestNames:
    """Tests the way character names are grabbed from filenames"""

    @pytest.fixture
    def character(self):
        def make_character(filename):
            parseables = fixture_dir(['parsing', 'names', filename])
            characters = list(npc.parser.get_characters(search_paths=[parseables]))
            return characters[0]
        return make_character

    def test_notes(self, character):
        c = character('Standard Dude - dude man.nwod')
        assert c.get_first('name') == 'Standard Dude'

    def test_doctor(self, character):
        c = character('Dr. Manly Mann.nwod')
        assert c.get_first('name') == "Dr. Manly Mann"
