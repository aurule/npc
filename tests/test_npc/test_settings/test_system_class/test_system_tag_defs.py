from npc.settings import Settings, System

def test_includes_global_tags():
    settings = Settings()
    system = settings.get_system("fate")

    tag_defs = system.system_tag_defs

    assert "type" in tag_defs

def test_includes_system_tags():
    settings = Settings()
    system = settings.get_system("fate")

    tag_defs = system.system_tag_defs

    assert "concept" in tag_defs
