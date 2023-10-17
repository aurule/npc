import pytest

from npc.settings.migrations.settings_migration import SettingsMigration

class FakeMigration(SettingsMigration):
    def __init__(self, sequence):
        self.seq: int = sequence

    def should_apply(self, file_key: str) -> bool:
        return False

    def migrate(self, file_key: str):
        pass

    @property
    def sequence(self) -> int:
        return self.seq

def test_compares_sequence():
    settings = Settings()
    migration1 = Migration1to2(settings)
    migration2 = FakeMigration(settings)
    migration2.sequence = 20

    assert migration1 < migration2

def test_not_defined_for_other_objects():
    migration = FakeMigration(10)
    other = dict()

    with pytest.raises(NotImplementedError):
        migration < other
