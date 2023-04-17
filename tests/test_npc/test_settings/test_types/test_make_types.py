from npc.settings.types import make_types

def test_makes_all_types():
    type_defs = {
        "test": {"name": "Test Type"},
        "testier": {"name": "Testing Type"},
    }

    types = make_types(type_defs)

    assert "test" in types
    assert "testier" in types
