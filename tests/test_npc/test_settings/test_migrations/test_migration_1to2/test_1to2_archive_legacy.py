from tests.fixtures import tmp_campaign

from npc.settings import Settings

from npc.settings.migrations.migration_1to2 import Migration1to2

def test_ignores_legacy_dir_if_nothing_present(tmp_campaign):
    tmp_campaign.settings_file.unlink()
    tmp_campaign.cache_dir.rmdir()
    migration = Migration1to2(tmp_campaign.settings)

    migration.archive_legacy_files("campaign")

    assert not tmp_campaign.settings_dir.joinpath("legacy").exists()

def test_creates_legacy_dir_with_files(tmp_campaign):
    migration = Migration1to2(tmp_campaign.settings)

    migration.archive_legacy_files("campaign")

    assert tmp_campaign.settings_dir.joinpath("legacy").exists()

def test_moves_files(tmp_campaign):
    migration = Migration1to2(tmp_campaign.settings)

    migration.archive_legacy_files("campaign")

    assert tmp_campaign.settings_dir.joinpath("legacy", "settings.yaml").exists()

def test_moves_dirs(tmp_campaign):
    test_dir = tmp_campaign.settings_dir.joinpath("test")
    test_dir.mkdir()
    test_dir.joinpath("file.test").touch()
    migration = Migration1to2(tmp_campaign.settings)

    migration.archive_legacy_files("campaign")

    assert tmp_campaign.settings_dir.joinpath("legacy", "test", "file.test").exists()
