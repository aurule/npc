from npc.settings import MetatagSpec

def test_includes_statics():
    metatag_def = {
        "desc": "A testing tag",
        "static": {
            "test": "yes"
        },
        "match": ["brains"]
    }
    metatag = MetatagSpec("metatest", metatag_def)

    assert "test" in metatag.required_tag_names

def test_includes_matches():
    metatag_def = {
        "desc": "A testing tag",
        "static": {
            "test": "yes"
        },
        "match": ["brains"]
    }
    metatag = MetatagSpec("metatest", metatag_def)

    assert "brains" in metatag.required_tag_names
