from npc.characters import Tag

from npc.listers.tag_view_collection import TagViewCollection

def test_joins_tag_views():
    tag1 = Tag(name="test", value="yes")
    tag2 = Tag(name="test", value="very")

    collection = TagViewCollection([tag1, tag2])

    assert str(collection) == "yes, very"

def test_blank_when_empty():
    collection = TagViewCollection()

    assert str(collection) == ""
