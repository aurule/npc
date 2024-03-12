from sqlalchemy import select, func
from tests.fixtures import tmp_campaign, db
from npc.characters import Character

from npc.campaign import CharacterCollection

def test_includes_top_level(tmp_campaign, db):
    loc = tmp_campaign.characters_dir / "Test Mann - tester.npc"
    with loc.open('w', newline="\n") as file:
        file.write("@type person")
    collection = CharacterCollection(tmp_campaign, db=db)

    result = list(collection.valid_character_files())

    assert loc in result

def test_includes_subdirs(tmp_campaign, db):
    tmp_campaign.patch_campaign_settings({
        "characters": {
            "ignore_subpaths": ["noplz"]
        }
    })
    subdir = tmp_campaign.characters_dir / "yesplz"
    subdir.mkdir()
    loc = subdir / "Test Mann - tester.npc"
    with loc.open('w', newline="\n") as file:
        file.write("@type person")
    collection = CharacterCollection(tmp_campaign, db=db)

    result = list(collection.valid_character_files())

    assert loc in result

def test_skips_ignored_dirs(tmp_campaign, db):
    tmp_campaign.patch_campaign_settings({
        "characters": {
            "ignore_subpaths": ["noplz"]
        }
    })
    ignored = tmp_campaign.characters_dir / "noplz"
    ignored.mkdir()
    loc = ignored / "Test Mann - tester.npc"
    with loc.open('w', newline="\n") as file:
        file.write("@type person")
    collection = CharacterCollection(tmp_campaign, db=db)

    result = list(collection.valid_character_files())

    assert loc not in result

def test_includes_npc_suffix(tmp_campaign, db):
    loc = tmp_campaign.characters_dir / "Test Mann - tester.npc"
    with loc.open('w', newline="\n") as file:
        file.write("@type person")
    collection = CharacterCollection(tmp_campaign, db=db)

    result = list(collection.valid_character_files())

    assert loc in result

def test_includes_type_suffix(tmp_campaign, db):
    tmp_campaign.patch_campaign_settings({"system": "fate"})
    loc = tmp_campaign.characters_dir / "Test Mann - tester.fate"
    with loc.open('w', newline="\n") as file:
        file.write("@type person")
    collection = CharacterCollection(tmp_campaign, db=db)
    pass

def test_skips_non_sheets(tmp_campaign, db):
    loc = tmp_campaign.characters_dir / "Test Mann - tester.nope"
    with loc.open('w', newline="\n") as file:
        file.write("@type person")
    collection = CharacterCollection(tmp_campaign, db=db)

    result = list(collection.valid_character_files())

    assert loc not in result
