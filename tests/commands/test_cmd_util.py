"""
Test most of the functions in `npc/commands/util.py`.

The function `create_path_from_character` is complex enough that it gets its own
tests in `test_pathing.py`.
"""

import npc
from npc.commands import util

import pytest
from tests.util import fixture_dir

def test_find_empty_dirs(tmpdir):
    tmpdir.mkdir('empty1')
    tmpdir.mkdir('empty2')
    tmpdir.mkdir('not_empty')
    tmpdir.join('not_empty', 'test.txt').write_text('.', 'utf-8')
    result = list(util.find_empty_dirs(str(tmpdir)))
    assert str(tmpdir.join('empty1')) in result
    assert str(tmpdir.join('empty2')) in result

class TestSortCharacters:
    @pytest.fixture
    def characters(self):
        return [
            npc.Character(name=['Alfred Lisbon'], group=['High Rollers']),
            npc.Character(name=['Baldy Parson'], group=['High Rollers']),
            npc.Character(name=['Zach Albright'], group=['Low Rollers'])
        ]

    def test_last(self, characters):
        result = util.character_sorter.CharacterSorter('last').sort(characters)
        assert list(map(lambda c: c.get_first('name'), result)) == ['Zach Albright', 'Alfred Lisbon', 'Baldy Parson']

    def test_first(self, characters):
        result = util.character_sorter.CharacterSorter('first').sort(characters)
        assert list(map(lambda c: c.get_first('name'), result)) == ['Alfred Lisbon', 'Baldy Parson', 'Zach Albright']

    def test_reverse(self, characters):
        result = util.character_sorter.CharacterSorter('-first').sort(characters)
        assert list(map(lambda c: c.get_first('name'), result)) == ['Zach Albright', 'Baldy Parson', 'Alfred Lisbon']

    def test_multiple(self, characters):
        result = util.character_sorter.CharacterSorter('group', '-last').sort(characters)
        assert list(map(lambda c: c.get_first('name'), result)) == ['Baldy Parson', 'Alfred Lisbon', 'Zach Albright']

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
