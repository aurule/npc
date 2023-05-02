from npc.settings import Settings, System

def test_includes_global_metatags():
    settings = Settings()
    settings.data["npc"]["metatags"] = {
        "brewer": {
            "desc": "Brewer at brainz beer",
            "set": {
                "employer": "Brainz"
            },
            "match": [
                "job"
            ]
        }
    }
    system = settings.get_system("nwod")

    tag_defs = system.system_metatag_defs

    assert "brewer" in tag_defs

def test_includes_system_metatags():
    settings = Settings()
    system = settings.get_system("nwod")

    tag_defs = system.system_metatag_defs

    assert "changeling" in tag_defs
