from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QDialogButtonBox, QFormLayout, QLabel, QPushButton, QLineEdit, QComboBox,
    QHBoxLayout, QToolButton, QGroupBox, QCheckBox, QTextEdit, QScrollArea,
    QGridLayout
)
from PySide6.QtCore import Qt, QTimer

from npc.campaign import Pathfinder
from npc.characters import CharacterFactory, CharacterWriter
from npc.db import DB, character_repository

from ..models import CharacterTypesModel
from ..helpers import theme_or_resource_icon
from ..widgets import DebounceLineEdit
from ..widgets.size_policies import *

class NewCharacterDialog(QDialog):
    def __init__(self, parent, db: DB = None):
        super().__init__(parent = parent)

        self.campaign = parent.campaign
        self.base_dir = self.campaign.characters_dir

        self.character_type = ""
        self.character_name = ""
        self.character_mnemonic = ""
        self.character_tags = [] # list of RawTag objects
        self.db = db or DB()
        self.pathfinder = Pathfinder(self.campaign)
        self.writer = CharacterWriter(self.campaign, db=db)

        factory = CharacterFactory(self.campaign)
        character = factory.make(
            realname = "",
            type_key = "",
            mnemonic = "",
        )
        with self.db.session() as session:
            session.add(character)
            session.commit()

        self.character_id = character.id

        self.setWindowTitle("Add a New Character")

        self.init_elements()

    def init_elements(self):
        form_lines = QFormLayout()

        # name input
        name_input = DebounceLineEdit()
        name_input.debouncedText.connect(self.save_name)
        form_lines.addRow("&Name:", name_input)

        # mnemonic input
        mnemonic_input = DebounceLineEdit()
        mnemonic_input.debouncedText.connect(self.save_mnemonic)
        form_lines.addRow("&Mnemonic:", mnemonic_input)

        # type picker
        types_model = CharacterTypesModel(self.campaign)
        self.type_picker = QComboBox()
        self.type_picker.setModel(types_model)
        self.type_picker.setPlaceholderText("Pick a character type")
        self.type_picker.setCurrentIndex(-1)
        self.type_picker.currentIndexChanged.connect(self.save_type)
        form_lines.addRow("&Type:", self.type_picker)

        # path label
        self.path_preview = QLabel(" ")
        self.path_preview.setSizePolicy(fixed_vertical)
        form_lines.addRow("Path:", self.path_preview)

        master_layout = QVBoxLayout(self)
        master_layout.addLayout(form_lines)

        # special flags

        flags_box_layout = QHBoxLayout()

        delist_checkbox = QCheckBox("Delist")
        delist_checkbox.setIcon(theme_or_resource_icon("view-hidden"))
        delist_checkbox.setToolTip("Exclude this character from generated listings")
        delist_checkbox.stateChanged.connect(lambda s: self.save_flag("delist", s))
        flags_box_layout.addWidget(delist_checkbox)

        sticky_checkbox = QCheckBox("Sticky")
        sticky_checkbox.setIcon(theme_or_resource_icon("window-pin"))
        sticky_checkbox.setToolTip("Do not automatically move this character's file")
        sticky_checkbox.stateChanged.connect(lambda s: self.save_flag("sticky", s))
        flags_box_layout.addWidget(sticky_checkbox)

        nolint_checkbox = QCheckBox("No Linting")
        nolint_checkbox.setIcon(theme_or_resource_icon("bug"))
        nolint_checkbox.setToolTip("Do not check this character for errors")
        nolint_checkbox.stateChanged.connect(lambda s: self.save_flag("nolint", s))
        flags_box_layout.addWidget(nolint_checkbox)

        flags_box = QGroupBox("Flags")
        flags_box.setLayout(flags_box_layout)
        master_layout.addWidget(flags_box)

        # description input

        desc_label = QLabel("Description:")
        master_layout.addWidget(desc_label)
        self.desc_debounce = QTimer()
        self.desc_debounce.setSingleShot(True)
        self.desc_debounce.setInterval(300)
        desc_input = QTextEdit()
        desc_input.textChanged.connect(self.desc_debounce.start)
        self.desc_debounce.timeout.connect(lambda: self.save_desc(desc_input.toMarkdown()))
        master_layout.addWidget(desc_input)

        # tag management
        tags_label = QLabel("Tags:")
        master_layout.addWidget(tags_label)
        tag_scroller = QScrollArea()
        scroller_layout = QGridLayout()
        tag_scroller.setLayout(scroller_layout)
        master_layout.addWidget(tag_scroller)

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
        scroller_layout.addLayout(tag_line, 0, 0)

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
        scroller_layout.addLayout(new_tag_line, 1, 0)

        # buttons

        QBtn = QDialogButtonBox.Save | QDialogButtonBox.Cancel
        buttonBox = QDialogButtonBox(QBtn)
        self.save_button = buttonBox.button(QDialogButtonBox.Save)
        self.save_button.setEnabled(False)
        buttonBox.accepted.connect(self.write_character_file)
        buttonBox.rejected.connect(self.delete_character_entry)

        master_layout.addWidget(buttonBox)

    def write_character_file(self):
        type_spec = self.campaign.get_type(self.character_type)
        body = type_spec.default_sheet_body()
        self.update_attr("file_body", body)

        query = character_repository.get(self.character_id)
        with self.db.session() as session:
            character = session.scalar(query)
            session.commit()
        self.writer.write(character)

        self.accept()

    def delete_character_entry(self):
        query = character_repository.destroy(self.character_id)
        with self.db.session() as session:
            session.execute(query)
            session.commit()
        self.reject()

    def update_attr(self, attr_name, attr_value):
        query = character_repository.update_attrs_by_id(
            self.character_id,
            {attr_name: attr_value})
        with self.db.session() as session:
            session.execute(query)
            session.commit()

        self.update_path_preview()

    def update_path_preview(self, *args, **kwargs):
        query = character_repository.get(self.character_id)
        with self.db.session() as session:
            character = session.scalar(query)
            session.commit()

        path = self.pathfinder.build_character_path(character)
        filename = self.pathfinder.make_filename(character)
        new_path = path / filename

        if character.file_path == new_path:
            return

        query = character_repository.update_attrs_by_id(
            self.character_id,
            {"file_loc": str(new_path)})
        with self.db.session() as session:
            session.execute(query)
            session.commit()

        self.path_preview.setText(str(new_path.relative_to(self.base_dir)))
        self.path_preview.setToolTip(str(new_path))

    def save_name(self, new_name: str):
        self.update_attr("realname", new_name)
        self.character_name = new_name
        self.ok_check()

    def save_mnemonic(self, new_mnemonic: str):
        self.update_attr("mnemonic", new_mnemonic)
        self.character_mnemonic = new_mnemonic
        self.ok_check()

    def save_type(self, type_index: int):
        self.update_attr("type_key", self.type_picker.currentData().key)
        self.character_type = self.type_picker.currentData().key
        self.ok_check()

    def ok_check(self, *args, **kwargs):
        self.save_button.setEnabled(bool(
            self.character_name \
            and self.character_type \
            and self.character_mnemonic
        ))

    def save_flag(self, flag, state: int):
        self.update_attr(flag, state == Qt.CheckState.Checked.value)

    def save_desc(self, new_desc):
        self.update_attr("desc", new_desc.strip())
