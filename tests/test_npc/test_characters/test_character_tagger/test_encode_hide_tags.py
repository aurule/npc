from tests.fixtures import tmp_campaign
from npc.characters import Character, RawTag

from npc.characters import CharacterTagger

def test_saves_hidden_values(tmp_campaign):
    character = Character()
    tagger = CharacterTagger(tmp_campaign, character)
    tags = [RawTag("hide", "org")]

    tagger.encode_hide_tags(tags)

    assert tagger.hidden == ["org>>all"]

def test_excludes_hide_tags(tmp_campaign):
    character = Character()
    tagger = CharacterTagger(tmp_campaign, character)
    tags = [RawTag("hide", "org")]

    result = tagger.encode_hide_tags(tags)

    assert result == []

def test_includes_other_tags(tmp_campaign):
    character = Character()
    tagger = CharacterTagger(tmp_campaign, character)
    tags = [RawTag("hide", "org"), RawTag("org", "rebels")]

    result = tagger.encode_hide_tags(tags)

    assert len(result) == 1
