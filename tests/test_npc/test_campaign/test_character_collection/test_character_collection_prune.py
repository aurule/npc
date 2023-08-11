from tests.fixtures import tmp_campaign, db
from sqlalchemy import select
from npc.characters import Character

from npc.campaign import CharacterCollection

def test_removes_empty_dirs(tmp_campaign, db):
    empty = tmp_campaign.characters_dir / "empty"
    empty.mkdir()
    collection = CharacterCollection(tmp_campaign, db=db)

    collection.prune_empty_dirs()

    assert not empty.exists()

def test_removes_parents_when_made_empty(tmp_campaign, db):
    to_empty = tmp_campaign.characters_dir / "to_empty"
    to_empty.mkdir()
    nothing = to_empty / "nothing"
    nothing.mkdir()
    collection = CharacterCollection(tmp_campaign, db=db)

    collection.prune_empty_dirs()

    assert not to_empty.exists()

def test_leaves_populated_dirs(tmp_campaign, db):
    full = tmp_campaign.characters_dir / "full"
    full.mkdir()
    test_file = full / "test.txt"
    test_file.touch()
    collection = CharacterCollection(tmp_campaign, db=db)

    collection.prune_empty_dirs()

    assert full.exists()
