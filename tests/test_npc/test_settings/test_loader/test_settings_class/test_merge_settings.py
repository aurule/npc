from npc.settings import Settings

def test_adds_new_values():
    settings = Settings()
    new_vars = {"npc": {"editor": "hello"}}

    settings.merge_settings(new_vars)

    assert settings.get("npc.editor") == "hello"

def test_merges_into_namespace():
    settings = Settings()
    new_vars = {"editor": "hello"}

    settings.merge_settings(new_vars, namespace = "npc")

    assert settings.get("npc.editor") == "hello"
