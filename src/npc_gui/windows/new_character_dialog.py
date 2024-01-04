from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QDialogButtonBox, QFormLayout, QLabel, QPushButton, QLineEdit, QComboBox
)

class NewCharacterDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.setWindowTitle("Add a New Character")

        form_lines = QFormLayout()

        # type picker
        self.type_picker = QComboBox()
        self.type_picker.setPlaceholderText("Pick a character type")
        self.type_picker.setCurrentIndex(-1)
        form_lines.addRow("&Type:", self.type_picker)

        # name input
        name_input = QLineEdit()
        form_lines.addRow("&Name:", name_input)

        # mnemonic input
        mnemonic_input = QLineEdit()
        form_lines.addRow("&Mnemonic:", mnemonic_input)

        master_layout = QVBoxLayout(self)
        master_layout.addLayout(form_lines)

        # label showing constructed path within characters path

        tags_label = QLabel("Tags:")
        master_layout.addWidget(tags_label)

        # hbox with tag picker and value input, then small add/plus button
        #   orrrrrr just use the table editing features to add rows
        # small table of tags added so far
        #   each tag name and value is editable

        QBtn = QDialogButtonBox.Save | QDialogButtonBox.Cancel
        buttonBox = QDialogButtonBox(QBtn)
        self.save_button = buttonBox.button(QDialogButtonBox.Save)
        self.save_button.setEnabled(False)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        master_layout.addWidget(buttonBox)
