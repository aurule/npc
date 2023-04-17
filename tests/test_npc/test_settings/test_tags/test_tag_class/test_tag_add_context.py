import pytest

from npc.settings import Tag

def test_raises_on_call():
    tag_def = {"desc": "A testing tag"}
    tag = Tag("test", tag_def)

    with pytest.raises(TypeError):
        tag.add_context("parent", {})
