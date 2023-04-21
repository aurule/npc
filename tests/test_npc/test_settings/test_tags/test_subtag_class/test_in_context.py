import pytest

from npc.settings.tags import SubTag, Tag

def test_returns_existing_context_by_key():
    tag = Tag("test", {"desc": "A test tag"})
    subtag = SubTag("thing")
    context_def = Tag("thing", {"desc": "The thing to test"})

    subtag.add_context("test", context_def)

    assert subtag.in_context("test").desc == context_def.desc

def test_returns_none_on_unknown_context_key():
    subtag = SubTag("thing")

    assert subtag.in_context("nope") is None
