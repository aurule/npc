import pytest
from tests.fixtures import tmp_campaign

from npc.settings import Settings
from npc.util.errors import ParseError

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

def test_adds_new_keys(tmp_campaign):
    migration = FakeMigration(tmp_campaign.settings)
    data = {"npc": {"test": "very yes"}}
    migration.write_settings("campaign", data)

    migration.refresh_settings("campaign")

    assert migration.settings.get("npc.test") == "very yes"
