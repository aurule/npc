import pytest

from tests.fixtures import tmp_campaign, db
from npc.campaign import Campaign

from npc.campaign import Pathfinder

def test_adds_first_value_component(tmp_campaign, db):
    patch = {
        "characters": {
            "subpath_components": [
                {
                    "selector": "first_value",
                    "tags": ["brains", "test"]
                }
            ]
        }
    }
    tmp_campaign.patch_campaign_settings(patch)
    finder = Pathfinder(tmp_campaign, db=db)

    stack = finder.make_component_stack(True)

    assert stack[0].SELECTOR == "first_value"

def test_adds_static_value_component(tmp_campaign, db):
    patch = {
        "characters": {
            "subpath_components": [
                {
                    "selector": "static_value",
                    "value": "brains"
                }
            ]
        }
    }
    tmp_campaign.patch_campaign_settings(patch)
    finder = Pathfinder(tmp_campaign, db=db)

    stack = finder.make_component_stack(True)

    assert stack[0].SELECTOR == "static_value"

def test_adds_conditional_value_component(tmp_campaign, db):
    patch = {
        "characters": {
            "subpath_components": [
                {
                    "selector": "conditional_value",
                    "tags": ["brains", "test"],
                    "value": "sure"
                }
            ]
        }
    }
    tmp_campaign.patch_campaign_settings(patch)
    finder = Pathfinder(tmp_campaign, db=db)

    stack = finder.make_component_stack(True)

    assert stack[0].SELECTOR == "conditional_value"

def test_propagates_exists_option(tmp_campaign, db):
    patch = {
        "characters": {
            "subpath_components": [
                {
                    "selector": "first_value",
                    "tags": ["brains", "test"]
                }
            ]
        }
    }
    tmp_campaign.patch_campaign_settings(patch)
    finder = Pathfinder(tmp_campaign, db=db)

    stack = finder.make_component_stack(True)

    assert stack[0].only_existing is True

def test_throws_error_on_bad_selector(tmp_campaign, db):
    patch = {
        "characters": {
            "subpath_components": [
                {
                    "selector": "nopealope",
                    "tags": ["brains", "test"]
                }
            ]
        }
    }
    tmp_campaign.patch_campaign_settings(patch)
    finder = Pathfinder(tmp_campaign, db=db)

    with pytest.raises(ValueError):
        finder.make_component_stack(True)
