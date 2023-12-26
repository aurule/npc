from npc.characters import Tag

from npc.listers.tag_view_collection import TagViewCollection

def test_returns_first_tag_view():
    tag1 = Tag(name="test", value="yes")
    tag2 = Tag(name="test", value="yes")
    tags = [tag1, tag2]
    collection = TagViewCollection(tags)

    first_view = collection.first()

    assert (first_view.name, first_view.value) == (tag1.name, tag1.value)
