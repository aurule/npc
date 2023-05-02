from npc.settings import Settings

from npc.settings import Metatag

class TestWithMatchingValues():
    def test_creates_tag(self):
        settings = Settings()
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

        settings.merge_data(new_defs, "npc.systems.generic")
        system = settings.get_system("generic")
        metatag = system.metatags["test"]

        result = metatag.expand("first", system)

        assert result[0].name == "single"
        assert result[0].value == "first"

    def test_uses_first_match(self):
        settings = Settings()
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

        settings.merge_data(new_defs, "npc.systems.generic")
        system = settings.get_system("generic")
        metatag = system.metatags["test"]

        result = metatag.expand("firstest", system)

        assert result[0].name == "multi"
        assert result[0].value == "first"

    def test_drops_extra_values(self):
        settings = Settings()
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

        settings.merge_data(new_defs, "npc.systems.generic")
        system = settings.get_system("generic")
        metatag = system.metatags["test"]

        result = metatag.expand("first and then more", system)

        assert result[0].name == "single"
        assert result[0].value == "first"

    def test_ignores_separator(self):
        settings = Settings()
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

        settings.merge_data(new_defs, "npc.systems.generic")
        system = settings.get_system("generic")
        metatag = system.metatags["test"]

        result = metatag.expand("first last", system)

        assert result[0].name == "multi"
        assert result[0].value == "first last"

class TestWithNoMatch():
    def test_uses_separator(self):
        settings = Settings()
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

        settings.merge_data(new_defs, "npc.systems.generic")
        system = settings.get_system("generic")
        metatag = system.metatags["test"]

        result = metatag.expand("something else", system)

        assert result[0].name == "single"
        assert result[0].value == "something"

class TestNesting():
    def test_uses_subtag_values(self):
        settings = Settings()
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

        settings.merge_data(new_defs, "npc.systems.generic")
        system = settings.get_system("generic")
        metatag = system.metatags["test"]

        result = metatag.expand("first last alope", system)
        print(result)

        assert result[0].name == "multi"
        assert result[0].value == "first last"

        assert result[1].name == "single"
        assert result[1].value == "alope"
