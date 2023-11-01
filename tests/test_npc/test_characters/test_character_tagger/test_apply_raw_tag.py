from tests.fixtures import tmp_campaign
from npc.characters import Character, RawTag

from npc.characters import CharacterTagger

def test_handles_mapped_tags(tmp_campaign):
    character = Character()
    tagger = CharacterTagger(tmp_campaign, character)
    rawtag = RawTag("realname", "Test Mann")

    tagger.apply_raw_tag(rawtag)

    assert character.realname == "Test Mann"

def test_makes_tag_for_mapped_when_instructed(tmp_campaign):
    character = Character()
    tagger = CharacterTagger(tmp_campaign, character)
    rawtag = RawTag("realname", "Test Mann")

    tagger.apply_raw_tag(rawtag, mapped=False)

    assert character.realname != "Test Mann"
    assert character.tags[0].name == "realname"

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
    character = Character()
    tagger = CharacterTagger(tmp_campaign, character)
    rawtag = RawTag("test", "nope")

    tagger.apply_raw_tag(rawtag)

    assert character.tags[0].name == "foo"

def test_handles_regular_tags(tmp_campaign):
    character = Character()
    tagger = CharacterTagger(tmp_campaign, character)
    rawtag = RawTag("age", "55")

    tagger.apply_raw_tag(rawtag)

    assert character.tags[0].name == "age"
