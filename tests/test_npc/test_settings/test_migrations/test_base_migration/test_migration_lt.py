import pytest

from npc.settings import Settings
from npc.settings.migrations.migration_1to2 import Migration1to2

from tests.fixtures import FakeMigration

def test_compares_sequence():
    settings = Settings()
    migration1 = Migration1to2(settings)
    migration2 = FakeMigration(settings)
    migration2.sequence = 20

    assert migration1 < migration2

def test_not_defined_for_other_objects():
    migration = FakeMigration()
    migration.sequence = 10
    other = dict()

    with pytest.raises(NotImplementedError):
        migration < other
