import pytest

from npc.settings import SettingsWriter

def test_throws_not_implemented(tmp_path):
    test_file = tmp_path / "test.yaml"
    with test_file.open("w") as f:
        f.write("test: true")
    writer = SettingsWriter(test_file)

    with pytest.raises(NotImplementedError):
        writer.merge_data()
