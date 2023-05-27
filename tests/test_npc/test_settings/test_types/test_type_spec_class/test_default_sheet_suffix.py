from pathlib import Path

from npc.settings.types import TypeSpec

def test_inherits_from_sheet():
    type_def = {"name": "Test type", "sheet_path": "/dev/null/test.test"}
    chartype = TypeSpec("test", type_def)

    assert chartype.default_sheet_suffix == ".test"

def test_defaults_to_npc():
    type_def = {"name": "Test type"}
    chartype = TypeSpec("test", type_def)

    assert chartype.default_sheet_suffix == ".npc"
