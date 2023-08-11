from tests.fixtures import fixture_file, db
from npc.campaign import Campaign

from npc.campaign.reorganizers import CharacterReorganizer

def test_gathers_all_characters(db):
    campaign = Campaign(fixture_file("reorg", "only_existing"))
    campaign.characters.refresh()
    reorganizer = CharacterReorganizer(campaign, db)

    reorganizer.gather_paths()

    assert len(reorganizer.relocations) == 2

def test_gets_ideal_paths_that_exist(db):
    campaign = Campaign(fixture_file("reorg", "only_existing"))
    campaign.characters.refresh()
    reorganizer = CharacterReorganizer(campaign, db, exists=True)

    reorganizer.gather_paths()

    for reloc in reorganizer.relocations:
        assert reloc.satisfied

def test_gets_ideal_paths_that_dont_exist(db):
    campaign = Campaign(fixture_file("reorg", "allow_new"))
    campaign.characters.refresh()
    reorganizer = CharacterReorganizer(campaign, db, exists=False)

    reorganizer.gather_paths()

    plan = reorganizer.make_movement_plan()
    assert len(plan) == 1
