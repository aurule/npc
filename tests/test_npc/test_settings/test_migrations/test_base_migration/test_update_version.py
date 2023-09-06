from tests.fixtures import tmp_campaign

from npc.settings.migrations.settings_migration import SettingsMigration

class FakeMigration(SettingsMigration):
    def __init__(self, settings):
        self.settings = settings

    def should_apply(self, file_key: str) -> bool:
        return False

    def migrate(self, file_key: str):
        pass

    @property
    def sequence(self) -> int:
        return 10

def test_overwrites_version(tmp_campaign):
    migration = FakeMigration(tmp_campaign.settings)

    migration.update_version("campaign", "2.3.4")

    data = migration.load_settings("campaign")
    assert data.get("npc.version") == "2.3.4"
