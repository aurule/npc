from npc.settings import Settings, System

def test_changes_on_key():
    settings = Settings()

    system1 = settings.get_system("nwod")
    system2 = settings.get_system("nwod")
    system2.key = "nope"

    assert system1.__hash__() != system2.__hash__()

def test_changes_on_data():
    settings = Settings()

    system1 = settings.get_system("nwod")
    system2 = settings.get_system("nwod")
    system2.name = "Nope"

    assert system1.__hash__() != system2.__hash__()

def test_changes_on_settings():
    settings1 = Settings()
    settings2 = Settings()

    system1 = settings1.get_system("nwod")
    system2 = settings2.get_system("nwod")

    assert system1.__hash__() != system2.__hash__()
