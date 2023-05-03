from tests.fixtures import tmp_campaign
from npc.characters import RawTag

from npc.characters import CharacterFactory

def test_saves_realname(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)

    character = factory.make("Test Mann")

    assert character.realname == "Test Mann"

def test_saves_type(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)

    character = factory.make("Test Mann", type_key = "person")

    assert character.type_key == "person"

def test_allows_unknown_type(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)

    character = factory.make("Test Mann", type_key = "nope")

    assert character.type_key == "nope"

def test_handles_mapped_tags(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)
    tags = [RawTag("type", "humanoid")]

    character = factory.make("Test Mann", tags=tags)

    assert character.type_key == "humanoid"

def test_adds_regular_tags(tmp_campaign):
    factory = CharacterFactory(tmp_campaign)
    tags = [RawTag("kingdom", "animalia")]

    character = factory.make("Test Mann", tags=tags)

    assert "kingdom" in [tag.name for tag in character.tags]

class TestNestedTag():
    def test_adds_deep_nested_tags(self, tmp_campaign):
        new_defs = {
            "tags": {
                "test1": {
                    "desc": "First test tag",
                    "subtags": {
                        "test2": {
                            "desc": "Second test tag",
                            "subtags": {
                                "test3": {
                                    "desc": "Third test tag",
                                }
                            }
                        }
                    }
                }
            }
        }
        tmp_campaign.patch_campaign_settings(new_defs)
        factory = CharacterFactory(tmp_campaign)
        tags = [
            RawTag("test1", "Testers"),
            RawTag("test2", "Lead"),
            RawTag("test3", "Pro"),
        ]

        character = factory.make("Test Mann", tags=tags)

        assert character.tags[0].subtags[0].subtags[0].value == "Pro"

    def test_adds_shallow_nested_tags(self, tmp_campaign):
        factory = CharacterFactory(tmp_campaign)
        tags = [
            RawTag("group", "Testers"),
            RawTag("rank", "Lead"),
        ]

        character = factory.make("Test Mann", tags=tags)

        assert character.tags[0].subtags[0].value == "Lead"

class TestMetatagsStatic():
    def test_adds_tags(self, tmp_campaign):
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
        factory = CharacterFactory(tmp_campaign)
        tags = [
            RawTag("test", "Testers"),
        ]

        character = factory.make("Test Mann", tags=tags)

        assert character.tags[0].name == "foo"
        assert character.tags[0].value == "bar"

    def test_preserves_order(self, tmp_campaign):
        new_defs = {
            "metatags": {
                "test": {
                    "desc": "A testing tag",
                    "static": {
                        "foo": "bar",
                        "fuzzy": "wuzzy",
                    }
                }
            }
        }
        tmp_campaign.patch_campaign_settings(new_defs)
        factory = CharacterFactory(tmp_campaign)
        tags = [
            RawTag("test", "Testers"),
        ]

        character = factory.make("Test Mann", tags=tags)

        assert character.tags[0].name == "foo"
        assert character.tags[1].name == "fuzzy"

    def test_makes_subtags(self, tmp_campaign):
        new_defs = {
            "metatags": {
                "test": {
                    "desc": "A testing tag",
                    "static": {
                        "employer": "bear",
                        "job": "wuzzy",
                    }
                }
            }
        }
        tmp_campaign.patch_campaign_settings(new_defs)
        factory = CharacterFactory(tmp_campaign)
        tags = [
            RawTag("test", "Testers"),
        ]

        character = factory.make("Test Mann", tags=tags)

        assert character.tags[0].subtags[0].name == "job"

