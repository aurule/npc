import npc
import pytest
import os

@pytest.fixture
def characters(campaign, prefs):
    os.mkdir(prefs.get('paths.characters'))
    return campaign

@pytest.fixture(params=['human', 'fetch', 'goblin'])
def commandline(request):
    return ['g', 'testmann', request.param, '-g', 'fork', 'spoon']

def test_missing_template(parser, prefs, campaign):
    args = parser.parse_args(['g', 'noname', 'notfound'])
    result = npc.commands.create_simple(args, prefs)
    assert not result.success
    assert result.errcode == 7

def test_creates_character(parser, prefs, characters, commandline):
    args = parser.parse_args(commandline)
    result = npc.commands.create_simple(args, prefs)
    assert result.success
    character = characters.join(prefs.get('paths.characters'), 'testmann.nwod')
    assert character.check()

def test_duplicate_character(parser, prefs, characters, commandline):
    args = parser.parse_args(commandline)
    npc.commands.create_simple(args, prefs)
    result = npc.commands.create_simple(args, prefs)
    assert not result.success
    assert result.errcode == 1

def test_adds_group_tags(parser, prefs, characters, commandline):
    args = parser.parse_args(commandline)
    npc.commands.create_simple(args, prefs)
    character = characters.join(prefs.get('paths.characters'), 'testmann.nwod')
    data = next(c for c in npc.parser.get_characters([str(character)], []))
    assert data['group'] == ['fork', 'spoon']
