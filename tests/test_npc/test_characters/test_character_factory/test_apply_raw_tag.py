from tests.fixtures import tmp_campaign
from npc.characters import Character, RawTag

from npc.characters import CharacterFactory

def test_handles_mapped_tags(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)
    character = Character()
    rawtag = RawTag("realname", "Test Mann")
    stack = [character]

    new_stack = factory.apply_raw_tag(rawtag, character, stack)

    assert character.realname == "Test Mann"
    assert new_stack == stack

def test_makes_tag_for_mapped_when_instructed(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)
    character = Character()
    rawtag = RawTag("realname", "Test Mann")
    stack = [character]

    new_stack = factory.apply_raw_tag(rawtag, character, stack, mapped=False)

    assert character.realname != "Test Mann"
    assert character.tags[0].name == "realname"
    assert new_stack == stack

def test_handles_metatags(tmp_campaign):
    new_defs = {
        "metatags": {
            "test": {
                "desc": "A testing tag",
                "static": {
                    "foo": "bar"
                }
            }
        }
    }
    tmp_campaign.patch_campaign_settings(new_defs)
    factory = CharacterFactory(tmp_campaign)
    character = Character()
    rawtag = RawTag("test", "nope")
    stack = [character]

    new_stack = factory.apply_raw_tag(rawtag, character, stack)

    assert character.tags[0].name == "foo"
    assert new_stack == stack

def test_handles_regular_tags(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)
    character = Character()
    rawtag = RawTag("age", "55")
    stack = [character]

    new_stack = factory.apply_raw_tag(rawtag, character, stack)

    assert character.tags[0].name == "age"
    assert new_stack == stack
