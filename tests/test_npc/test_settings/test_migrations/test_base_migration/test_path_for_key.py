import pytest

from tests.fixtures import FakeMigration

def test_gets_saved_path(tmp_path):
    migration = FakeMigration()
    key = "test"
    migration.settings.loaded_paths[key] = tmp_path

    result = migration.path_for_key(key)

    assert result == tmp_path

def test_returns_none_when_no_path():
    migration = FakeMigration()
    key = "test"

    result = migration.path_for_key(key)

    assert result is None
