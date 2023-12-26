from npc_cli.presenters import directory_list

def test_includes_passed_names():
    dirs = ["test", "me", "plz"]

    result = directory_list(dirs)

    assert "test" in result

def test_appends_slash():
    dirs = ["test"]

    result = directory_list(dirs)

    assert "test/" in result
