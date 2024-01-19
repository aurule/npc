import pytest

from npc.campaign.subpath_components import StaticValueComponent

def test_gets_existing_key():
    spec = {
        "selector": "static_value",
        "value": "test",
    }
    comp = StaticValueComponent(None, spec, False)

    result = comp.from_spec("value")

    assert result == spec["value"]

def test_raises_on_missing_key():
    spec = {
        "selector": "first_value",
        "value": "test",
    }
    comp = StaticValueComponent(None, spec, False)

    with pytest.raises(KeyError):
        result = comp.from_spec("nope")
