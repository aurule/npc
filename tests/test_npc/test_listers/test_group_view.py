from npc.listers.group_view import GroupView

def test_uses_title():
    view = GroupView("test view")

    assert view.title == "test view"
