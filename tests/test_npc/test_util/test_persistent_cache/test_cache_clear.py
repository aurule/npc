from npc.util import PersistentCache

def test_removes_data(tmp_path):
    test_file = tmp_path / "test.yml"
    cache = PersistentCache(test_file, {"test": True})
    cache.save()

    cache.clear()

    with test_file.open("r") as f:
        contents = f.read()
    assert "test" not in contents
