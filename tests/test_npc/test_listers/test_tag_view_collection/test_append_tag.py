from npc.characters import Tag

from npc.listers.tag_view_collection import TagViewCollection

def test_saves_corresponding_tag_view():
    tag = Tag(name="test", value="yes")
    collection = TagViewCollection()

    collection.append_tag(tag)

    assert collection.tag_views[0].value == tag.value
