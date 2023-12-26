from tests.fixtures import tmp_campaign, db

from npc.characters import Character

from npc_cli.helpers import write_new_character

def test_adds_to_db(tmp_campaign, db):
    character = Character(
        realname="Test Mann",
        mnemonic="nah",
        type_key="person",
        file_body="")

    write_new_character(character, tmp_campaign, db=db)

    assert character.id

def test_updates_character_path(tmp_campaign, db):
    character = Character(
        realname="Test Mann",
        mnemonic="nah",
        type_key="person",
        file_body="")

    write_new_character(character, tmp_campaign, db=db)

    assert character.file_loc

def test_creates_file(tmp_campaign, db):
    character = Character(
        realname="Test Mann",
        mnemonic="nah",
        type_key="person",
        file_body="")

    write_new_character(character, tmp_campaign, db=db)

    assert character.file_path.exists()
