from tests.fixtures import tmp_campaign
from npc.characters import Character, RawTag, Tag

from npc.characters import CharacterTagger

class TestTopLevelTag:
    def test_true_if_all(self, tmp_campaign):
        character = Character()
        tagger = CharacterTagger(tmp_campaign, character)
        tagger.hidden = ["thing>>all"]
        tag = Tag(name="thing", value="maybe")

        result = tagger.tag_is_hidden(tag)

        assert result == "all"

    def test_true_if_one(self, tmp_campaign):
        character = Character()
        tagger = CharacterTagger(tmp_campaign, character)
        tagger.hidden = ["thing>>maybe"]
        tag = Tag(name="thing", value="maybe")

        result = tagger.tag_is_hidden(tag)

        assert result == "one"

    def test_false_if_wrong_value(self, tmp_campaign):
        character = Character()
        tagger = CharacterTagger(tmp_campaign, character)
        tagger.hidden = ["thing>>other"]
        tag = Tag(name="thing", value="maybe")

        result = tagger.tag_is_hidden(tag)

        assert result is None

    def test_false_if_wrong_name(self, tmp_campaign):
        character = Character()
        tagger = CharacterTagger(tmp_campaign, character)
        tagger.hidden = ["something>>all"]
        tag = Tag(name="thing", value="maybe")

        result = tagger.tag_is_hidden(tag)

        assert result is None

    def test_false_if_nothing_hidden(self, tmp_campaign):
        character = Character()
        tagger = CharacterTagger(tmp_campaign, character)
        tag = Tag(name="thing", value="maybe")

        result = tagger.tag_is_hidden(tag)

        assert result is None

class TestSubTag:
    def test_works_on_subtags(self, tmp_campaign):
        character = Character()
        tagger = CharacterTagger(tmp_campaign, character)
        tagger.hidden = ["location>>here>>wanderer>>all"]
        parent_tag = Tag(name="location", value="here")
        tagger.context_stack.append(parent_tag)
        tag = Tag(name="wanderer")

        result = tagger.tag_is_hidden(tag)

        assert result == "all"
