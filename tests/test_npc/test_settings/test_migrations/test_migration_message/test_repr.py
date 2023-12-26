from npc.settings.migrations.migration_message import MigrationMessage

def test_includes_message():
    migme = MigrationMessage("howdy")

    result = repr(migme)

    assert "howdy" in result

def test_includes_file():
    migme = MigrationMessage("howdy", file="ohno")

    result = repr(migme)

    assert "ohno" in result

def test_includes_key():
    migme = MigrationMessage("howdy", key="whoops.a.daisy")

    result = repr(migme)

    assert "whoops.a.daisy" in result
