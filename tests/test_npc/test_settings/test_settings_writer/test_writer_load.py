from npc.settings import SettingsWriter

def test_loads_data(tmp_path):
    test_file = tmp_path / "test.yaml"
    with test_file.open("w") as f:
        f.write("test: true")
    writer = SettingsWriter(test_file)

    writer.load()

    assert writer.get("test") is True
