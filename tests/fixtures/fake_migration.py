from npc.settings import Settings
from npc.settings.migrations.settings_migration import SettingsMigration

class FakeMigration(SettingsMigration):
    def __init__(self, settings: Settings = None):
        self.settings = settings or Settings()
        self.sequence = 10

    def should_apply(self, file_key: str) -> bool:
        return False

    def migrate(self, file_key: str):
        pass

    @property
    def sequence(self) -> int:
        return self._sequence

    @sequence.setter
    def sequence(self, val: int):
        self._sequence = val

