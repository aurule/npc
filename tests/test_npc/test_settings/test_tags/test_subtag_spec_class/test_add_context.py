import pytest

from npc.settings.tags import SubTagSpec, TagSpec

def test_adds_the_tag_as_context():
    tag = TagSpec("test", {"desc": "A test tag"})
    subtag = SubTagSpec("thing")
    context_def = TagSpec("thing", {"desc": "The thing to test"})

    subtag.add_context("test", context_def)

    assert subtag.contexts.get("test") == context_def

def test_enforces_matching_name():
    tag = TagSpec("test", {"desc": "A test tag"})
    subtag = SubTagSpec("thing")
    context_def = TagSpec("other", {"desc": "The thing to test"})

    with pytest.raises(KeyError):
        subtag.add_context("test", context_def)
