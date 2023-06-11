from tests.fixtures import tmp_campaign

from npc.characters import Tag, Character
from npc.linters.tag_bucket import TagBucket
from npc.settings.tags import TagSpec

from npc.linters import CharacterLinter

def test_checks_char_attributes(tmp_campaign):
    character = Character()
    linter = CharacterLinter(character, tmp_campaign)

    linter.lint()

    assert linter.errors[0].tag_name == "type"

def test_skips_tags_without_file_loc(tmp_campaign):
    character = Character(
        realname="Test Mann",
        mnemonic="tester",
        type_key="person",
        desc="Oh hello",
        tags=[],
    )
    linter = CharacterLinter(character, tmp_campaign)

    linter.lint()

    assert len(linter.errors) == 0

def test_skips_with_missing_file(tmp_campaign):
    character = Character(
        realname="Test Mann",
        mnemonic="tester",
        type_key="person",
        desc="Oh hello",
        file_loc=tmp_campaign.characters_dir / "Test Mann - tester.npc",
        tags=[],
    )
    linter = CharacterLinter(character, tmp_campaign)

    linter.lint()

    assert len(linter.errors) == 0

def test_checks_tags(tmp_campaign):
    character = Character(
        realname="Test Mann",
        mnemonic="tester",
        type_key="person",
        desc="Oh hello",
        file_loc=tmp_campaign.characters_dir / "Test Mann - tester.npc",
        tags=[],
    )
    with character.file_path.open('w', newline="\n") as file:
        file.write("@type person\n@faketype blah\n@faketype bloo")
    linter = CharacterLinter(character, tmp_campaign)

    linter.lint()

    assert linter.errors[0].tag_name == "faketype"
