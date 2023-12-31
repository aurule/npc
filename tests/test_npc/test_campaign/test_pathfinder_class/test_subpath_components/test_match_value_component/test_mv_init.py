import pytest

from npc.campaign.subpath_components import MatchValueComponent

def test_stores_tag_names():
    spec = {
        "selector": "first_value",
        "tags": ["brains", "test"],
        "equals": "testing",
        "value": "Test Me",
    }

    comp = MatchValueComponent(None, spec, False)

    assert comp.tag_names == spec["tags"]

def test_errors_on_missing_tags():
    spec = {
        "selector": "first_value",
        "xtags": ["brains", "test"],
        "equals": "testing",
        "value": "Test Me",
    }

    with pytest.raises(KeyError):
        comp = MatchValueComponent(None, spec, False)

def test_errors_on_missing_equals():
    spec = {
        "selector": "first_value",
        "tags": ["brains", "test"],
        "xequals": "testing",
        "value": "Test Me",
    }

    with pytest.raises(KeyError):
        comp = MatchValueComponent(None, spec, False)

def test_errors_on_missing_value():
    spec = {
        "selector": "first_value",
        "tags": ["brains", "test"],
        "equals": "testing",
        "xvalue": "Test Me",
    }

    with pytest.raises(KeyError):
        comp = MatchValueComponent(None, spec, False)
