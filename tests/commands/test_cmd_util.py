import npc
from npc.commands import util

import pytest
from tests.util import fixture_dir

class TestCreatePath:
    def test_no_type(self, tmpdir):
        char = npc.Character(type=['human'])
        result = util.create_path_from_character(char, base_path=str(tmpdir))
        assert result == str(tmpdir)

    def test_type(self, tmpdir):
        char = npc.Character(type=['human'])
        tmpdir.mkdir('Humans')
        result = util.create_path_from_character(char, base_path=str(tmpdir))
        assert result == str(tmpdir.join('Humans'))

    def test_changeling_court(self, tmpdir):
        char = npc.Character(type=['changeling'], court=['Spring'])
        tmpdir.mkdir('Changelings')
        tmpdir.join('Changelings').mkdir('Spring')
        result = util.create_path_from_character(char, base_path=str(tmpdir))
        assert result == str(tmpdir.join('Changelings', 'Spring'))

    def test_changeling_courtless(self, tmpdir):
        char = npc.Character(type=['changeling'])
        tmpdir.mkdir('Changelings')
        tmpdir.join('Changelings').mkdir('Courtless')
        result = util.create_path_from_character(char, base_path=str(tmpdir))
        assert result == str(tmpdir.join('Changelings', 'Courtless'))

    @pytest.mark.parametrize('tagname', ('foreign', 'wanderer'))
    def test_foreign(self, tmpdir, tagname):
        char = npc.Character()
        char.append(tagname, 'Chicago')
        tmpdir.mkdir('Foreign')
        result = util.create_path_from_character(char, base_path=str(tmpdir))
        assert result == str(tmpdir.join('Foreign'))

    def test_nested_groups(self, tmpdir):
        char = npc.Character(group=['group1', 'group2'])
        tmpdir.mkdir('group1')
        tmpdir.join('group1').mkdir('group2')
        result = util.create_path_from_character(char, base_path=str(tmpdir))
        assert result == str(tmpdir.join('group1', 'group2'))

    def test_sequential_groups(self, tmpdir):
        char = npc.Character(group=['group1', 'group2'])
        tmpdir.mkdir('group1')
        tmpdir.mkdir('group2')
        result = util.create_path_from_character(char, base_path=str(tmpdir))
        assert result == str(tmpdir.join('group1'))

    def test_missing_group_dir(self, tmpdir):
        char = npc.Character(group=['group1', 'group2'])
        tmpdir.mkdir('group2')
        result = util.create_path_from_character(char, base_path=str(tmpdir))
        assert result == str(tmpdir.join('group2'))

    def test_precedence(self, tmpdir):
        """Order should be type, changeling court or courtless, foreign, group"""
        attributes = {
            "type": ['changeling'],
            "court": ['Summer'],
            "foreign": ['Chicago'],
            'group': ['group1', 'group2']
        }
        char = npc.Character(attributes=attributes)
        tmpdir.mkdir('Changelings')
        tmpdir.join('Changelings').mkdir('Foreign')
        tmpdir.join('Changelings', 'Foreign').mkdir('Summer')
        tmpdir.join('Changelings').mkdir('Summer')
        tmpdir.join('Changelings', 'Summer').mkdir('group2')
        tmpdir.join('Changelings').mkdir('group2')

        result = util.create_path_from_character(char, base_path=str(tmpdir))
        assert result == str(tmpdir.join('Changelings', 'Summer', 'group2'))

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
        result = util.sort_characters(characters)
        control = util.sort_characters(characters, 'last')
        assert result == control

    def test_last(self, characters):
        result = util.sort_characters(characters, 'last')
        assert result[0].get_first('name') == 'Zach Albright'
        assert result[1].get_first('name') == 'Alfred Lisbon'
        assert result[2].get_first('name') == 'Baldy Parson'

    def test_first(self, characters):
        result = util.sort_characters(characters, 'first')
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
