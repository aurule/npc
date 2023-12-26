from npc.settings import Settings, System

def test_rejects_non_system():
    settings = Settings()

    system = settings.get_system("nwod")

    assert system != "nwod"

class TestWithMatchingData():
    def test_eq_with_same_settings(self):
        settings = Settings()

        system1 = settings.get_system("nwod")
        system2 = settings.get_system("nwod")

        assert system1 == system2
