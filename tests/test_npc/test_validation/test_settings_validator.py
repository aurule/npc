from tests.fixtures import MockSettings

from npc.validation import SettingsValidator

def test_missing_version(tmp_path):
    settings_dir = tmp_path / ".npc"
    settings_dir.mkdir()
    settings_file = settings_dir / "settings.yaml"
    with settings_file.open('w', newline="\n") as f:
        f.write("npc: {tags: {foo: {desc: 'nothing'}}}")

    settings = MockSettings()
    settings.load_settings_file(settings_file, file_key="test")
    validator = SettingsValidator(settings)

    messages = validator.validate()

    assert "missing npc.version" in messages[0].message

def test_redefined_locked_tag(tmp_path):
    settings_dir = tmp_path / ".npc"
    settings_dir.mkdir()
    settings_file = settings_dir / "settings.yaml"
    with settings_file.open('w', newline="\n") as f:
        f.write("npc: {version: '2.0.0', tags: {type: {desc: 'nothing'}}}")

    settings = MockSettings()
    settings.load_settings_file(settings_file, file_key="test")
    validator = SettingsValidator(settings)

    messages = validator.validate()

    assert "is locked" in messages[0].message
