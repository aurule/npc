from pathlib import Path
from tests.fixtures import tmp_campaign, change_cwd
from npc.settings import Settings

from npc_cli.helpers import find_or_make_settings_file

def test_aborts_on_bad_location_type():
    result = find_or_make_settings_file(None, "test")

    assert result is None

def test_user_gets_user_settings(tmp_path):
    settings = Settings(personal_dir=tmp_path)

    result = find_or_make_settings_file(settings, "user")

    assert result == str(settings.personal_dir / "settings.yaml")

class TestCampaignLocation():
    def test_without_campaign_returns_null(self, tmp_path):
        settings = Settings(personal_dir=tmp_path)

        result = find_or_make_settings_file(settings, "campaign")

        assert result is None

    def test_gets_campaign_file(self, tmp_campaign):
        with change_cwd(tmp_campaign.root):
            result = find_or_make_settings_file(tmp_campaign.settings, "campaign")

            assert result == str(tmp_campaign.settings_file)

class TestTargetFileDoesNotExist():
    def test_creates_file(self, tmp_path):
        settings = Settings(personal_dir=tmp_path/"test")

        result = find_or_make_settings_file(settings, "user")

        assert Path(result).exists()
