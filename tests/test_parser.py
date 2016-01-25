import npc
import pytest
import os

@pytest.fixture(scope="module")
def char_parser():
    base = os.path.dirname(os.path.realpath(__file__))
    parseables = os.path.join(base, "fixtures/parsing/characters")
    return npc.parser.get_characters(search_paths=[parseables])

def test_completeness(char_parser):
    test_against = [
        {'type': ['Changeling'], 'name': ['Chaser'], 'court': ['Summer'], 'description': 'Powerful dude in summer. Former USSOCOM operative, officially listed as MIA.', 'kith': ['Soldier'], 'rank': {'Summer': ['Arrayer of Distant Thunder']}, 'seeming': ['Wizened'], 'path': '/Users/pandrews/Workspace/npc/tests/fixtures/parsing/characters/Changelings/Chaser.nwod', 'motley': ['Something'] },
        {'type': ['Changeling'], 'group': ['Tolltaker Knighthood'], 'name': ['Foolish Mortal'], 'court': ['Summer'], 'description': 'Breaks things and hurts people for money, and for fun. Not a nice person. Gender is very hard to discern; he uses male pronouns as a matter of convenience. He claims his name comes from his Keeper, who only ever referred to him as "Foolish Mortal", with disdain.', 'kith': ['Gargantuan'], 'rank': {'Tolltaker Knighthood': ['Master at Harms'], 'Summer': ['Man at Arms', 'Arrayer of Distant Thunder']}, 'seeming': ['Ogre'], 'path': '/Users/pandrews/Workspace/npc/tests/fixtures/parsing/characters/Changelings/Foolish Mortal.nwod', 'motley': ['Fools Guild']},
        {'name': ['Kabana Matansa', 'Kabbie'], 'court': ['Spring'], 'mask': ['Hair is permanently spiked, and he dyes it in sections of contrasting colors.'], 'motley': ['Six Slices'], 'path': '/Users/pandrews/Workspace/npc/tests/fixtures/parsing/characters/Changelings/Kabana Matansa.nwod', 'type': ['Changeling'], 'group': ["Entertainer's Guild"], 'foreign': ['Chicago'], 'description': 'Speaks idiocy to power. Likes to test monarchs by spouting gibberish at them, then challenging them to discern it from the bizarre truths of the world.', 'rank': {'Spring': ['Jester']}, 'kith': ['Muse'], 'seeming': ['Fairest'], 'mien': ['Skin is shiney and polished, with no hard edges anywhere.']},
        {'type': ['Changeling'], 'name': ['Test Mann', 'Dickie to his enemies', "Simp to people who don't like him"], 'description': "A tester by nature, he pokes and pries everywhere he isn't welcome. Where he *is* welcome, he's a cheerful guy.", 'kith': ['Windwing'], 'rank': {}, 'seeming': ['Beast'], 'path': '/Users/pandrews/Workspace/npc/tests/fixtures/parsing/characters/Changelings/Test Mann.nwod'},
        {'name': ['Wines'], 'court': ['Autumn'], 'mien': ['Like water'], 'motley': ['Something'], 'path': '/Users/pandrews/Workspace/npc/tests/fixtures/parsing/characters/Changelings/Wines.nwod', 'type': ['Changeling'], 'group': ['PBPD'], 'description': 'Works within the police force to keep everyone safe', 'rank': {'PBPD': ['Det. Lt.']}, 'mask': ['Pallor to his skin'], 'kith': ['Brewer'], 'seeming': ['Wizened'], 'appearance': ['Very blue']},
        {'type': ['Fetch'], 'rank': {}, 'name': ['macho mannersson '], 'path': '/Users/pandrews/Workspace/npc/tests/fixtures/parsing/characters/Fetches/macho mannersson - faker.nwod', 'description': 'I know nossink!'},
        {'type': ['Goblin'], 'group': ['Wobtegwa Docklands'], 'name': ['Nopealope'], 'description': 'Natural-born coward. Catches his own wares nightly, then returns to the market by day to sell.', 'dead': ['Killed by the Fisher Twins while out'], 'rank': {}, 'path': '/Users/pandrews/Workspace/npc/tests/fixtures/parsing/characters/Goblins/Nopealope.nwod'},
        {'type': ['Human'], 'group': ['PBPD', 'Drop Squad Posse'], 'name': ['Winnifred Manchester III'], 'description': 'Winnie is not The Poo, but she hears that joke *way* too often. Good cop, keeps her head down, is consumed by existential angst over her role in society and the world.', 'rank': {}, 'path': '/Users/pandrews/Workspace/npc/tests/fixtures/parsing/characters/Humans/Winnifred Manchester III.nwod'}
    ]
    assert list(char_parser) == list(test_against)

