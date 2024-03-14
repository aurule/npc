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

class TestHandlesMetatags:
    """This incidentally tests the expand_metatag internal method"""

    def test_creates_static_tags(self, tmp_campaign):
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

    def test_match_creates_known_tags(self, tmp_campaign):
        new_defs = {
            "metatags": {
                "test": {
                    "desc": "A testing tag",
                    "static": {
                        "foo": "bar"
                    },
                    "match": [
                        "name"
                    ]
                }
            }
        }
        tmp_campaign.patch_campaign_settings(new_defs)
        character = Character()
        tagger = CharacterTagger(tmp_campaign, character)
        rawtag = RawTag("test", "nope")

        tagger.apply_raw_tag(rawtag)

        assert character.tags[1].name == "name"

    def test_match_creates_unknown_tags(self, tmp_campaign):
        new_defs = {
            "metatags": {
                "test": {
                    "desc": "A testing tag",
                    "static": {
                        "foo": "bar"
                    },
                    "match": [
                        "fimbul"
                    ]
                }
            }
        }
        tmp_campaign.patch_campaign_settings(new_defs)
        character = Character()
        tagger = CharacterTagger(tmp_campaign, character)
        rawtag = RawTag("test", "nope")

        tagger.apply_raw_tag(rawtag)

        assert character.tags[1].name == "fimbul"

    def test_match_creates_known_subtags(self, tmp_campaign):
        new_defs = {
            "metatags": {
                "test": {
                    "desc": "A testing tag",
                    "static": {
                        "foo": "bar"
                    },
                    "match": [
                        "name",
                        "with"
                    ]
                }
            }
        }
        tmp_campaign.patch_campaign_settings(new_defs)
        character = Character()
        tagger = CharacterTagger(tmp_campaign, character)
        rawtag = RawTag("test", "nope alope")

        tagger.apply_raw_tag(rawtag)

        name_tag = character.tags[1]
        assert name_tag.name == "name"
        assert name_tag.subtags[0].name == "with"

    def test_match_creates_subtags_then_main_tags(self, tmp_campaign):
        new_defs = {
            "metatags": {
                "test": {
                    "desc": "A testing tag",
                    "static": {
                        "foo": "bar"
                    },
                    "match": [
                        "name",
                        "with",
                        "fimbul"
                    ]
                }
            }
        }
        tmp_campaign.patch_campaign_settings(new_defs)
        character = Character()
        tagger = CharacterTagger(tmp_campaign, character)
        rawtag = RawTag("test", "nope alope")

        tagger.apply_raw_tag(rawtag)

        assert character.tags[2].name == "fimbul"

    def test_match_handles_incorrect_subtag(self, tmp_campaign):
        new_defs = {
            "metatags": {
                "test": {
                    "desc": "A testing tag",
                    "static": {
                        "foo": "bar"
                    },
                    "match": [
                        "name",
                        "role"
                    ]
                }
            }
        }
        tmp_campaign.patch_campaign_settings(new_defs)
        character = Character()
        tagger = CharacterTagger(tmp_campaign, character)
        rawtag = RawTag("test", "nope alope")

        tagger.apply_raw_tag(rawtag)

        assert character.tags[2].name == "role"

def test_handles_regular_tags(tmp_campaign):
    character = Character()
    tagger = CharacterTagger(tmp_campaign, character)
    rawtag = RawTag("age", "55")

    tagger.apply_raw_tag(rawtag)

    assert character.tags[0].name == "age"

def test_sets_hidden_attr(tmp_campaign):
    character = Character()
    tagger = CharacterTagger(tmp_campaign, character)
    tagger.hidden = ["age>>all"]
    rawtag = RawTag("age", "55")

    tagger.apply_raw_tag(rawtag)

    assert character.tags[0].hidden == "all"

def test_handles_no_value(tmp_campaign):
    character = Character()
    tagger = CharacterTagger(tmp_campaign, character)
    rawtag = RawTag("foreign", "mars")

    tagger.apply_raw_tag(rawtag)

    assert character.tags[0].value is None

def test_handles_incorrect_subtag(tmp_campaign):
    character = Character()
    tagger = CharacterTagger(tmp_campaign, character)
    rawtag1 = RawTag("group", "band")
    rawtag2 = RawTag("role", "front man")

    tagger.apply_raw_tag(rawtag1)
    tagger.apply_raw_tag(rawtag2)

    assert character.tags[1].name == "role"
