from npc.campaign.subpath_components import get_component

def test_gets_existing_component():
    component = get_component("first_value")

    assert component is not None

def test_returns_none_for_unknown_component():
    component = get_component("nah_brah")

    assert component is None
