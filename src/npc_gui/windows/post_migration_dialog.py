from PySide6.QtWidgets import QMessageBox

class PostMigrationDialog(QMessageBox):
    def __init__(self, location: str, messages: list[str], parent = None):
        super().__init__(parent)

        self.setIcon(QMessageBox.Information)
        self.setText("Settings Updated")
        self.setInformativeText(f"Your {location} settings have been updated.")
        self.setDetailedText("\n".join([m.message for m in messages]))
        self.addButton(QMessageBox.StandardButtons.Ok)
