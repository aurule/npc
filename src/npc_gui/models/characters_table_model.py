from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
from functools import cache

from npc.campaign import CharacterCollection
from npc.characters import Character
from npc.listers import CharacterView

class CharactersTableModel(QAbstractTableModel):
    def __init__(self, collection: CharacterCollection, tag_names: list[str]):
        super().__init__()

        self.set_tag_names(tag_names)

        self.collection = collection

        self.views = [CharacterView(c) for c in collection.all()]

    def data(self, index, role: int):
        if role == Qt.DisplayRole:
            view = self.views[index.row()]
            tag = self.tag_names[index.column()]
            if view.has(tag):
                return view.first(tag)

    def headerData(self, section: int, orientation, role: int):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]

            if orientation == Qt.Vertical:
                return section

    def rowCount(self, _index=None):
        return self.collection.count

    def columnCount(self, _index=None):
        return len(self._headers)

    def set_tag_names(self, tag_names: list[str]):
        self.tag_names = tag_names
        self._headers = self.header_names()

    def header_names(self) -> list[str]:
        return [n.capitalize() for n in self.tag_names]

    def sort(self, column, order):
        def comparator(character):
            tag = self.tag_names[column]
            return character.first(tag)

        reverse = order == Qt.DescendingOrder
        self.views = sorted(self.views, key=comparator, reverse=reverse)

        # trigger a redraw
        topleft = self.index(0,0)
        botright = self.index(self.rowCount(), self.columnCount())
        self.dataChanged.emit(topleft, botright)
