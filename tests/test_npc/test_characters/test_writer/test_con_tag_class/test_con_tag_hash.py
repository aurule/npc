from npc.characters.writer.con_tag_class import ConTag

def test_changes_on_name():
    tag1 = ConTag("name", "value")
    tag2 = ConTag("other", "value")

    assert tag1.__hash__() != tag2.__hash__()

def test_changes_on_value():
    tag1 = ConTag("name", "value1")
    tag2 = ConTag("name", "value2")

    assert tag1.__hash__() != tag2.__hash__()

def test_matches_on_same_name_value():
    tag1 = ConTag("name", "value")
    tag2 = ConTag("name", "value")

    assert tag1.__hash__() == tag2.__hash__()
