from npc.characters.writer.con_tag_class import ConTag

def test_rejects_non_contag():
    tag = ConTag("name", "value")

    assert tag != "name value"

def test_true_with_same_name_value():
    tag1 = ConTag("name", "value")
    tag2 = ConTag("name", "value")

    assert tag1 == tag2
