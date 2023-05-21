import pytest
from npc.characters import Character

from npc.characters.writer.helpers import make_contags

def test_makes_type():
    character = Character(type_key="human", id=1, realname="test mann", file_loc="/dev/null")

    result = make_contags(character)

    assert "type" in result
    assert result["type"].value == "human"

def test_makes_realname_when_needed():
    character = Character(id=1, realname="test mann", file_loc="/dev/null/nope.npc")

    result = make_contags(character)

    assert "realname" in result
    assert result["realname"].value == "test mann"

def test_does_not_make_realname_when_not_needed():
    character = Character(id=1, realname="test mann", file_loc="/dev/null/test mann.npc")

    result = make_contags(character)

    assert "realname" not in result

@pytest.mark.parametrize("tag_name", ["sticky", "nolint", "delist"])
def test_makes_flags(tag_name):
    args = {tag_name: True}
    character = Character(file_loc="/dev/null", realname="test mann", **args)

    result = make_contags(character)

    assert tag_name in result
