from npc.characters import Tag

from npc.views.tag_view import TagView

def test_uses_tag_name():
    tag = Tag(name="test", value="testing", subtags=[])

    view = TagView(tag)

    assert view.name == tag.name

def test_uses_tag_value():
    tag = Tag(name="test", value="testing", subtags=[])

    view = TagView(tag)

    assert view.value == tag.value

def test_adds_attr_for_subtag():
    subtag = Tag(name="when", value="now")
    tag = Tag(name="test", value="testing", subtags=[subtag])

    view = TagView(tag)

    assert hasattr(view, "when")

def test_reuses_subtag_attr():
    subtag1 = Tag(name="when", value="now")
    subtag2 = Tag(name="when", value="right now")
    tag = Tag(name="test", value="testing", subtags=[subtag1, subtag2])

    view = TagView(tag)

    assert hasattr(view, "when")
    assert len(view.when.all()) == 2

def test_default_str_value():
    tag = Tag(name="test", value="testing", subtags=[])

    view = TagView(tag)

    assert str(view) == tag.value

def test_has_true_with_tag():
    subtag = Tag(name="when", value="now")
    tag = Tag(name="test", value="testing", subtags=[subtag])

    view = TagView(tag)

    assert view.has("when")

def test_has_false_without_tag():
    tag = Tag(name="test", value="testing")

    view = TagView(tag)

    assert not view.has("when")
