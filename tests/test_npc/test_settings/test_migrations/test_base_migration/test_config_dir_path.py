import pytest
from tests.fixtures import tmp_campaign, FakeMigration

def test_gets_user_dir():
    migration = FakeMigration()

    result = migration.config_dir_path("user")

    assert result == migration.settings.personal_dir

def test_gets_campaign_dir(tmp_campaign):
    migration = FakeMigration(tmp_campaign.settings)

    result = migration.config_dir_path("campaign")

    assert result == tmp_campaign.settings_dir

def test_none_for_others():
    migration = FakeMigration()

    result = migration.config_dir_path("other")

    assert result is None
