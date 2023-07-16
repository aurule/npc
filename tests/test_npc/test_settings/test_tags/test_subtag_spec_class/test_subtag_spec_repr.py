import pytest

from npc.settings.tags import SubTagSpec, TagSpec

def test_includes_tag_name():
    subtag = SubTagSpec("thing")

    assert "thing" in repr(subtag)

def test_includes_contexts():
    tag = TagSpec("test", {"desc": "A test tag"})
    subtag = SubTagSpec("thing")
    context_def = TagSpec("thing", {"desc": "The thing to test"})

    subtag.add_context("test", context_def)

    assert "test" in repr(subtag)
