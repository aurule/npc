from pathlib import Path

from npc.settings.types import TypeSpec

def test_makes_path():
    type_def = {"name": "Test type", "sheet_path": "/dev/null"}
    chartype = TypeSpec("test", type_def)

    assert isinstance(chartype.sheet_path, Path)

def test_safe_on_null():
    type_def = {"name": "Test type"}
    chartype = TypeSpec("test", type_def)

    assert chartype.sheet_path is None
