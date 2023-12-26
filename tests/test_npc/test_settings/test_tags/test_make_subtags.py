from npc.settings.tags import make_tags

tag_defs = {
    "first": {
        "desc": "First tag",
        "subtags": {
            "primero": {
                "desc": "First of firsts"
            },
            "segundo": {
                "desc": "Second of firsts",
                "subtags": {
                    "tercero": {
                        "desc": "First of seconds"
                    }
                }
            }
        }
    }
}

def test_flattens_subtags():
    tags = make_tags(tag_defs)

    assert "primero" in tags.keys()

def test_makes_all_subtags():
    tags = make_tags(tag_defs)

    assert "primero" in tags.keys()
    assert "segundo" in tags.keys()
    assert "tercero" in tags.keys()

def test_adds_context():
    tags = make_tags(tag_defs)

    assert "first" in tags.get("primero").contexts

def test_adds_deep_subtags():
    tags = make_tags(tag_defs)

    assert "tercero" in tags.keys()
