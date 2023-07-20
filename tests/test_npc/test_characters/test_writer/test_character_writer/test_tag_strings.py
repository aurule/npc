import pytest
import re

from tests.fixtures import tmp_campaign, create_character
from npc.characters import CharacterFactory, Character, RawTag
from npc.campaign import Campaign
from npc.db import DB

from npc.characters import CharacterWriter

def test_rejects_incomplete_character(tmp_campaign):
    character = Character()
    db = DB(clearSingleton=True)
    writer = CharacterWriter(tmp_campaign, db=db)

    with pytest.raises(AttributeError):
        writer.tag_strings(character)

def test_includes_desc(tmp_campaign):
    db = DB(clearSingleton=True)
    character = create_character([], tmp_campaign, db, desc="test description")
    writer = CharacterWriter(tmp_campaign, db=db)

    result = writer.tag_strings(character)

    assert "test description" in result

def test_includes_contags(tmp_campaign):
    db = DB(clearSingleton=True)
    character = create_character([("delist", True)], tmp_campaign, db)
    writer = CharacterWriter(tmp_campaign, db=db)

    result = writer.tag_strings(character)

    assert "@delist" in result

def test_includes_normal_tags(tmp_campaign):
    db = DB(clearSingleton=True)
    character = create_character([("title", "True Bro")], tmp_campaign, db)
    writer = CharacterWriter(tmp_campaign, db=db)

    result = writer.tag_strings(character)

    assert "@title True Bro" in result

def test_includes_all_normal_tags(tmp_campaign):
    db = DB(clearSingleton=True)
    character = create_character([
        ("title", "True Bro"),
        ("title", "Esteemed"),
    ], tmp_campaign, db)
    writer = CharacterWriter(tmp_campaign, db=db)

    result = writer.tag_strings(character)

    assert "@title True Bro" in result
    assert "@title Esteemed" in result

def test_includes_metatags(tmp_campaign):
    tmp_campaign.patch_campaign_settings({"system": "nwod"})
    db = DB(clearSingleton=True)
    character = create_character(
        [
            ("seeming", "beast"),
            ("kith", "hunterheart"),
        ],
        tmp_campaign,
        db,
        type_key="changeling")
    writer = CharacterWriter(tmp_campaign, db=db)

    result = writer.tag_strings(character)

    assert "@changeling beast hunterheart" in result

def test_includes_unknown_tags(tmp_campaign):
    db = DB(clearSingleton=True)
    character = create_character([("asdf", "literally what")], tmp_campaign, db)
    writer = CharacterWriter(tmp_campaign, db=db)

    result = writer.tag_strings(character)

    assert "@asdf literally what" in result

def test_puts_unknowns_at_end_without_rest_block(tmp_campaign):
    new_defs = {
        "characters": {
            "use_blocks": ["flags", "bio", "geo", "assoc"]
        }
    }
    tmp_campaign.patch_campaign_settings(new_defs)
    db = DB(clearSingleton=True)
    character = create_character([("asdf", "literally what")], tmp_campaign, db)
    writer = CharacterWriter(tmp_campaign, db=db)

    result = writer.tag_strings(character)

    assert re.search(r"@asdf literally what$", result)

def test_puts_unknowns_at_rest_block(tmp_campaign):
    new_defs = {
        "characters": {
            "use_blocks": ["rest", "flags", "bio", "geo", "assoc"]
        }
    }
    tmp_campaign.patch_campaign_settings(new_defs)
    db = DB(clearSingleton=True)
    character = create_character([("asdf", "literally what")], tmp_campaign, db)
    writer = CharacterWriter(tmp_campaign, db=db)

    result = writer.tag_strings(character)

    assert re.search(r"^\n@asdf literally what", result)
