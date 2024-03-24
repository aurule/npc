from PySide6.QtWidgets import QMessageBox

class NoCampaignDialog(QMessageBox):
    def __init__(self, campaign_path: str, parent = None):
        super().__init__(parent)

        self.setIcon(QMessageBox.Critical)
        self.setText("No Campaign")
        self.setInformativeText(f"The folder {campaign_path} is not an NPC campaign, nor are any of its parent directories.")
        self.addButton(QMessageBox.Ok)
        self.setDefaultButton(QMessageBox.Ok)
