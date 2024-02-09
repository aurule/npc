from PySide6.QtWidgets import (
    QTreeView, QAbstractItemView
)

from PySide6.QtCore import Qt

from npc.db import DB
from ..models import TagTreeModel

class TagTreeView(QTreeView):
    def __init__(self, taggable_type: str, taggable_id: int, db: DB = None, parent = None):
        super().__init__(parent)

        self.taggable_type = taggable_type
        self.taggable_id = taggable_id

        self.model = TagTreeModel(taggable_type, taggable_id, db)
        self.setModel(self.model)

        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setAnimated(False)
