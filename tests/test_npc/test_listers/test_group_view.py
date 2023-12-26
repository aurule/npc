from npc.listers.group_view import GroupView

def test_uses_title():
    view = GroupView("test view")

    assert view.title == "test view"

def test_uses_grouping():
    view = GroupView("test view", "blerb")

    assert view.grouping == "blerb"

def test_default_str():
    view = GroupView("test view", "blerb")

    assert str(view) == "test view"
