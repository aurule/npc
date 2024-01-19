import pytest

from npc.campaign.subpath_components import StaticValueComponent

def test_gets_value():
    spec = {
        "selector": "static_value",
        "value": "test",
    }
    comp = StaticValueComponent(None, spec, False)

    result = comp.value(None, None)

    assert result == spec["value"]

def test_uses_fallback():
    spec = {
        "selector": "static_value",
        "value": "test",
        "fallback": "whee",
    }
    comp = StaticValueComponent(None, spec, False)
    comp._value = None

    result = comp.value(None, None)

    assert result == spec["fallback"]
