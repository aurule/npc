import pytest
from npc.util.win_sanitize import win_sanitize

@pytest.mark.parametrize("unsafe", ['\\', '/', ':', '*', '?', '"', '<', '>', '|'])
def test_replaces_unsafe_characters(unsafe):
    raw = f"Test string {unsafe}"

    result = win_sanitize(raw)

    assert result == "Test string _"
