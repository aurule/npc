import pytest
from tests.fixtures import tmp_campaign, FakeMigration

from ruamel.yaml.scanner import ScannerError

def test_loads_settings_yaml(tmp_campaign):
    migration = FakeMigration(tmp_campaign.settings)

    result = migration.load_settings("campaign")

    assert result.get("npc.version")

def test_aborts_on_missing_folder():
    migration = FakeMigration()

    result = migration.load_settings("campaign")

    assert not result.get("npc.version")

def test_aborts_on_missing_file(tmp_campaign):
    migration = FakeMigration(tmp_campaign.settings)
    tmp_campaign.settings_dir.joinpath("settings.yaml").unlink()

    result = migration.load_settings("campaign")

    assert not result.get("npc.version")

def test_does_not_ignore_parse_errors(tmp_campaign):
    migration = FakeMigration(tmp_campaign.settings)
    with tmp_campaign.settings_dir.joinpath("settings.yaml").open("a") as file:
        file.write("because: %no")

    with pytest.raises(ScannerError):
        result = migration.load_settings("campaign")
