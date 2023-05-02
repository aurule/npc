from npc.settings import Settings

from npc.settings import Metatag

def test_adds_tags():
    settings = Settings()
    system = settings.get_system("generic")
    metatag_def = {
        "desc": "A testing tag",
        "static": {
            "foo": "bar"
        }
    }
    metatag = Metatag("test", metatag_def)

    result = metatag.expand("whatevs", system)

    assert result[0].name == "foo"

def test_preserves_order():
    settings = Settings()
    system = settings.get_system("generic")
    metatag_def = {
        "desc": "A testing tag",
        "static": {
            "foo": "bar",
            "fuzzy": "wuzzy",
        }
    }
    metatag = Metatag("test", metatag_def)

    result = metatag.expand("whatevs", system)

    assert result[0].name == "foo"
    assert result[1].name == "fuzzy"

def test_makes_subtags():
    settings = Settings()
    system = settings.get_system("generic")
    metatag_def = {
        "desc": "A testing tag",
        "static": {
            "employer": "bear",
            "job": "wuzzy",
        }
    }
    metatag = Metatag("test", metatag_def)

    result = metatag.expand("whatevs", system)

    assert result[1].name == "job"
