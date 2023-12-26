import pytest

from npc.campaign.subpath_components import FirstValueComponent

def test_stores_tag_names():
    spec = {
        "selector": "first_value",
        "tags": ["brains", "test"]
    }

    comp = FirstValueComponent(None, spec, False)

    assert comp.tag_names == spec["tags"]

def test_errors_on_missing_tags():
    spec = {
        "selector": "first_value",
        "xtags": ["brains", "test"]
    }

    with pytest.raises(KeyError):
        comp = FirstValueComponent(None, spec, False)
