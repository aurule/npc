from tests.fixtures import fixture_file

from npc.util.legacy import load_json

def test_handles_single_line_comments():
    target = fixture_file("json", "single_comment.json")

    loaded = load_json(target)

    assert loaded["testing"] == "yes"

def test_handles_multi_line_comments():
    target = fixture_file("json", "multi_comment.json")

    loaded = load_json(target)

    assert loaded["testing"] == "yes"

def test_handles_trailing_commas():
    target = fixture_file("json", "trailing_commas.json")

    loaded = load_json(target)

    assert loaded["testing"] == "yes"
