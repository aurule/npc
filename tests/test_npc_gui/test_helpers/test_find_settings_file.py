from tests.fixtures import tmp_campaign, change_cwd, MockSettings

from npc_gui.helpers import find_settings_file

def test_aborts_on_bad_location_type():
    result = find_settings_file(None, "test")

    assert result is None

class TestUserLocation():
    def test_without_user_settings_returns_none(self, tmp_path):
        settings = MockSettings(personal_dir=tmp_path)

        result = find_settings_file(settings, "user")

        assert result is None

    def test_gets_user_file(self, tmp_path):
        settings = MockSettings(personal_dir=tmp_path)
        tmp_path.joinpath("settings.yaml").touch()

        result = find_settings_file(settings, "user")

        assert result == str(settings.personal_dir / "settings.yaml")

class TestCampaignLocation():
    def test_without_campaign_returns_none(self, tmp_path):
        settings = MockSettings()

        result = find_settings_file(settings, "campaign")

        assert result is None

    def test_gets_campaign_file(self, tmp_campaign):
        with change_cwd(tmp_campaign.root):
            result = find_settings_file(tmp_campaign.settings, "campaign")

            assert result == str(tmp_campaign.settings_file)
