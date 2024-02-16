import yaml

from npc.util import PersistentCache

def test_with_file_gets_data(tmp_path):
    test_file = tmp_path / "test.yml"
    with test_file.open("w", newline="\n") as f:
        yaml.dump({"test": True}, f)
    cache = PersistentCache(test_file)

    cache.load()

    assert cache.get("test") is True

def test_with_file_replaces_data(tmp_path):
    test_file = tmp_path / "test.yml"
    with test_file.open("w", newline="\n") as f:
        yaml.dump({"test": True}, f)
    cache = PersistentCache(test_file, {"test": False})

    cache.load()

    assert cache.get("test") is True

def test_without_file_erases_data(tmp_path):
    test_file = tmp_path / "test.yml"
    cache = PersistentCache(test_file, {"test": False})

    cache.load()

    assert cache.get("test") is None
