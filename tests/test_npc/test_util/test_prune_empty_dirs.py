from npc.util import prune_empty_dirs

def test_removes_empty_dirs(tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()

    prune_empty_dirs(tmp_path)

    assert not empty.exists()

def test_removes_parents_when_made_empty(tmp_path):
    to_empty = tmp_path / "to_empty"
    to_empty.mkdir()
    nothing = to_empty / "nothing"
    nothing.mkdir()

    prune_empty_dirs(tmp_path)

    assert not to_empty.exists()

def test_leaves_populated_dirs(tmp_path):
    full = tmp_path / "full"
    full.mkdir()
    test_file = full / "test.txt"
    test_file.touch()

    prune_empty_dirs(tmp_path)

    assert full.exists()
