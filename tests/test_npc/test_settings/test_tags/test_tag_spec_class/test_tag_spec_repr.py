import pytest

from npc.settings import TagSpec

def test_includes_tag_name():
    tag_def = {"desc": "A testing tag"}
    tag = TagSpec("test", tag_def)

    assert "test" in repr(tag)

def test_includes_subtag_names():
    tag_def = {"desc": "A testing tag", "subtags": {"with": {"desc": "A subtag"}}}
    tag = TagSpec("test", tag_def)

    assert "with" in repr(tag)
