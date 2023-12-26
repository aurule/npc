from npc.settings import Settings, System

def test_rejects_non_system():
    settings = Settings()

    system = settings.get_system("nwod")

    assert system != "nwod"

class TestWithMismatchedData():
    def test_neq_with_same_settings(self):
        settings = Settings()

        system1 = settings.get_system("nwod")
        system2 = settings.get_system("fate")

        assert system1 != system2

    def test_neq_with_different_settings(self):
        settings1 = Settings()
        settings2 = Settings()

        system1 = settings1.get_system("nwod")
        system2 = settings2.get_system("fate")

        assert system1 != system2
