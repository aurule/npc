from npc.templates.filters import trim_tags

def test_strips_normal_tags():
    value_in = "<p>a test string</p>"

    result = trim_tags(value_in)

    assert result == "a test string"

def test_strips_complex_tags():
    value_in = '<span class="funkytown" style="background-color: white">a test string</span>'

    result = trim_tags(value_in)

    assert result == "a test string"

def test_ignores_tag_matching():
    value_in = "<span>a test string</p>"

    result = trim_tags(value_in)

    assert result == "a test string"

def test_returns_val_on_missing_start_tag():
    value_in = "a test string</p>"

    result = trim_tags(value_in)

    assert result == "a test string</p>"

def test_returns_val_on_missing_end_tag():
    value_in = "<p>a test string"

    result = trim_tags(value_in)

    assert result == "<p>a test string"

def test_returns_val_on_no_tags():
    value_in = "a test string"

    result = trim_tags(value_in)

    assert result == "a test string"
