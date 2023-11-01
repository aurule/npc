from tests.fixtures import tmp_campaign
from npc.characters import Character, RawTag

from npc.characters import CharacterTagger

def test_removes_whitespace(tmp_campaign):
    character = Character()
    tagger = CharacterTagger(tmp_campaign, character)

    result = tagger.build_hide_value("thing  >> other")

    assert result == "thing>>other"

def test_adds_all_without_tag_value(tmp_campaign):
    character = Character()
    tagger = CharacterTagger(tmp_campaign, character)

    result = tagger.build_hide_value("thing")

    assert result == "thing>>all"
