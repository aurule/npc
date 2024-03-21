from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl

from npc.settings import Settings

class SettingsOutdatedDialog(QMessageBox):
    def __init__(self, settings: Settings, location: str, parent = None):
        super().__init__(parent)

        package_version = settings.versions.get("package")
        file_version = settings.versions.get(location)

        self.setIcon(QMessageBox.Warning)
        self.setText("NPC is Outdated")
        self.setInformativeText(f"The installed version of NPC ({package_version}) is older than the one which last updated your {location} settings ({file_version}). Because of this, NPC may behave incorrectly.\n\nDo you want to download the latest release?")
        self.addButton(QMessageBox.StandardButtons.Yes)
        self.addButton(QMessageBox.StandardButtons.No)
        self.setDefaultButton(QMessageBox.StandardButtons.Yes)

        self.accepted.connect(self.open_release_webpage)

    def open_release_webpage(self):
        QDesktopServices.openUrl(QUrl("https://github.com/aurule/npc/releases/latest"))
