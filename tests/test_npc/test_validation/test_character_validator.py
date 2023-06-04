from tests.fixtures import tmp_campaign
from npc.characters import Character

from npc.validation import CharacterValidator

def test_missing_type(tmp_campaign):
    character = Character(
        realname="Test Mann",
        desc="tester",
        mnemonic="tester")
    validator = CharacterValidator(tmp_campaign)

    result = validator.validate(character)

    assert "missing value" in str(result[0])

def test_default_type(tmp_campaign):
    character = Character(
        realname="Test Mann",
        desc="tester",
        mnemonic="tester",
        type_key=Character.DEFAULT_TYPE)
    validator = CharacterValidator(tmp_campaign)

    result = validator.validate(character)

    assert "required" in str(result[0])

def test_bad_type(tmp_campaign):
    character = Character(
        realname="Test Mann",
        desc="tester",
        mnemonic="tester",
        type_key="nah")
    validator = CharacterValidator(tmp_campaign)

    result = validator.validate(character)

    assert "unrecognized" in str(result[0])

def test_missing_name(tmp_campaign):
    character = Character(
        desc="tester",
        mnemonic="tester",
        type_key="person")
    validator = CharacterValidator(tmp_campaign)

    result = validator.validate(character)

    assert "missing name" in str(result[0])

def test_missing_desc(tmp_campaign):
    character = Character(
        realname="Test Mann",
        mnemonic="tester",
        type_key="person")
    validator = CharacterValidator(tmp_campaign)

    result = validator.validate(character)

    assert "missing description" in str(result[0])

def test_missing_mnemonic(tmp_campaign):
    character = Character(
        realname="Test Mann",
        desc="tester",
        type_key="person")
    validator = CharacterValidator(tmp_campaign)

    result = validator.validate(character)

    assert "missing mnemonic" in str(result[0])
