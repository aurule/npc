import pytest
from tests.fixtures import tmp_campaign

from npc.settings import Settings

from npc.settings.migrations.settings_migration import SettingsMigration

class FakeMigration(SettingsMigration):
    def __init__(self, settings: Settings = None):
        if not settings:
            settings = Settings()
        self.settings = settings

    def should_apply(self, file_key: str) -> bool:
        return False

    def migrate(self, file_key: str):
        pass

    @property
    def sequence(self) -> int:
        return 10

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
