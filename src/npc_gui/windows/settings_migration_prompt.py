from PySide6.QtWidgets import QMessageBox

import click

from ..helpers import find_settings_file
from npc.settings.migrations import SettingsMigrator

class SettingsMigrationPrompt(QMessageBox):
    def __init__(self, migrator: SettingsMigrator, location: str, parent = None):
        super().__init__(parent)

        self.settings = migrator.settings
        self.location = location

        self.setIcon(QMessageBox.Critical)
        self.setText("Settings Are Out of Date")
        self.setInformativeText(f"Your {location} settings are out of date and need to be migrated. Do you want to migrate now, open the files for manual inspection, or abort?")
        self.setDetailedText(f"") # get from migrator
        migrate_button = self.addButton("Migrate", QMessageBox.AcceptRole)
        browse_button = self.addButton("Browse", QMessageBox.RejectRole)
        browse_button.pressed.connect(self.browse_settings)
        self.addButton(QMessageBox.Abort)
        self.setDefaultButton(migrate_button)

    def browse_settings(self):
        target_file = find_settings_file(self.settings, self.location)
        click.launch(str(target_file), locate=True)
