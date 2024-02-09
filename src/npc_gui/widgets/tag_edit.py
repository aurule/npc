from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QComboBox, QCompleter, QToolButton
)
from PySide6.QtCore import Qt

from npc.db import DB
from ..models import TagNameItemsModel
from ..helpers import theme_or_resource_icon
from .size_policies import *
from .debounce_line_edit import DebounceLineEdit

class TagEdit(QWidget):
    def __init__(self, tag_id: int, parent_widget=None, db: DB = None):
        super().__init__(parent_widget)

        self.db = db or DB()
        self.tag_id = tag_id

        self.init_widgets()

    def init_widgets(self):
        self.container = QHBoxLayout(self)

        tags_model = TagNameItemsModel(parent.campaign)
        picker = QComboBox()
        picker.setModel(tags_model)
        picker.setCurrentIndex(-1)
        picker.setEditable(True)
        picker.lineEdit().setPlaceholderText("Tag name")
        picker.setSizePolicy(fixed_horizontal)
        # picker.changed.connect(self.save_name)
        tag_completer = QCompleter(tags_model, picker)
        tag_completer.setCaseSensitivity(Qt.CaseInsensitive)
        tag_completer.setCompletionMode(QCompleter.InlineCompletion)
        picker.setCompleter(tag_completer)
        self.container.addWidget(picker)
        value_input = DebounceLineEdit()
        # value_input.debouncedText.connect(self.save_value)
        self.container.addWidget(value_input)
        menu_btn = QToolButton()
        menu_btn.setSizePolicy(fixed_horizontal)
        menu_btn.setIcon(theme_or_resource_icon("menu-more"))
        menu_btn.setToolButtonStyle(Qt.ToolButtonIconOnly)
        menu_btn.setToolTip("Tag actions...")
        self.container.addWidget(menu_btn)
