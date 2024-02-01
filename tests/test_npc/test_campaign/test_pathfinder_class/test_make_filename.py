import pytest

from tests.fixtures import tmp_campaign, db
from npc.characters import Character, CharacterReader

from npc.campaign import Pathfinder

def test_uses_safe_name(tmp_campaign, db):
    character = Character(realname="Test Mann", mnemonic="")
    finder = Pathfinder(tmp_campaign, db=db)

    result = finder.make_filename(character)

    assert "Test Mann" in result

def test_sanitizes_unsafe_name(tmp_campaign, db):
    character = Character(realname='Test "Tester" Mann', mnemonic="")
    finder = Pathfinder(tmp_campaign, db=db)

    result = finder.make_filename(character)

    assert "Test _Tester_ Mann" in result

def test_uses_safe_mnemonic(tmp_campaign, db):
    character = Character(realname="jon", mnemonic="dragon man")
    finder = Pathfinder(tmp_campaign, db=db)

    result = finder.make_filename(character)

    assert "dragon man" in result

def test_sanitizes_unsafe_mnemonic(tmp_campaign, db):
    character = Character(realname="jon", mnemonic="dragon? man")
    finder = Pathfinder(tmp_campaign, db=db)

    result = finder.make_filename(character)

    assert "dragon_ man" in result

def test_uses_type_sheet_suffix(tmp_campaign, db):
    tmp_campaign.patch_campaign_settings({"system": "fate"})
    character = Character(realname="Test Mann", mnemonic="dragon man", type_key="supporting")
    finder = Pathfinder(tmp_campaign, db=db)

    result = finder.make_filename(character)

    assert ".fate" in result

def test_skips_empty_mnemonic(tmp_campaign, db):
    character = Character(realname="yoho", mnemonic="")
    finder = Pathfinder(tmp_campaign, db=db)

    result = finder.make_filename(character)

    assert CharacterReader.NAME_SEPARATOR not in result

def test_blank_without_name(tmp_campaign, db):
    character = Character(realname="", mnemonic="dragon man")
    finder = Pathfinder(tmp_campaign, db=db)

    result = finder.make_filename(character)

    assert result == ""
