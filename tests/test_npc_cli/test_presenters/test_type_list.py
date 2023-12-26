from npc_cli.presenters import type_list

def test_includes_passed_types():
    types = {"a": {}, "b": {}}

    result = type_list(types)

    assert "a" in result
    assert "b" in result

def test_wraps_keys_in_quotes():
    types = {"a": {}, "b": {}}

    result = type_list(types)

    assert "'a'" in result

def test_separates_by_comma():
    types = {"a": {}, "b": {}}

    result = type_list(types)

    assert "'a'," in result
