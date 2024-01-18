from npc.characters import Tag

from npc.views.tag_view_collection import TagViewCollection

def test_returns_tag_views_list():
    tag1 = Tag(name="test", value="yes")
    tag2 = Tag(name="test", value="yes")
    tags = [tag1, tag2]
    collection = TagViewCollection(tags)

    all_views = collection.all()

    assert [(v.name, v.value) for v in all_views] == [(t.name, t.value) for t in tags]
