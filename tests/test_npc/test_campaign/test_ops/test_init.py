import yaml

from npc.campaign import init
from npc.settings import Settings

class TestSettingsFile:
    campaign_name = "Test Campaign"
    campaign_system = "fate"
    campaign_desc = "A test campaign for testing"

    def test_creates_settings_file(self, tmp_path):
        init(tmp_path, name = self.campaign_name, system = self.campaign_system)

        settings_file = tmp_path / ".npc" / "settings.yaml"

        assert settings_file.exists()

    def test_includes_name(self, tmp_path):
        init(tmp_path, name = self.campaign_name, system = self.campaign_system)

        settings_file = tmp_path / ".npc" / "settings.yaml"
        with settings_file.open("r") as f:
            settings_contents = yaml.safe_load(f)

        assert settings_contents["campaign"]["name"] == self.campaign_name

    def test_includes_system(self, tmp_path):
        init(tmp_path, name = self.campaign_name, system = self.campaign_system)

        settings_file = tmp_path / ".npc" / "settings.yaml"
        with settings_file.open("r") as f:
            settings_contents = yaml.safe_load(f)

        assert settings_contents["campaign"]["system"] == self.campaign_system

    def test_omits_empty_desc(self, tmp_path):
        init(tmp_path, name = self.campaign_name, system = self.campaign_system)

        settings_file = tmp_path / ".npc" / "settings.yaml"
        with settings_file.open("r") as f:
            settings_contents = yaml.safe_load(f)

        assert "desc" not in settings_contents["campaign"]

    def test_includes_filled_desc(self, tmp_path):
        init(tmp_path, name = self.campaign_name, system = self.campaign_system, desc = self.campaign_desc)

        settings_file = tmp_path / ".npc" / "settings.yaml"
        with settings_file.open("r") as f:
            settings_contents = yaml.safe_load(f)

        assert settings_contents["campaign"]["desc"] == self.campaign_desc

def test_creates_settings_object_when_none_supplied(tmp_path):
    settings = init(tmp_path, name = "test", system = "fate")

    assert isinstance(settings, Settings)

def test_updates_settings_obj(tmp_path):
    settings = Settings()

    returned_settings = init(tmp_path, name = "test", system = "fate", settings = settings)

    assert "name" in settings.get("campaign")

def test_creates_required_dirs(tmp_path):
    settings = Settings()

    init(tmp_path, name = "test", system = "fate", settings = settings)

    for dirname in settings.required_dirs:
        assert tmp_path.joinpath(dirname).exists()

def test_creates_optional_dirs(tmp_path):
    settings = Settings()
    optional_dirs = settings.get("campaign.create_on_init")
    optional_dirs.append("hello")

    init(tmp_path, name = "test", system = "fate", settings = settings)

    for dirname in settings.init_dirs:
        assert tmp_path.joinpath(dirname).exists()
