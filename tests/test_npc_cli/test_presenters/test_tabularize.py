from npc_cli.presenters import tabularize

def test_inserts_title():
    table = tabularize([[]], [], title = "Test Title")

    assert "[Test Title]" in table

def test_includes_headers():
    table = tabularize([("a", "b")], ("Test", "Header"))

    assert "Header" in table

def test_shows_data():
    table = tabularize([("first", "second")], ("Test", "Header"))

    assert "first" in table

def test_shows_int_data():
    table = tabularize([(1, "second")], ("Test", "Header"))

    assert "1" in table
