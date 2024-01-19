from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QDialogButtonBox, QFormLayout, QLabel, QPushButton, QLineEdit, QComboBox,
    QHBoxLayout, QToolButton, QGroupBox
)
from PySide6.QtCore import Qt, QTimer

from npc.campaign import Pathfinder
from npc.characters import CharacterFactory
from npc.db import DB, character_repository

from ..models import CharacterTypesModel
from ..helpers import theme_or_resource_icon
from ..widgets.size_policies import *

class NewCharacterDialog(QDialog):
    def __init__(self, parent, db: DB = None):
        super().__init__(parent = parent)

        self.character_type = ""
        self.character_name = ""
        self.character_mnemonic = ""
        self.character_tags = [] # list of RawTag objects
        self.db = db or DB()
        self.pathfinder = Pathfinder(parent.campaign)

        factory = CharacterFactory(parent.campaign)
        character = factory.make(
            realname = "placeholder",
            type_key = "placeholder",
            mnemonic = "placeholder",
        )
        with self.db.session() as session:
            session.add(character)
            session.commit()

        self.character_id = character.id

        # create and insert new character into db with placeholders
        # update those values in save methods
        # on accept, write the file
        # on reject, delete the db entry

        self.setWindowTitle("Add a New Character")

        form_lines = QFormLayout()

        # type picker
        types_model = CharacterTypesModel(parent.campaign)
        self.type_picker = QComboBox()
        self.type_picker.setModel(types_model)
        self.type_picker.setPlaceholderText("Pick a character type")
        self.type_picker.setCurrentIndex(-1)
        self.type_picker.currentIndexChanged.connect(self.save_type)
        form_lines.addRow("&Type:", self.type_picker)

        # name input
        self.name_debounce = QTimer()
        self.name_debounce.setInterval(500)
        self.name_debounce.setSingleShot(True)
        self.name_debounce.timeout.connect(self.save_name)
        self.name_input = QLineEdit()
        self.name_input.textChanged.connect(self.name_debounce.start)
        form_lines.addRow("&Name:", self.name_input)

        # mnemonic input
        mnemonic_input = QLineEdit()
        mnemonic_input.textChanged.connect(self.save_mnemonic)
        mnemonic_input.textChanged.connect(self.ok_check)
        mnemonic_input.textChanged.connect(self.update_path)
        form_lines.addRow("&Mnemonic:", mnemonic_input)

        # path label
        self.path_preview = QLabel("Characters/Test Mann - testy boi.npc")
        self.path_preview.setSizePolicy(fixed_vertical)
        form_lines.addRow("Path:", self.path_preview)

        # box for flags: sticky, nolint, delist

        master_layout = QVBoxLayout(self)
        master_layout.addLayout(form_lines)

        # tag management
        tag_box = QGroupBox("Tags")
        tag_box.setFlat(True)
        tag_box_layout = QVBoxLayout()
        tag_box.setLayout(tag_box_layout)
        master_layout.addWidget(tag_box)

        # need a scrolling area

        tag_line = QHBoxLayout()
        picker = QComboBox()
        picker.setPlaceholderText("Tag name")
        picker.setCurrentIndex(-1)
        picker.setEditable(True)
        picker.setSizePolicy(fixed_horizontal)
        tag_line.addWidget(picker)
        value = QLineEdit()
        tag_line.addWidget(value)
        menu_btn = QToolButton()
        menu_btn.setSizePolicy(fixed_horizontal)
        menu_btn.setIcon(theme_or_resource_icon("menu-more"))
        menu_btn.setToolButtonStyle(Qt.ToolButtonIconOnly)
        menu_btn.setToolTip("Tag actions...")
        tag_line.addWidget(menu_btn)
        tag_box_layout.addLayout(tag_line)

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
        tag_box_layout.addLayout(new_tag_line)

        # description input

        QBtn = QDialogButtonBox.Save | QDialogButtonBox.Cancel
        buttonBox = QDialogButtonBox(QBtn)
        self.save_button = buttonBox.button(QDialogButtonBox.Save)
        self.save_button.setEnabled(False)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        master_layout.addWidget(buttonBox)

    def save_name(self):
        new_name = self.name_input.text()
        query = character_repository.update_attrs_by_id(self.character_id, {"realname": new_name})

        with self.db.session() as session:
            session.execute(query)
            session.commit()

        self.character_name = new_name
        self.ok_check()
        self.update_path()

    def save_mnemonic(self, new_mnemonic: str):
        self.character_mnemonic = new_mnemonic

    def save_type(self, type_index: int):
        self.character_type = self.type_picker.currentData().key
        self.ok_check()
        self.update_path()

    def ok_check(self, *args, **kwargs):
        self.save_button.setEnabled(bool(
            self.character_name \
            and self.character_type \
            and self.character_mnemonic
        ))

    def update_path(self, *args, **kwargs):
        query = character_repository.get(self.character_id)
        with self.db.session() as session:
            character = session.scalar(query)
            session.commit()

        path = self.pathfinder.build_character_path(character)
        print(path)
        # use pathfinder to build a new path string
