from tests.fixtures import tmp_campaign, db
from sqlalchemy import select
from npc.characters import Character

from npc.campaign import CharacterCollection

def test_changes_existing_record(tmp_campaign, db):
    raise NotImplementedError()

def test_errors_on_bad_id(tmp_campaign, db):
    raise NotImplementedError()

def test_errors_on_bad_attr(tmp_campaign, db):
    raise NotImplementedError()
