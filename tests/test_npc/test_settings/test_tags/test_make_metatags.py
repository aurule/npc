from npc.settings.tags import make_metatags

def test_makes_all_metatags():
    metatag_defs = {
        "first": {
            "desc": "First tag",
            "set": {
                "employer": "Self-employed"
            },
            "match": [
                "job"
            ]
        },
        "second": {
            "desc": "Second tag",
            "set": {
                "employer": "Brainz Beer"
            },
            "match": [
                "job"
            ]
        }
    }
    metatags = make_metatags(metatag_defs)

    assert "first" in metatags
    assert "second" in metatags
