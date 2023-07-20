import pytest

from npc.campaign.subpath_components import StaticValueComponent

def test_stores_value():
    spec = {
        "selector": "static_value",
        "value": "test",
    }

    comp = StaticValueComponent(None, spec, False)

    assert comp._value == spec["value"]

def test_errors_on_missing_value():
    spec = {
        "selector": "first_value",
        "xvalue": "test",
    }

    with pytest.raises(KeyError):
        comp = StaticValueComponent(None, spec, False)
