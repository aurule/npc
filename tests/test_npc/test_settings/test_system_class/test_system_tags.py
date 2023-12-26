from npc.settings import Settings, System

def test_includes_global_tags():
    settings = Settings()
    system = settings.get_system("fate")

    tags = system.tags

    assert "type" in tags

def test_includes_system_tags():
    settings = Settings()
    system = settings.get_system("fate")

    tags = system.tags

    assert "concept" in tags
