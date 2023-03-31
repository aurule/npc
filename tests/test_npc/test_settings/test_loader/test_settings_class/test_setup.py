import yaml

from npc.settings import Settings

def test_loads_default_settings():
    settings = Settings()

    assert settings.get("npc.version") != ""

def test_loads_personal_settings(tmp_path):
    personal_settings = {"npc": {"editor": "custom"}}
    temp_file = tmp_path / "settings.yaml"
    temp_file.write_text(yaml.dump(personal_settings))

    settings = Settings(personal_dir = tmp_path)

    assert settings.get("npc.editor") == "custom"

def test_saves_campaign_path(tmp_path):
    settings = Settings(campaign_dir = tmp_path)

    assert settings.campaign_dir == tmp_path
