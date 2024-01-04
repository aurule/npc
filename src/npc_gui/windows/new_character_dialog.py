from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QDialogButtonBox
)

class NewCharacterDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.setWindowTitle("Add a New Character")

        master_layout = QVBoxLayout(self)

        QBtn = QDialogButtonBox.Save | QDialogButtonBox.Cancel
        buttonBox = QDialogButtonBox(QBtn)
        self.save_button = buttonBox.button(QDialogButtonBox.Save)
        self.save_button.setEnabled(False)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        master_layout.addWidget(buttonBox)
