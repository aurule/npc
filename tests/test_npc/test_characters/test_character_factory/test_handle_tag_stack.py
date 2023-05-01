from tests.fixtures import tmp_campaign
from npc.characters import Character, Tag
from npc.characters.character_factory import TagContext
from npc.settings import TagSpec, SubTagSpec
from npc.settings.tags import make_tags

from npc.characters import CharacterFactory

class TestWithoutContext():
    def test_adds_to_character(self, tmp_campaign):
        tag_defs = {
            "test": {
                "desc": "a test tag"
            }
        }
        specs = make_tags(tag_defs)
        character = Character()
        tag = Tag(name="test", value="yes")
        stack = []
        factory = CharacterFactory(tmp_campaign)

        factory.handle_tag_stack(character, tag, specs["test"], stack)

        assert tag in character.tags

    def test_with_subtags_pushes_to_stack(self, tmp_campaign):
        tag_defs = {
            "test": {
                "desc": "a test tag",
                "subtags": {
                    "oops": {
                        "desc": "a thing"
                    }
                }
            }
        }
        specs = make_tags(tag_defs)
        character = Character()
        tag = Tag(name="test", value="yes")
        stack = []
        factory = CharacterFactory(tmp_campaign)

        factory.handle_tag_stack(character, tag, specs["test"], stack)

        assert tag == stack[0].tag

class TestWithContextAndMatch():
    def test_appends_to_context_tag(self, tmp_campaign):
        tag_defs = {
            "parent": {
                "desc": "a parent tag",
                "subtags": {
                    "test": {
                        "desc": "the tag to test"
                    }
                }
            }
        }
        specs = make_tags(tag_defs)
        character = Character()
        parent_tag = Tag(name="parent", value="yes")
        tag = Tag(name="test", value="yes")
        stack = [TagContext(parent_tag, ["test"])]
        factory = CharacterFactory(tmp_campaign)

        factory.handle_tag_stack(character, tag, specs["test"], stack)

        assert tag in parent_tag.subtags

    def test_with_subtags_pushes_to_stack(self, tmp_campaign):
        tag_defs = {
            "parent": {
                "desc": "a parent tag",
                "subtags": {
                    "test": {
                        "desc": "the tag to test",
                        "subtags": {
                            "another": {
                                "desc": "another nested tag"
                            }
                        }
                    }
                }
            }
        }
        specs = make_tags(tag_defs)
        character = Character()
        parent_tag = Tag(name="parent", value="yes")
        tag = Tag(name="test", value="yes")
        stack = [TagContext(parent_tag, ["test"])]
        factory = CharacterFactory(tmp_campaign)

        factory.handle_tag_stack(character, tag, specs["test"], stack)

        assert tag == stack[1].tag

class TestWithContextAndNotMatch():
    def test_pops_from_stack(self, tmp_campaign):
        tag_defs = {
            "test": {
                "desc": "a test tag"
            }
        }
        specs = make_tags(tag_defs)
        character = Character()
        parent_tag = Tag(name="parent", value="yes")
        tag = Tag(name="test", value="yes")
        stack = [TagContext(parent_tag, ["nope"])]
        factory = CharacterFactory(tmp_campaign)

        factory.handle_tag_stack(character, tag, specs["test"], stack)

        assert not stack

    def test_tries_one_level_up(self, tmp_campaign):
        tag_defs = {
            "parent": {
                "desc": "a parent tag",
                "subtags": {
                    "test": {
                        "desc": "the tag to test",
                        "subtags": {
                            "another": {
                                "desc": "another nested tag"
                            }
                        }
                    }
                }
            }
        }
        specs = make_tags(tag_defs)
        character = Character()
        top_parent_tag = Tag(name="parent", value="yes")
        middle_tag = Tag(name="test", value="yes")
        tag = Tag(name="test", value="welp")
        stack = [
            TagContext(top_parent_tag, ["test"]),
            TagContext(middle_tag, ["another"]),
        ]
        factory = CharacterFactory(tmp_campaign)

        factory.handle_tag_stack(character, tag, specs["test"], stack)

        assert tag in top_parent_tag.subtags

    def test_adds_to_character_with_no_matches_anywhere(self, tmp_campaign):
        tag_defs = {
            "parent": {
                "desc": "a parent tag",
                "subtags": {
                    "test": {
                        "desc": "the tag to test",
                        "subtags": {
                            "another": {
                                "desc": "another nested tag"
                            }
                        }
                    }
                }
            },
            "other": {
                "desc": "something else"
            }
        }
        specs = make_tags(tag_defs)
        character = Character()
        top_parent_tag = Tag(name="parent", value="yes")
        middle_tag = Tag(name="test", value="yes")
        tag = Tag(name="other", value="welp")
        stack = [
            TagContext(top_parent_tag, ["test"]),
            TagContext(middle_tag, ["another"]),
        ]
        factory = CharacterFactory(tmp_campaign)

        factory.handle_tag_stack(character, tag, specs["other"], stack)

        assert tag in character.tags
