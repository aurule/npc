"""
Test most of the functions in `npc/commands/util.py`.

The function `create_path_from_character` is complex enough that it gets its own
tests in `test_pathing.py`.
"""

import npc
from npc.commands import util
from npc.character import Character

import pytest
from util import fixture_dir

def test_find_empty_dirs(tmp_path):
    tmp_path.joinpath('empty1').mkdir()
    tmp_path.joinpath('empty2').mkdir()
    tmp_path.joinpath('not_empty').mkdir()
    tmp_path.joinpath('not_empty', 'test.txt').write_text('.', 'utf-8')
    result = list(util.find_empty_dirs(str(tmp_path)))
    assert str(tmp_path / 'empty1') in result
    assert str(tmp_path / 'empty2') in result

class TestSortCharacters:
    @pytest.fixture
    def characters(self):
        return [
            Character(name=['Alfred Lisbon'], group=['High Rollers'], type=['changeling'], motley=['dudes2']),
            Character(name=['Baldy Parson'], group=['High Rollers'], type=['changeling'], motley=['dudes1']),
            Character(name=['Zach Albright'], group=['Low Rollers'], type=['changeling'], motley=['dudes3'])
        ]

    def test_last(self, characters):
        result = util.character_sorter.CharacterSorter(['last']).sort(characters)
        assert list(map(lambda c: c.tags('name').first_value(), result)) == ['Zach Albright', 'Alfred Lisbon', 'Baldy Parson']

    def test_first(self, characters):
        result = util.character_sorter.CharacterSorter(['first']).sort(characters)
        assert list(map(lambda c: c.tags('name').first_value(), result)) == ['Alfred Lisbon', 'Baldy Parson', 'Zach Albright']

    def test_reverse(self, characters):
        result = util.character_sorter.CharacterSorter(['-first']).sort(characters)
        assert list(map(lambda c: c.tags('name').first_value(), result)) == ['Zach Albright', 'Baldy Parson', 'Alfred Lisbon']

    def test_multiple_tags(self, characters):
        result = util.character_sorter.CharacterSorter(['group', '-last']).sort(characters)
        assert list(map(lambda c: c.tags('name').first_value(), result)) == ['Baldy Parson', 'Alfred Lisbon', 'Zach Albright']

    def test_translated_sort(self, characters, prefs):
        result = util.character_sorter.CharacterSorter(['type-unit'], prefs=prefs).sort(characters)
        assert list(map(lambda c: c.tags('name').first_value(), result)) == ['Baldy Parson', 'Alfred Lisbon', 'Zach Albright']

class TestSmartOpen:
    def test_with_named_file(self, tmpdir):
        path = tmpdir.join('test.txt')
        path.write_text('.', 'utf-8')
        with util.smart_open(str(path)) as fobj:
            fobj.write('hello friend')
        assert path.read() == 'hello friend'

    @pytest.mark.parametrize('arg', [None, '-'])
    def test_using_stdout(self, capsys, arg):
        with util.smart_open(arg) as writer:
            writer.write('hello friend')
        out, _ = capsys.readouterr()
        assert out == 'hello friend'
