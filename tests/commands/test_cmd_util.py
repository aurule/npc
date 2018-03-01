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
            npc.Character(name=['Alfred Lisbon']),
            npc.Character(name=['Baldy Parson']),
            npc.Character(name=['Zach Albright'])
        ]

    def test_default(self, characters):
        result = util.character_sorter.sort_characters(characters)
        control = util.character_sorter.sort_characters(characters, 'last')
        assert result == control

    def test_last(self, characters):
        result = util.character_sorter.sort_characters(characters, 'last')
        assert result[0].get_first('name') == 'Zach Albright'
        assert result[1].get_first('name') == 'Alfred Lisbon'
        assert result[2].get_first('name') == 'Baldy Parson'

    def test_first(self, characters):
        result = util.character_sorter.sort_characters(characters, 'first')
        assert result[0].get_first('name') == 'Alfred Lisbon'
        assert result[1].get_first('name') == 'Baldy Parson'
        assert result[2].get_first('name') == 'Zach Albright'

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
