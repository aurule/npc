from npc.characters import Tag

from npc.listers.tag_view_collection import TagViewCollection

def test_returns_tag_views_after_first():
    tag1 = Tag(name="test", value="yes")
    tag2 = Tag(name="test", value="yes")
    tags = [tag1, tag2]
    collection = TagViewCollection(tags)

    remaining_views = collection.rest()

    assert [(v.name, v.value) for v in remaining_views] == [(tag2.name, tag2.value)]
