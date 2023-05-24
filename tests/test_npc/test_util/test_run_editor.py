from npc.util import run_editor

def test_uses_given_editor():
    result = run_editor("asdf", "testedit", debug=True)

    assert "testedit" in result

def test_defaults_to_system_editor():
    result = run_editor("asdf", debug=True)

    assert "Launch" in result
