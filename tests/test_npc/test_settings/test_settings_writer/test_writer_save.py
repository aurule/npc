from npc.settings import SettingsWriter

def test_preserves_comments(tmp_path):
    test_file = tmp_path / "test.yaml"
    with test_file.open("w") as f:
        f.write("# hmmm\ntest: true")
    writer = SettingsWriter(test_file)

    writer.load()
    writer.set("test", False)
    writer.save()

    with test_file.open("r") as f:
        contents = f.read()
    assert "hmmm" in contents

def test_writes_changes(tmp_path):
    test_file = tmp_path / "test.yaml"
    with test_file.open("w") as f:
        f.write("# hmmm\ntest: true")
    writer = SettingsWriter(test_file)

    writer.load()
    writer.set("test", False)
    writer.save()

    with test_file.open("r") as f:
        contents = f.read()
    assert "false" in contents
