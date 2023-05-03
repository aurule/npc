import pytest
from copy import copy
from tests.fixtures import tmp_campaign
from npc.characters import Character, RawTag

from npc.characters import CharacterFactory

class TestWithNonMappedTag():
    def test_returns_false(self, tmp_campaign):
        factory = CharacterFactory(tmp_campaign)
        character = Character()
        tag = RawTag("fizzle", "yes")

        result = factory.handle_mapped_tag(tag, character)

        assert not result

class TestWithMappedTag():
    def test_returns_true(self):
        factory = CharacterFactory(tmp_campaign)
        character = Character()
        tag = RawTag("type", "person")

        result = factory.handle_mapped_tag(tag, character)

        assert result

    def test_type_assigns_type_key(self):
        factory = CharacterFactory(tmp_campaign)
        character = Character()
        tag = RawTag("type", "person")

        factory.handle_mapped_tag(tag, character)

        assert character.type_key == "person"

    def test_realname_assigns_realname(self):
        factory = CharacterFactory(tmp_campaign)
        character = Character()
        tag = RawTag("realname", "Hank")

        factory.handle_mapped_tag(tag, character)

        assert character.realname == "Hank"

    def test_sticky_sets_sticky_true(self):
        factory = CharacterFactory(tmp_campaign)
        character = Character()
        tag = RawTag("sticky", None)

        factory.handle_mapped_tag(tag, character)

        assert character.sticky

    def test_nolint_sets_nolint_true(self):
        factory = CharacterFactory(tmp_campaign)
        character = Character()
        tag = RawTag("nolint", None)

        factory.handle_mapped_tag(tag, character)

        assert character.nolint

    def test_delist_sets_delist_true(self):
        factory = CharacterFactory(tmp_campaign)
        character = Character()
        tag = RawTag("delist", None)

        factory.handle_mapped_tag(tag, character)

        assert character.delist

    def test_unkonwn_throws_error(self):
        factory = CharacterFactory(tmp_campaign)
        Character.MAPPED_TAGS.append("invalid")
        character = Character()
        tag = RawTag("invalid", None)

        with pytest.raises(NotImplementedError):
            factory.handle_mapped_tag(tag, character)

        Character.MAPPED_TAGS.pop()
