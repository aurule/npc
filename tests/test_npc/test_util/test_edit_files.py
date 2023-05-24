from npc.settings import Settings

from npc.util import edit_files

def test_uses_editor_from_settings(tmp_path):
    settings = Settings()
    settings.merge_data({"npc": {"editor": "testedit"}})
    file = tmp_path / "test.txt"
    file.touch()

    result = edit_files([file], settings = settings, debug = True)

    assert "testedit" in result[0]

def test_includes_all_files_with_custom_editor(tmp_path):
    settings = Settings()
    settings.merge_data({"npc": {"editor": "testedit"}})
    file1 = tmp_path / "test1.txt"
    file1.touch()
    file2 = tmp_path / "test2.txt"
    file2.touch()

    result = edit_files([file1, file2], settings=settings, debug = True)

    assert "test1.txt" in result[0]
    assert "test2.txt" in result[1]

def test_defaults_to_system_editor(tmp_path):
    file = tmp_path / "test.txt"
    file.touch()

    result = edit_files([file], debug = True)

    assert "Launching" in result[0]

def test_includes_all_files_with_system_editor(tmp_path):
    file1 = tmp_path / "test1.txt"
    file1.touch()
    file2 = tmp_path / "test2.txt"
    file2.touch()

    result = edit_files([file1, file2], debug = True)

    assert "test1.txt" in result[0]
    assert "test2.txt" in result[1]
