import npc
import pytest
import os
from tests.util import fixture_dir

@pytest.fixture
def master_list(scope="session"):
    return [
        {'type': ['Changeling'], 'name': ['Chaser'], 'court': ['Summer'], 'description': 'Powerful dude in summer. Former USSOCOM operative, officially listed as MIA.', 'kith': ['Soldier'], 'rank': {'Summer': ['Arrayer of Distant Thunder']}, 'seeming': ['Wizened'], 'path': '/Users/pandrews/Workspace/npc/tests/fixtures/parsing/characters/Changelings/Chaser.nwod', 'motley': ['Something'] },
        {'type': ['Changeling'], 'group': ['Tolltaker Knighthood'], 'name': ['Foolish Mortal'], 'court': ['Summer'], 'description': 'Breaks things and hurts people for money, and for fun. Not a nice person. Gender is very hard to discern; he uses male pronouns as a matter of convenience. He claims his name comes from his Keeper, who only ever referred to him as "Foolish Mortal", with disdain.', 'kith': ['Gargantuan'], 'rank': {'Tolltaker Knighthood': ['Master at Harms'], 'Summer': ['Man at Arms', 'Arrayer of Distant Thunder']}, 'seeming': ['Ogre'], 'path': '/Users/pandrews/Workspace/npc/tests/fixtures/parsing/characters/Changelings/Foolish Mortal.nwod', 'motley': ['Fools Guild']},
        {'name': ['Kabana Matansa', 'Kabbie'], 'court': ['Spring'], 'mask': ['Hair is permanently spiked, and he dyes it in sections of contrasting colors.'], 'motley': ['Six Slices'], 'path': '/Users/pandrews/Workspace/npc/tests/fixtures/parsing/characters/Changelings/Kabana Matansa.nwod', 'type': ['Changeling'], 'group': ["Entertainer's Guild"], 'foreign': ['Chicago'], 'description': 'Speaks idiocy to power. Likes to test monarchs by spouting gibberish at them, then challenging them to discern it from the bizarre truths of the world.', 'rank': {'Spring': ['Jester']}, 'kith': ['Muse'], 'seeming': ['Fairest'], 'mien': ['Skin is shiney and polished, with no hard edges anywhere.']},
        {'type': ['Changeling'], 'name': ['Test Mann', 'Dickie to his enemies', "Simp to people who don't like him"], 'description': "A tester by nature, he pokes and pries everywhere he isn't welcome. Where he *is* welcome, he's a cheerful guy.", 'kith': ['Windwing'], 'rank': {}, 'seeming': ['Beast'], 'path': '/Users/pandrews/Workspace/npc/tests/fixtures/parsing/characters/Changelings/Test Mann.nwod'},
        {'name': ['Wines'], 'court': ['Autumn'], 'mien': ['Like water'], 'motley': ['Something'], 'path': '/Users/pandrews/Workspace/npc/tests/fixtures/parsing/characters/Changelings/Wines.nwod', 'type': ['Changeling'], 'group': ['PBPD'], 'description': 'Works within the police force to keep everyone safe', 'rank': {'PBPD': ['Det. Lt.']}, 'mask': ['Pallor to his skin'], 'kith': ['Brewer'], 'seeming': ['Wizened'], 'appearance': ['Very blue']},
        {'type': ['Fetch'], 'rank': {}, 'name': ['macho mannersson'], 'path': '/Users/pandrews/Workspace/npc/tests/fixtures/parsing/characters/Fetches/macho mannersson - faker.nwod', 'description': 'I know nossink!'},
        {'type': ['Goblin'], 'group': ['Wobtegwa Docklands'], 'name': ['Nopealope'], 'description': 'Natural-born coward. Catches his own wares nightly, then returns to the market by day to sell.', 'dead': ['Killed by the Fisher Twins while out'], 'rank': {}, 'path': '/Users/pandrews/Workspace/npc/tests/fixtures/parsing/characters/Goblins/Nopealope.nwod'},
        {'type': ['Human'], 'group': ['PBPD', 'Drop Squad Posse'], 'name': ['Winnifred Manchester III'], 'description': 'Winnie is not The Poo, but she hears that joke *way* too often. Good cop, keeps her head down, is consumed by existential angst over her role in society and the world.', 'rank': {}, 'path': '/Users/pandrews/Workspace/npc/tests/fixtures/parsing/characters/Humans/Winnifred Manchester III.nwod'}
    ]

