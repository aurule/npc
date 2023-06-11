from npc.settings.tags import TagSpec, UndefinedTagSpec

from npc.settings import Settings, System

def test_includes_global_tags():
    settings = Settings()
    system = settings.get_system("nwod")

    tag = system.get_type_tag("type", "changeling")

    assert isinstance(tag, TagSpec)
    assert tag.name == "type"

def test_includes_system_tags():
    settings = Settings()
    system = settings.get_system("fate")

    tag = system.get_type_tag("concept", "supporting")

    assert isinstance(tag, TagSpec)
    assert tag.name == "concept"

def test_includes_type_tags():
    settings = Settings()
    system = settings.get_system("nwod")

    tag = system.get_type_tag("motley", "changeling")

    assert isinstance(tag, TagSpec)
    assert tag.name == "motley"

def test_gets_obj_for_unknown_tag():
    settings = Settings()
    system = settings.get_system("fate")

    tag = system.get_type_tag("invalid", "supporting")

    assert isinstance(tag, UndefinedTagSpec)
    assert tag.name == "invalid"
