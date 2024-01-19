from PySide6.QtWidgets import (
    QDialog, QDialogButtonBox, QFormLayout, QWidget, QLabel, QPushButton,
    QHBoxLayout, QLineEdit, QComboBox, QTextEdit, QVBoxLayout,
    QApplication, QFileDialog
)
from PySide6.QtCore import Qt

from ..models import SystemListModel
from ..widgets.size_policies import *

class NewCampaignDialog(QDialog):
    def __init__(self, campaign_path: str, parent):
        super().__init__(parent=parent)

        self.campaign_path = campaign_path
        self.campaign_name = ""
        self.campaign_system = ""
        self.campaign_desc = ""

        self.setWindowTitle("Create a New Campaign")

        form_lines = QFormLayout()

        # directory display and picker button
        dir_picker_layout = QHBoxLayout()

        dir_label = QLabel("Directory:")
        dir_picker_layout.addWidget(dir_label)

        self.dir_path_label = QLabel(self.campaign_path)
        dir_picker_layout.addWidget(self.dir_path_label)

        dir_choose = QPushButton("&Change...")
        dir_choose.setSizePolicy(fixed_horizontal)
        dir_choose.clicked.connect(self.change_path)
        dir_picker_layout.addWidget(dir_choose)

        form_lines.addRow(dir_picker_layout)

        # name input
        name_input = QLineEdit()
        name_input.textChanged.connect(self.save_name)
        name_input.textChanged.connect(self.ok_check)
        form_lines.addRow("&Name:", name_input)

        # system picker
        systems_model = SystemListModel(parent.settings)
        self.system_picker = QComboBox()
        self.system_picker.setModel(systems_model)
        self.system_picker.setPlaceholderText("Pick a game system")
        self.system_picker.setCurrentIndex(-1)
        self.system_picker.currentIndexChanged.connect(self.save_system)
        self.system_picker.currentIndexChanged.connect(self.ok_check)
        form_lines.addRow("&System:", self.system_picker)

        master_layout = QVBoxLayout(self)
        master_layout.addLayout(form_lines)

        # large description input
        desc_label = QLabel("Description (optional):")
        desc_label.setAlignment(Qt.AlignLeft)
        master_layout.addWidget(desc_label)
        self.desc_input = QTextEdit()
        self.desc_input.textChanged.connect(self.save_desc)
        master_layout.addWidget(self.desc_input)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        buttonBox = QDialogButtonBox(QBtn)
        self.ok_button = buttonBox.button(QDialogButtonBox.Ok)
        self.ok_button.setEnabled(False)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        master_layout.addWidget(buttonBox)

        name_input.setFocus()

    def change_path(self, _checked):
        new_path = QFileDialog.getExistingDirectory(self, "Choose campaign directory")
        if new_path:
            self.campaign_path = new_path
            self.dir_path_label.setText(self.campaign_path)

    def save_name(self, new_name: str):
        self.campaign_name = new_name

    def save_system(self, system_index: int):
        self.campaign_system = self.system_picker.currentData().key

    def save_desc(self):
        self.campaign_desc = self.desc_input.toMarkdown()

    def ok_check(self, *args, **kwargs):
        if self.campaign_name and self.campaign_system:
            self.ok_button.setEnabled(True)
        else:
            self.ok_button.setEnabled(False)
