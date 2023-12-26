from pathlib import Path

from npc.settings.types import TypeSpec

def test_includes_key():
    type_def = {"name": "Test Type", "sheet_path": "/dev/null/test.test"}
    chartype = TypeSpec("test", type_def)

    result = repr(chartype)

    assert "key='test'" in result

def test_includes_name():
    type_def = {"name": "Test Type", "sheet_path": "/dev/null/test.test"}
    chartype = TypeSpec("test", type_def)

    result = repr(chartype)

    assert "name='Test Type'" in result