class TestMetadataValues():
    def test_adds_match_tag(self, tmp_campaign):
        new_defs = {
            "metatags": {
                "test": {
                    "match": ["single"]
                }
            },
            "tags": {
                "single": {
                    "desc": "Has multiple values",
                    "values": ["first"]
                }
            }
        }
        tmp_campaign.patch_campaign_settings(new_defs)
        factory = CharacterFactory(tmp_campaign)
        tags = [
            RawTag("test", "first"),
        ]

        character = factory.make("Test Mann", tags=tags)

        assert character.tags[0].name == "single"
        assert character.tags[0].value == "first"

    def test_uses_first_match(self, tmp_campaign):
        new_defs = {
            "metatags": {
                "test": {
                    "match": ["multi"]
                }
            },
            "tags": {
                "multi": {
                    "desc": "Has multiple values",
                    "values": ["first", "firstly", "firstest"]
                }
            }
        }
        tmp_campaign.patch_campaign_settings(new_defs)
        factory = CharacterFactory(tmp_campaign)
        tags = [
            RawTag("test", "firstest"),
        ]

        character = factory.make("Test Mann", tags=tags)

        assert character.tags[0].name == "multi"
        assert character.tags[0].value == "first"

    def test_drops_extra_values(self, tmp_campaign):
        new_defs = {
            "metatags": {
                "test": {
                    "match": ["single"]
                }
            },
            "tags": {
                "single": {
                    "desc": "Has multiple values",
                    "values": ["first", "second"]
                }
            }
        }
        tmp_campaign.patch_campaign_settings(new_defs)
        factory = CharacterFactory(tmp_campaign)
        tags = [
            RawTag("test", "first and then more"),
        ]

        character = factory.make("Test Mann", tags=tags)

        assert character.tags[0].name == "single"
        assert character.tags[0].value == "first"

    def test_ignores_separator(self, tmp_campaign):
        new_defs = {
            "metatags": {
                "test": {
                    "match": ["multi"]
                }
            },
            "tags": {
                "multi": {
                    "desc": "Has multiple values",
                    "values": ["first last"]
                }
            }
        }
        tmp_campaign.patch_campaign_settings(new_defs)
        factory = CharacterFactory(tmp_campaign)
        tags = [
            RawTag("test", "first last"),
        ]

        character = factory.make("Test Mann", tags=tags)

        assert character.tags[0].name == "multi"
        assert character.tags[0].value == "first last"

    def test_falls_back_on_separator(self, tmp_campaign):
        new_defs = {
            "metatags": {
                "test": {
                    "match": ["single"]
                }
            },
            "tags": {
                "single": {
                    "desc": "Has multiple values",
                    "values": ["first"]
                }
            }
        }
        tmp_campaign.patch_campaign_settings(new_defs)
        factory = CharacterFactory(tmp_campaign)
        tags = [
            RawTag("test", "something else"),
        ]

        character = factory.make("Test Mann", tags=tags)

        assert character.tags[0].name == "single"
        assert character.tags[0].value == "something"

    def test_uses_subtag_values(self, tmp_campaign):
        new_defs = {
            "metatags": {
                "test": {
                    "match": ["multi", "single"]
                }
            },
            "tags": {
                "multi": {
                    "desc": "Has multiple values",
                    "values": ["first last", "other"],
                    "subtags": {
                        "single": {
                            "desc": "A subtag with values",
                            "values": ["nope", "alope"]
                        }
                    }
                }
            }
        }
        tmp_campaign.patch_campaign_settings(new_defs)
        factory = CharacterFactory(tmp_campaign)
        tags = [
            RawTag("test", "first last alope"),
        ]

        character = factory.make("Test Mann", tags=tags)

        assert character.tags[0].name == "multi"
        assert character.tags[0].value == "first last"

        assert character.tags[0].subtags[0].name == "single"
        assert character.tags[0].subtags[0].value == "alope"

class TestMetadataSeparator():
    def test_creates_tag_to_first_sep(self, tmp_campaign):
        new_defs = {
            "metatags": {
                "test": {
                    "desc": "A testing tag",
                    "match": ["name", "title"],
                    "separator": ";",
                }
            }
        }
        tmp_campaign.patch_campaign_settings(new_defs)
        factory = CharacterFactory(tmp_campaign)
        tags = [
            RawTag("test", "whatevs;brainiac"),
        ]

        character = factory.make("Test Mann", tags=tags)

        assert character.tags[0].name == "name"
        assert character.tags[0].value == "whatevs"

    def test_creates_multiple_tags(self, tmp_campaign):
        new_defs = {
            "metatags": {
                "test": {
                    "desc": "A testing tag",
                    "match": ["name", "title"],
                    "separator": ";",
                }
            }
        }
        tmp_campaign.patch_campaign_settings(new_defs)
        factory = CharacterFactory(tmp_campaign)
        tags = [
            RawTag("test", "whatevs;brainiac"),
        ]

        character = factory.make("Test Mann", tags=tags)

        assert character.tags[1].name == "title"
        assert character.tags[1].value == "brainiac"

    def test_discards_trailing_parts(self, tmp_campaign):
        new_defs = {
            "metatags": {
                "test": {
                    "desc": "A testing tag",
                    "match": ["name", "title"],
                    "separator": ";",
                }
            }
        }
        tmp_campaign.patch_campaign_settings(new_defs)
        factory = CharacterFactory(tmp_campaign)
        tags = [
            RawTag("test", "whatevs;brainiac;something else"),
        ]

        character = factory.make("Test Mann", tags=tags)

        assert len(character.tags) == 2

    def test_adds_second_tag_without_value(self, tmp_campaign):
        new_defs = {
            "metatags": {
                "test": {
                    "desc": "A testing tag",
                    "match": ["name", "title"],
                    "separator": ";",
                }
            }
        }
        tmp_campaign.patch_campaign_settings(new_defs)
        factory = CharacterFactory(tmp_campaign)
        tags = [
            RawTag("test", "whatevs brainiac"),
        ]

        character = factory.make("Test Mann", tags=tags)

        assert character.tags[1].value == ""

    def test_makes_subtags_from_matched_tag(self, tmp_campaign):
        new_defs = {
            "metatags": {
                "test": {
                    "desc": "A testing tag",
                    "match": ["employer", "job"],
                    "separator": ";",
                }
            }
        }
        tmp_campaign.patch_campaign_settings(new_defs)
        factory = CharacterFactory(tmp_campaign)
        tags = [
            RawTag("test", "whatevs brainiac"),
        ]

        character = factory.make("Test Mann", tags=tags)

        assert character.tags[0].subtags[0].name == "job"

    def test_makes_subtags_from_static_tag(self, tmp_campaign):
        new_defs = {
            "metatags": {
                "test": {
                    "desc": "A testing tag",
                    "static": {
                        "employer": "Bear Co."
                    },
                    "match": ["job"],
                }
            }
        }
        tmp_campaign.patch_campaign_settings(new_defs)
        factory = CharacterFactory(tmp_campaign)
        tags = [
            RawTag("test", "Fuzz Inspector"),
        ]

        character = factory.make("Test Mann", tags=tags)

        assert character.tags[0].subtags[0].name == "job"
