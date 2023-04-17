from npc.settings import Settings, System

def test_includes_global_tags():
    settings = Settings()
    system = settings.get_system("fate")

    tags = system.tags

    tag_names = [t.name for t in tags]
    assert "type" in tag_names

def test_includes_system_tags():
    settings = Settings()
    system = settings.get_system("fate")

    tags = system.tags

    tag_names = [t.name for t in tags]
    assert "concept" in tag_names
