from tests.fixtures import tmp_campaign
from npc.characters import Character, RawTag, Tag

from npc.characters import CharacterTagger

def test_true_if_all(tmp_campaign):
    character = Character()
    tagger = CharacterTagger(tmp_campaign, character)
    tagger.hidden = ["thing>>all"]
    tag = Tag(name="thing", value="maybe")

    result = tagger.tag_is_hidden(tag)

    assert result == "all"

def test_true_if_one(tmp_campaign):
    character = Character()
    tagger = CharacterTagger(tmp_campaign, character)
    tagger.hidden = ["thing>>maybe"]
    tag = Tag(name="thing", value="maybe")

    result = tagger.tag_is_hidden(tag)

    assert result == "one"

def test_false_if_wrong_value(tmp_campaign):
    character = Character()
    tagger = CharacterTagger(tmp_campaign, character)
    tagger.hidden = ["thing>>other"]
    tag = Tag(name="thing", value="maybe")

    result = tagger.tag_is_hidden(tag)

    assert result is None

def test_false_if_wrong_name(tmp_campaign):
    character = Character()
    tagger = CharacterTagger(tmp_campaign, character)
    tagger.hidden = ["something>>all"]
    tag = Tag(name="thing", value="maybe")

    result = tagger.tag_is_hidden(tag)

    assert result is None

def test_false_if_nothing_hidden(tmp_campaign):
    character = Character()
    tagger = CharacterTagger(tmp_campaign, character)
    tag = Tag(name="thing", value="maybe")

    result = tagger.tag_is_hidden(tag)

    assert result is None
