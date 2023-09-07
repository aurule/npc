import pytest
from tests.fixtures import tmp_campaign

from npc.settings import Settings

from npc.settings.migrations.migration_1to2 import Migration1to2

class TestWithModernFile:
    def test_bumps_version(self, tmp_campaign):
        migration = Migration1to2(tmp_campaign.settings)
        migration.update_version("campaign", "1.2.3")

        migration.migrate("campaign")

        data = migration.load_settings("campaign")
        assert data.get("npc.version") == "2.0.0"

class TestWithNoFile:
    def test_creates_minimal_file(self, tmp_campaign):
        tmp_campaign.settings_file.unlink()
        migration = Migration1to2(tmp_campaign.settings)

        migration.migrate("campaign")

        data = migration.load_settings("campaign")
        assert data.get("npc.version") == "2.0.0"

    def test_archives_all_content(self, tmp_campaign):
        tmp_campaign.settings_file.unlink()
        tmp_campaign.settings_dir.joinpath("file.test").touch()
        migration = Migration1to2(tmp_campaign.settings)

        migration.migrate("campaign")

        legacy_file = tmp_campaign.settings_dir.joinpath("legacy", "file.test")
        assert legacy_file.exists()

    def test_does_not_archive_new_file(self, tmp_campaign):
        tmp_campaign.settings_file.unlink()
        migration = Migration1to2(tmp_campaign.settings)

        migration.migrate("campaign")

        assert tmp_campaign.settings_file.exists()

class TestWithLegacyFile:
    @pytest.mark.xfail(reason="Conversion not yet implemented")
    def test_migrates_old_settings(self, tmp_campaign):
        tmp_campaign.settings_file.unlink()
        legacy_settings = tmp_campaign.settings_dir.joinpath("settings.json")
        with legacy_settings.open("w") as f:
            f.write('{"campaign_name": "some old test"}')
        legacy_settings.touch()

        migration = Migration1to2(tmp_campaign.settings)

        data = migration.load_settings("campaign")
        assert data.get("campaign.name") == "some old test"

    def test_archives_all_content(self, tmp_campaign):
        tmp_campaign.settings_file.unlink()
        legacy_settings = tmp_campaign.settings_dir.joinpath("settings.json")
        with legacy_settings.open("w") as f:
            f.write('{"campaign_name": "some old test"}')
        migration = Migration1to2(tmp_campaign.settings)

        migration.migrate("campaign")

        legacy_file = tmp_campaign.settings_dir.joinpath("legacy", "settings.json")
        assert legacy_file.exists()

    def test_does_not_archive_new_file(self, tmp_campaign):
        tmp_campaign.settings_file.unlink()
        legacy_settings = tmp_campaign.settings_dir.joinpath("settings.json")
        with legacy_settings.open("w") as f:
            f.write('{"campaign_name": "some old test"}')
        migration = Migration1to2(tmp_campaign.settings)

        migration.migrate("campaign")

        assert tmp_campaign.settings_file.exists()
