from npc.settings import Settings

from npc.settings import Metatag

class TestWithSensibleSeparators():
    def test_creates_tag_to_first_sep(self):
        settings = Settings()
        system = settings.get_system("generic")
        metatag_def = {
            "desc": "A testing tag",
            "match": ["name", "title"],
            "separator": ";",
        }
        metatag = Metatag("test", metatag_def)

        result = metatag.expand("whatevs;brainiac", system)

        assert result[0].name == "name"
        assert result[0].value == "whatevs"

    def test_creates_multiple_tags(self):
        settings = Settings()
        system = settings.get_system("generic")
        metatag_def = {
            "desc": "A testing tag",
            "match": ["name", "title"],
            "separator": ";",
        }
        metatag = Metatag("test", metatag_def)

        result = metatag.expand("whatevs;brainiac", system)

        assert result[1].name == "title"

class TestWithExtraParts():
    def test_discards_trailing_parts(self):
        settings = Settings()
        system = settings.get_system("generic")
        metatag_def = {
            "desc": "A testing tag",
            "match": ["name", "title"],
            "separator": ";",
        }
        metatag = Metatag("test", metatag_def)

        result = metatag.expand("whatevs;brainiac;something else", system)

        assert len(result) == 2

class TestWithMissingParts():
    def test_adds_second_tag_without_value(self):
        settings = Settings()
        system = settings.get_system("generic")
        metatag_def = {
            "desc": "A testing tag",
            "match": ["name", "title"],
            "separator": ";",
        }
        metatag = Metatag("test", metatag_def)

        result = metatag.expand("whatevs brainiac", system)

        assert result[1].value == ""

class TestSubtags():
    def test_makes_subtags_from_matched_tag(self):
        settings = Settings()
        system = settings.get_system("generic")
        metatag_def = {
            "desc": "A testing tag",
            "match": ["employer", "job"],
            "separator": ";",
        }
        metatag = Metatag("test", metatag_def)

        result = metatag.expand("whatevs;brainiac", system)

        assert result[1].name == "job"

    def test_makes_subtags_from_static_tag(self):
        settings = Settings()
        system = settings.get_system("generic")
        metatag_def = {
            "desc": "A testing tag",
            "static": {
                "employer": "Bear Co."
            },
            "match": ["job"],
        }
        metatag = Metatag("test", metatag_def)

        result = metatag.expand("Fuzz Inspector", system)

        assert result[1].name == "job"
