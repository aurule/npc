from npc.settings import Settings, System
from npc.settings.tags import TagSpec, UndefinedTagSpec

def test_gets_global_tag():
    settings = Settings()
    system = settings.get_system("fate")

    tag = system.get_tag("type")

    assert isinstance(tag, TagSpec)
    assert tag.name == "type"

def test_gets_system_tag():
    settings = Settings()
    system = settings.get_system("fate")

    tag = system.get_tag("concept")

    assert isinstance(tag, TagSpec)
    assert tag.name == "concept"

def test_gets_obj_for_unknown_tag():
    settings = Settings()
    system = settings.get_system("fate")

    tag = system.get_tag("invalid")

    assert isinstance(tag, UndefinedTagSpec)
    assert tag.name == "invalid"
