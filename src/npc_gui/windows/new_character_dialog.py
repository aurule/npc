from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QDialogButtonBox, QFormLayout, QLabel, QPushButton, QLineEdit, QComboBox,
    QHBoxLayout, QGroupBox, QCheckBox, QTextEdit, QScrollArea, QGridLayout, QToolButton
)
from PySide6.QtCore import Qt, QTimer, QSize

from npc.campaign import Pathfinder
from npc.characters import CharacterFactory, CharacterWriter
from npc.db import DB, character_repository

from ..models import CharacterTypesModel
from ..helpers import fetch_icon
from ..widgets import DebounceLineEdit, TagTreeView
from ..widgets.size_policies import *

class NewCharacterDialog(QDialog):
    def __init__(self, parent, db: DB = None):
        super().__init__(parent = parent)

        self.campaign = parent.campaign
        self.base_dir = self.campaign.characters_dir

        self.character_type = ""
        self.character_name = ""
        self.character_mnemonic = ""
        self.db = db or DB()
        self.pathfinder = Pathfinder(self.campaign)
        self.writer = CharacterWriter(self.campaign, db=db)

        factory = CharacterFactory(self.campaign)
        self.character = factory.make(
            realname = "",
            type_key = "",
            mnemonic = "",
        )
        with self.db.session() as session:
            session.add(self.character)
            session.commit()

        self.character_id = self.character.id

        self.setWindowTitle("Add a New Character")

        self.init_elements()

    def init_elements(self):
        master_layout = QGridLayout(self)

        left_form = QFormLayout()
        left_form.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        name_input = DebounceLineEdit()
        name_input.debouncedText.connect(self.save_name)
        left_form.addRow("&Name:", name_input)

        types_model = CharacterTypesModel(self.campaign)
        self.type_picker = QComboBox()
        self.type_picker.setModel(types_model)
        self.type_picker.setPlaceholderText("Pick a character type")
        self.type_picker.setCurrentIndex(-1)
        self.type_picker.currentIndexChanged.connect(self.save_type)
        left_form.addRow("&Type:", self.type_picker)

        self.type_detail = QLabel()
        self.type_detail.setWordWrap(True)
        left_form.addRow(self.type_detail)

        master_layout.addLayout(left_form, 0, 0)


        right_form = QFormLayout()
        right_form.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        mnemonic_input = DebounceLineEdit()
        mnemonic_input.debouncedText.connect(self.save_mnemonic)
        right_form.addRow("&Mnemonic:", mnemonic_input)


        flags_box_layout = QHBoxLayout()

        delist_checkbox = QCheckBox("Delist")
        delist_checkbox.setIcon(fetch_icon("hide_table_column"))
        delist_checkbox.setToolTip("Exclude this character from generated listings")
        delist_checkbox.stateChanged.connect(lambda s: self.save_flag("delist", s))
        flags_box_layout.addWidget(delist_checkbox)

        sticky_checkbox = QCheckBox("Sticky")
        sticky_checkbox.setIcon(fetch_icon("window-pin"))
        sticky_checkbox.setToolTip("Do not automatically move this character's file")
        sticky_checkbox.stateChanged.connect(lambda s: self.save_flag("sticky", s))
        flags_box_layout.addWidget(sticky_checkbox)

        nolint_checkbox = QCheckBox("No Linting")
        nolint_checkbox.setIcon(fetch_icon("bug"))
        nolint_checkbox.setToolTip("Do not check this character for errors")
        nolint_checkbox.stateChanged.connect(lambda s: self.save_flag("nolint", s))
        flags_box_layout.addWidget(nolint_checkbox)

        flags_box = QGroupBox("Flags")
        flags_box.setLayout(flags_box_layout)
        # master_layout.addWidget(flags_box, 1, 1, 2, 1)
        right_form.addRow(flags_box)
        master_layout.addLayout(right_form, 0, 1)


        path_pair = QHBoxLayout()
        path_label = QLabel("Path:")
        self.path_preview = QLabel(" ")
        self.path_preview.setSizePolicy(fixed_vertical)
        path_pair.addWidget(path_label)
        path_pair.addWidget(self.path_preview)
        master_layout.addLayout(path_pair, 1, 0, 1, -1)


        desc_pair = QVBoxLayout()
        desc_label = QLabel("Description:")
        self.desc_debounce = QTimer()
        self.desc_debounce.setSingleShot(True)
        self.desc_debounce.setInterval(300)
        desc_input = QTextEdit()
        desc_input.textChanged.connect(self.desc_debounce.start)
        self.desc_debounce.timeout.connect(lambda: self.save_desc(desc_input.toMarkdown()))
        desc_pair.addWidget(desc_label)
        desc_pair.addWidget(desc_input)
        master_layout.addLayout(desc_pair, 3, 0)


        tags_pair = QVBoxLayout()
        tags_label_line = QHBoxLayout()
        tags_label = QLabel("Tags:")
        tags_label_line.addWidget(tags_label)
        tag_add = QToolButton()
        tag_add.setIconSize(QSize(8, 8))
        tag_add.setSizePolicy(fixed_horizontal)
        tag_add.setIcon(fetch_icon("list-add"))
        tag_add.setToolButtonStyle(Qt.ToolButtonIconOnly)
        tags_label_line.addWidget(tag_add)
        tags_pair.addLayout(tags_label_line)

        tag_tree = TagTreeView(self.character_id, db=self.db)
        tag_add.pressed.connect(tag_tree.insert_row)
        tags_pair.addWidget(tag_tree)
        master_layout.addLayout(tags_pair, 3, 1)


        QBtn = QDialogButtonBox.Save | QDialogButtonBox.Cancel
        buttonBox = QDialogButtonBox(QBtn)
        self.save_button = buttonBox.button(QDialogButtonBox.Save)
        self.save_button.setEnabled(False)
        buttonBox.accepted.connect(self.write_character_file)
        buttonBox.rejected.connect(self.delete_character_entry)

        master_layout.addWidget(buttonBox, 4, 0, 1, -1)

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
        type_spec = self.type_picker.currentData()
        self.update_attr("type_key", type_spec.key)
        self.character_type = type_spec.key
        self.type_detail.setText(type_spec.desc)
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
