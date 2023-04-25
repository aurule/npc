import pytest

from npc.settings import TagSpec

def test_raises_on_call():
    tag_def = {"desc": "A testing tag"}
    tag = TagSpec("test", tag_def)

    with pytest.raises(TypeError):
        tag.add_context("parent", {})
