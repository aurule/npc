from npc.characters import Tag

def test_includes_name():
    tag = Tag(name="test", value="value")

    result = tag.emit()

    assert "test" in result

def test_includes_value_when_set():
    tag = Tag(name="test", value="value")

    result = tag.emit()

    assert "@test value" == result

def test_exclude_value_when_not_set():
    tag = Tag(name="test")

    result = tag.emit()

    assert "@test" == result

def test_includes_subtags():
    tag = Tag(name="test", value="value")
    tag.subtags = [
        Tag(name="sub1", value="value1"),
        Tag(name="sub2", value="value2"),
    ]

    result = tag.emit()

    assert "sub1" in result
    assert "sub2" in result
