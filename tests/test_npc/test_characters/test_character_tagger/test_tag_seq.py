from tests.fixtures import tmp_campaign
from npc.characters import Character, RawTag

from npc.characters import CharacterTagger

def test_returns_current_sequence_value(tmp_campaign):
    character = Character()
    tagger = CharacterTagger(tmp_campaign, character)

    result = tagger.tag_seq

    assert result == 0

def test_increments_sequence_value(tmp_campaign):
    character = Character()
    tagger = CharacterTagger(tmp_campaign, character)

    tagger.tag_seq
    result = tagger.tag_seq

    assert result == 1
