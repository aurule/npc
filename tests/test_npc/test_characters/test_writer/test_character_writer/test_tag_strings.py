import pytest
import re

from tests.fixtures import tmp_campaign, create_character, db
from npc.characters import Character
from npc.campaign import Campaign

from npc.characters import CharacterWriter

def test_rejects_incomplete_character(tmp_campaign, db):
    character = Character()
    writer = CharacterWriter(tmp_campaign, db=db)

    with pytest.raises(AttributeError):
        writer.tag_strings(character)

def test_includes_desc(tmp_campaign, db):
    character = create_character([], tmp_campaign, db, desc="test description")
    writer = CharacterWriter(tmp_campaign, db=db)

    result = writer.tag_strings(character)

    assert "test description" in result

def test_includes_contags(tmp_campaign, db):
    character = create_character([("delist", True)], tmp_campaign, db)
    writer = CharacterWriter(tmp_campaign, db=db)

    result = writer.tag_strings(character)

    assert "@delist" in result

def test_includes_normal_tags(tmp_campaign, db):
    character = create_character([("title", "True Bro")], tmp_campaign, db)
    writer = CharacterWriter(tmp_campaign, db=db)

    result = writer.tag_strings(character)

    assert "@title True Bro" in result

def test_includes_all_normal_tags(tmp_campaign, db):
    character = create_character([
        ("title", "True Bro"),
        ("title", "Esteemed"),
    ], tmp_campaign, db)
    writer = CharacterWriter(tmp_campaign, db=db)

    result = writer.tag_strings(character)

    assert "@title True Bro" in result
    assert "@title Esteemed" in result

def test_includes_metatags(tmp_campaign, db):
    tmp_campaign.patch_campaign_settings({"system": "nwod"})
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

def test_includes_unknown_tags(tmp_campaign, db):
    character = create_character([("asdf", "literally what")], tmp_campaign, db)
    writer = CharacterWriter(tmp_campaign, db=db)

    result = writer.tag_strings(character)

    assert "@asdf literally what" in result

def test_puts_unknowns_at_end_without_rest_block(tmp_campaign, db):
    new_defs = {
        "characters": {
            "use_blocks": ["flags", "bio", "geo", "assoc"]
        }
    }
    tmp_campaign.patch_campaign_settings(new_defs)
    character = create_character([("asdf", "literally what")], tmp_campaign, db)
    writer = CharacterWriter(tmp_campaign, db=db)

    result = writer.tag_strings(character)

    assert re.search(r"@asdf literally what$", result)

def test_puts_unknowns_at_rest_block(tmp_campaign, db):
    new_defs = {
        "characters": {
            "use_blocks": ["rest", "flags", "bio", "geo", "assoc"]
        }
    }
    tmp_campaign.patch_campaign_settings(new_defs)
    character = create_character([("asdf", "literally what")], tmp_campaign, db)
    writer = CharacterWriter(tmp_campaign, db=db)

    result = writer.tag_strings(character)

    assert re.search(r"^\n@asdf literally what", result)

def test_includes_hide_tags(tmp_campaign, db):
    character = create_character([
        ("title", "True Bro"),
        ("hide", "title"),
    ], tmp_campaign, db)
    writer = CharacterWriter(tmp_campaign, db=db)

    result = writer.tag_strings(character)

    assert "@title True Bro" in result
    assert "@hide title" in result
