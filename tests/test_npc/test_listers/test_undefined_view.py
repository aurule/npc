from npc.listers.undefined_view import UndefinedView

def test_has_always_false():
    view = UndefinedView()

    result = view.has("thing")

    assert result is False

def test_first_always_self():
    view = UndefinedView()

    result = view.first()

    assert result is view

def test_all_always_self():
    view = UndefinedView()

    result = view.all()

    assert result is view

def test_rest_always_self():
    view = UndefinedView()

    result = view.rest()

    assert result is view
