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

    metatags = system.metatags

    assert "brewer" in metatags

def test_includes_system_metatags():
    settings = Settings()
    system = settings.get_system("nwod")

    metatags = system.metatags

    assert "changeling" in metatags
