import yaml

from npc.settings import Settings

def test_purges_changed_values():
    settings = Settings()
    settings.data["npc"]["editor"] = "test"

    settings.refresh()

    assert settings.get("npc.editor") is None

def test_updates_personal_settings(tmp_path):
    settings = Settings(personal_dir = tmp_path)

    assert settings.get("npc.editor") is None

    personal_settings = {"npc": {"editor": "custom"}}
    temp_file = tmp_path / "settings.yaml"
    temp_file.write_text(yaml.dump(personal_settings))

    settings.refresh()

    assert settings.get("npc.editor") == "custom"
