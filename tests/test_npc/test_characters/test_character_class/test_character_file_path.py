from pathlib import Path
from npc.characters import Character

def test_sets_from_path(tmp_path):
    char = Character(id=5, realname="Test Mann", type_key="generic")

    char.file_path = tmp_path / "test mann.npc"

    assert "test mann.npc" in char.file_loc

def test_reads_to_path(tmp_path):
    char = Character(id=5, realname="Test Mann", type_key="generic")
    char.file_loc = str(tmp_path / "test mann.npc")

    assert isinstance(char.file_path, Path)
