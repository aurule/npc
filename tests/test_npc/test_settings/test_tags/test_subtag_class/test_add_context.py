import pytest

from npc.settings.tags import SubTag, Tag

def test_adds_the_tag_as_context():
    tag = Tag("test", {"desc": "A test tag"})
    subtag = SubTag("thing")
    context_def = Tag("thing", {"desc": "The thing to test"})

    subtag.add_context("test", context_def)

    assert subtag.contexts.get("test") == context_def

def test_enforces_matching_name():
    tag = Tag("test", {"desc": "A test tag"})
    subtag = SubTag("thing")
    context_def = Tag("other", {"desc": "The thing to test"})

    with pytest.raises(KeyError):
        subtag.add_context("test", context_def)
