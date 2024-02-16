from npc.util import PersistentCache

def test_saves_data(tmp_path):
    test_file = tmp_path / "test.yml"
    cache = PersistentCache(test_file, {"test": True})

    cache.save()

    with test_file.open("r") as f:
        contents = f.read()
    assert "test" in contents
