from tests.fixtures import tmp_campaign
from npc.characters import Character, RawTag

from npc.characters import CharacterTagger

def test_saves_hidden_values(tmp_campaign):
    character = Character()
    tagger = CharacterTagger(tmp_campaign, character)
    tags = [RawTag("hide", "org")]

    tagger.apply_tags(tags)

    assert tagger.hidden == ["org>>all"]

def test_applies_remaining_tags(tmp_campaign):
    character = Character()
    tagger = CharacterTagger(tmp_campaign, character)
    tags = [RawTag("hide", "org"), RawTag("org", "rebels")]

    tagger.apply_tags(tags)

    assert character.tags[0].name == "org"
