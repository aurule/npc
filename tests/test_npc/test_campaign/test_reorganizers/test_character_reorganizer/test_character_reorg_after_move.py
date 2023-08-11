from tests.fixtures import fixture_file, db
from npc.campaign import Campaign

from npc.campaign.reorganizers import CharacterReorganizer

def test_updates_db(db):
    campaign = Campaign(fixture_file("reorg", "allow_new"))
    campaign.characters.refresh()
    reorganizer = CharacterReorganizer(campaign, db, exists=False)
    reorganizer.gather_paths()
    plan = reorganizer.make_movement_plan()
    reloc = plan[0]

    reorganizer.after_move(reloc)

    char = campaign.characters.get(reloc.id)
    assert char.file_path == reloc.ideal_path
