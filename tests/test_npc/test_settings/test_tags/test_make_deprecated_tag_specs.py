from npc.settings.tags import make_deprecated_tag_specs

def test_makes_all_deprecated_tags():
    deprecated_tag_defs = {
        "first": {
            "desc": "Don't do it, I'm warning you",
            "version": "2.0.0"
        },
        "second": {
            "desc": "Really, though, don't",
            "version": "2.0.0"
        }
    }

    deprecated_tags = make_deprecated_tag_specs(deprecated_tag_defs)

    assert "first" in deprecated_tags
    assert "second" in deprecated_tags
