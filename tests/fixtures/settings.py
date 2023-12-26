from npc.settings import Settings

class MockSettings(Settings):
    """Settings variant for testing

    This settings class only loads the internal settings files and *not* the
    user settings. This is most important for the migration tests, which by
    design can modify settings files. It's also helpful for avoiding any
    potential test disruption from tag changes in the testing user's settings.
    """
    def refresh(self) -> None:
        self.data = {}
        self.load_settings_file(self.default_settings_path / "settings.yaml", file_key="internal")
        self.load_systems(self.default_settings_path / "systems")