def test_completeness(master_list):
    parseables = fixture_dir(['parsing', 'characters'])
    characters = npc.parser.get_characters(search_paths=[parseables])
    assert list(characters) == list(master_list)

def test_ignore_dir(master_list):
    parseables = fixture_dir(['parsing', 'characters'])
    ignore_me = fixture_dir(['parsing', 'characters', 'Fetches'])
    characters = npc.parser.get_characters(search_paths=[parseables], ignore_paths=[ignore_me])
    for c in characters:
        assert c['type'][0] != 'Fetch'

def test_ignore_file(master_list):
    parseables = fixture_dir(['parsing', 'characters'])
    ignore_me = fixture_dir(['parsing', 'characters', 'Changelings', 'Kabana Matansa.nwod'])
    characters = npc.parser.get_characters(search_paths=[parseables], ignore_paths=[ignore_me])
    for c in characters:
        assert 'Kabana Matansa' not in c['name']

def test_conflict_dir(master_list):
    """Ignore a directory when it is in both the search and ignore lists"""
    parseables = fixture_dir(['parsing', 'characters'])
    ignore_me = fixture_dir(['parsing', 'characters'])
    characters = npc.parser.get_characters(search_paths=[parseables], ignore_paths=[ignore_me])
    assert not len(list(characters))

def test_conflict_file():
    """Always parse a file when it is in the search and ignore lists"""
    parseables = fixture_dir(['parsing', 'characters', 'Changelings', 'Kabana Matansa.nwod'])
    ignore_me = fixture_dir(['parsing', 'characters', 'Changelings', 'Kabana Matansa.nwod'])
    characters = npc.parser.get_characters(search_paths=[parseables], ignore_paths=[ignore_me])
    assert len(list(characters)) == 1

def test_remove_filename_comments():
    parseables = fixture_dir(['parsing', 'characters', 'Fetches'])
    characters = list(npc.parser.get_characters(search_paths=[parseables]))
    assert characters[0]['name'][0] == 'macho mannersson'

class TestTags:
    """Tests the behavior of specific tags.

    Basic tag inclusion is handled above.
    """

    def test_changeling_shortcut(self):
        """@changeling should set type, seeming, and kith"""
        parseables = fixture_dir(['parsing', 'tags', 'Changeling Tag.nwod'])
        characters = list(npc.parser.get_characters(search_paths=[parseables]))
        c = characters[0]
        assert c['type'][0] == 'Changeling'
        assert c['seeming'][0] == 'Beast'
        assert c['kith'][0] == 'Hunterheart'

    def test_realname(self):
        """@realname should overwrite the first name entry"""
        parseables = fixture_dir(['parsing', 'tags', 'File Name.nwod'])
        characters = list(npc.parser.get_characters(search_paths=[parseables]))
        c = characters[0]
        assert c['name'][0] == 'Real Name'

    def test_group_rank(self):
        """@rank should scope its value to the most recent @group"""
        parseables = fixture_dir(['parsing', 'tags', 'Group Rank.nwod'])
        characters = list(npc.parser.get_characters(search_paths=[parseables]))
        c = characters[0]
        assert c['rank'] == {'Frat': ['Brother']}

    def test_bare_rank(self):
        """@rank should not be added without a prior @group"""
        parseables = fixture_dir(['parsing', 'tags', 'Bare Rank.nwod'])
        characters = list(npc.parser.get_characters(search_paths=[parseables]))
        c = characters[0]
        assert not c['rank']
