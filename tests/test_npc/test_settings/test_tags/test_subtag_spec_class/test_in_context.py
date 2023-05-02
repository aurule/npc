import pytest

from npc.settings.tags import SubTagSpec, TagSpec

def test_returns_existing_context_by_key():
    tag = TagSpec("test", {"desc": "A test tag"})
    subtag = SubTagSpec("thing")
    context_def = TagSpec("thing", {"desc": "The thing to test"})

    subtag.add_context("test", context_def)

    assert subtag.in_context("test").desc == context_def.desc

def test_returns_none_on_unknown_context_key():
    subtag = SubTagSpec("thing")

    assert subtag.in_context("nope") is None

def test_returns_default_if_given_on_unknown_context_key():
    subtag = SubTagSpec("thing")

    assert subtag.in_context("nope", "ohno") is "ohno"
