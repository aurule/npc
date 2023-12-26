import pytest
from copy import copy
from tests.fixtures import tmp_campaign
from npc.characters import Character, RawTag

from npc.characters import CharacterTagger

class TestWithNonMappedTag():
    def test_returns_false(self, tmp_campaign):
        character = Character()
        tagger = CharacterTagger(tmp_campaign, character)
        tag = RawTag("fizzle", "yes")

        result = tagger.handle_mapped_tag(tag)

        assert not result

class TestWithMappedTag():
    def test_returns_true(self):
        character = Character()
        tagger = CharacterTagger(tmp_campaign, character)
        tag = RawTag("type", "person")

        result = tagger.handle_mapped_tag(tag)

        assert result

    def test_type_assigns_type_key(self):
        character = Character()
        tagger = CharacterTagger(tmp_campaign, character)
        tag = RawTag("type", "person")

        tagger.handle_mapped_tag(tag)

        assert character.type_key == "person"

    def test_realname_assigns_realname(self):
        character = Character()
        tagger = CharacterTagger(tmp_campaign, character)
        tag = RawTag("realname", "Hank")

        tagger.handle_mapped_tag(tag)

        assert character.realname == "Hank"

    def test_sticky_sets_sticky_true(self):
        character = Character()
        tagger = CharacterTagger(tmp_campaign, character)
        tag = RawTag("sticky", None)

        tagger.handle_mapped_tag(tag)

        assert character.sticky

    def test_nolint_sets_nolint_true(self):
        character = Character()
        tagger = CharacterTagger(tmp_campaign, character)
        tag = RawTag("nolint", None)

        tagger.handle_mapped_tag(tag)

        assert character.nolint

    def test_delist_sets_delist_true(self):
        character = Character()
        tagger = CharacterTagger(tmp_campaign, character)
        tag = RawTag("delist", None)

        tagger.handle_mapped_tag(tag)

        assert character.delist

    def test_type_sets_desc(self):
        character = Character()
        tagger = CharacterTagger(tmp_campaign, character)
        tag = RawTag("description", "a person")

        tagger.handle_mapped_tag(tag)

        assert character.desc == "a person"

    def test_type_appends_desc(self):
        character = Character(desc="some text or something")
        tagger = CharacterTagger(tmp_campaign, character)
        tag = RawTag("description", "a person")

        tagger.handle_mapped_tag(tag)

        assert character.desc == "some text or something\n\na person"
