from PySide6.QtWidgets import (
    QTableView, QAbstractItemView, QHeaderView
)
from PySide6.QtCore import Qt

from ..models import CharactersTableModel

class ResourceTable(QTableView):
    def __init__(self, resources, tags: list[str], parent = None):
        super().__init__(parent)

        self.resources = resources
        self.tags = tags

        self.model = CharactersTableModel(
            resources,
            tags
        )
        self.setModel(self.model)

        self.verticalHeader().hide()
        self.setCornerButtonEnabled(False)
        self.setSortingEnabled(True)
        self.sortByColumn(0, Qt.AscendingOrder)
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
