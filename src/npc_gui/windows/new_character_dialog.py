from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QDialogButtonBox, QFormLayout, QLabel, QPushButton, QLineEdit, QComboBox,
    QHBoxLayout, QToolButton
)
from PySide6.QtCore import Qt

from ..helpers import theme_or_resource_icon
from ..widgets.size_policies import *

class NewCharacterDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.character_type = ""
        self.character_name = ""
        self.character_mnemonic = ""
        self.charcter_tags = [] # list of RawTag objects

        # tag defs view

        self.setWindowTitle("Add a New Character")

        form_lines = QFormLayout()

        # type picker
        self.type_picker = QComboBox()
        self.type_picker.setPlaceholderText("Pick a character type")
        self.type_picker.setCurrentIndex(-1)
        form_lines.addRow("&Type:", self.type_picker)

        # name input
        self.name_input = QLineEdit()
        form_lines.addRow("&Name:", self.name_input)

        # mnemonic input
        self.mnemonic_input = QLineEdit()
        form_lines.addRow("&Mnemonic:", self.mnemonic_input)

        # path label
        self.path_preview = QLabel("Characters/Test Mann - testy boi.npc")
        self.path_preview.setSizePolicy(fixed_vertical)
        form_lines.addRow("Path:", self.path_preview)

        master_layout = QVBoxLayout(self)
        master_layout.addLayout(form_lines)

        tags_label = QLabel("Tags:")
        tags_label.setSizePolicy(fixed_vertical)
        master_layout.addWidget(tags_label)

        # need a scrolling area
        # either a standalone scroll area, or a flat group box

        new_tag_line = QHBoxLayout()
        tag_name_picker = QComboBox() # allow custom input
        tag_name_picker.setPlaceholderText("Tag name")
        tag_name_picker.setCurrentIndex(-1)
        tag_name_picker.setEditable(True)
        tag_name_picker.setSizePolicy(fixed_horizontal)
        new_tag_line.addWidget(tag_name_picker)
        tag_value_entry = QLineEdit()
        new_tag_line.addWidget(tag_value_entry)
        new_tag_btn = QToolButton()
        new_tag_btn.setSizePolicy(fixed_horizontal)
        new_tag_btn.setIcon(theme_or_resource_icon("list-add"))
        new_tag_btn.setToolButtonStyle(Qt.ToolButtonIconOnly)
        new_tag_btn.setToolTip("Add tag")
        new_tag_line.addWidget(new_tag_btn)
        master_layout.addLayout(new_tag_line)

        QBtn = QDialogButtonBox.Save | QDialogButtonBox.Cancel
        buttonBox = QDialogButtonBox(QBtn)
        self.save_button = buttonBox.button(QDialogButtonBox.Save)
        self.save_button.setEnabled(False)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        master_layout.addWidget(buttonBox)
