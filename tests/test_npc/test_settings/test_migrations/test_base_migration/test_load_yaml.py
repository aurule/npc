import pytest
from tests.fixtures import tmp_campaign

from npc.settings import Settings

from npc.settings.migrations.settings_migration import SettingsMigration

class FakeMigration(SettingsMigration):
    def __init__(self, settings: Settings = None):
        self.settings = settings or Settings()

    def should_apply(self, file_key: str) -> bool:
        return False

    def migrate(self, file_key: str):
        pass

    @property
    def sequence(self) -> int:
        return 10

def test_loads_settings_yaml(tmp_campaign):
    migration = FakeMigration(tmp_campaign.settings)
    pass

def test_aborts_on_missing_file(tmp_campaign):
    pass

def test_does_not_ignore_parse_errors(tmp_campaign):
    pass
