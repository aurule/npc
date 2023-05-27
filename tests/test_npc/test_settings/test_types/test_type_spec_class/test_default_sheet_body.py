from tests.fixtures import fixture_file

from npc.settings.types import TypeSpec

def test_provides_fallback():
    type_def = {"name": "Test type"}
    chartype = TypeSpec("test", type_def)

    result = chartype.default_sheet_body()

    assert result == "--Notes--"

def test_gets_sheet_contents():
    type_def = {"name": "Test type", "sheet_path": str(fixture_file("sheets", "test.npc"))}
    chartype = TypeSpec("test", type_def)

    result = chartype.default_sheet_body()

    assert "testing your code" in result
