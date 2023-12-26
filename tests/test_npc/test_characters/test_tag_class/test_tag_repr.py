from npc.characters import Tag

def test_includes_id():
    tag = Tag(id=5, name="test", value="test")

    result = repr(tag)

    assert str(tag.id) in result

def test_includes_name():
    tag = Tag(id=5, name="test", value="test")

    result = repr(tag)

    assert tag.name in result

def test_includes_value():
    tag = Tag(id=5, name="test", value="test")

    result = repr(tag)

    assert tag.value in result

def test_includes_hidden():
    tag = Tag(id=5, name="test", value="test", hidden=True)

    result = repr(tag)

    assert "hidden=True" in result
