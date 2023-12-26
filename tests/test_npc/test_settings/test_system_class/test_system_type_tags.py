from npc.settings import Settings, System

def test_includes_global_tags():
    settings = Settings()
    system = settings.get_system("nwod")

    tags = system.type_tags("changeling")

    assert "type" in tags

def test_includes_system_tags():
    settings = Settings()
    system = settings.get_system("fate")

    tags = system.type_tags("supporting")

    assert "concept" in tags

def test_includes_type_tags():
    settings = Settings()
    system = settings.get_system("nwod")

    tags = system.type_tags("changeling")

    assert "motley" in tags
