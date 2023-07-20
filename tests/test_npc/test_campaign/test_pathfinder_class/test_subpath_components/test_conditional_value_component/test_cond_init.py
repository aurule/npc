import pytest

from npc.campaign.subpath_components import ConditionalValueComponent

def test_stores_tag_names():
    spec = {
        "selector": "first_value",
        "tags": ["brains", "test"],
        "value": "yep",
    }

    comp = ConditionalValueComponent(None, spec, False)

    assert comp.tag_names == spec["tags"]

def test_errors_on_missing_tags():
    spec = {
        "selector": "first_value",
        "xtags": ["brains", "test"],
        "value": "yep",
    }

    with pytest.raises(KeyError):
        comp = ConditionalValueComponent(None, spec, False)

def test_stores_value():
    spec = {
        "selector": "static_value",
        "tags": ["brains", "test"],
        "value": "test",
    }

    comp = ConditionalValueComponent(None, spec, False)

    assert comp._value == spec["value"]

def test_errors_on_missing_value():
    spec = {
        "selector": "first_value",
        "tags": ["brains", "test"],
        "xvalue": "test",
    }

    with pytest.raises(KeyError):
        comp = ConditionalValueComponent(None, spec, False)
