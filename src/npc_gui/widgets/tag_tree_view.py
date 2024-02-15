from PySide6.QtWidgets import (
    QTreeView, QAbstractItemView
)

from PySide6.QtCore import Qt

from npc.db import DB
from ..models import TagTreeModel

class TagTreeView(QTreeView):
    def __init__(self, character_id: int, db: DB = None, parent = None):
        super().__init__(parent)

        self.character_id = character_id

        self.tag_tree_model = TagTreeModel(character_id, db)
        self.setModel(self.tag_tree_model)

        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setAnimated(False)

    def insert_row(self):
        index: QModelIndex = self.selectionModel().currentIndex()
        model: QAbstractItemModel = self.model()
        parent: QModelIndex = index.parent()

        if not model.insertRow(index.row() + 1, parent):
            return
