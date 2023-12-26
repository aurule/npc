from npc.util import arg_or_default

def test_returns_truthy_var():
    var = "yes"
    default = "default"

    result = arg_or_default(var, default)

    assert result == var

def test_returns_default_on_falsey_var():
    var = ""
    default = "default"

    result = arg_or_default(var, default)

    assert result == default

def test_returns_default_on_none_var():
    var = None
    default = "default"

    result = arg_or_default(var, default)

    assert result == default
