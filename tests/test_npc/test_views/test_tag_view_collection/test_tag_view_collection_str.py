from npc.characters import Tag

from npc.views.tag_view_collection import TagViewCollection

def test_uses_first_tag_value():
    tag1 = Tag(name="test", value="yes")
    tag2 = Tag(name="test", value="very")

    collection = TagViewCollection([tag1, tag2])

    assert str(collection) == "yes"

def test_blank_when_empty():
    collection = TagViewCollection()

    assert str(collection) == ""
