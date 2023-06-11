from npc_cli.presenters import tag_table_data
from npc.settings import Settings

def test_shows_tags():
    settings = Settings()
    system = settings.get_system("generic")

    tag_names = [row[0] for row in tag_table_data(system.tags)]

    assert "org" in tag_names

def test_shows_first_subtags():
    settings = Settings()
    system = settings.get_system("generic")

    tag_names = [row[0] for row in tag_table_data(system.tags)]

    assert "\u2514 rank" in tag_names
