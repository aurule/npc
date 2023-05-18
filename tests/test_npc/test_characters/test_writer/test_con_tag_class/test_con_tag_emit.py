from npc.characters.writer.con_tag_class import ConTag

def test_includes_name():
    tag = ConTag("name", "value")

    result = tag.emit()

    assert "name" in result

def test_includes_value_when_set():
    tag = ConTag("name", "value")

    result = tag.emit()

    assert "@name value" == result

def test_exclude_value_when_not_set():
    tag = ConTag("name")

    result = tag.emit()

    assert "@name" == result
