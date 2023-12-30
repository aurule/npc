from PySide6.QtCore import QAbstractTableModel, Qt

class CharactersTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        # accept a collection of CharacterView objects
        # accept a list of tag names
        # header strings are tag names with basic capitalization and pluralization
        #   cache header strings on init and bust if tags are changed
        # use characterview.get(), a new method, to pick correct data for each cell
        self._headers = ["Name", "Mnemonic", "Type"]
        self._data = [
            ["Bro Mann", "cool guy", "mundane"],
        ]

    def data(self, index: int, role: int):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def headerData(self, section: int, orientation, role: int):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]

            if orientation == Qt.Vertical:
                return section

    def rowCount(self, index: int):
        return len(self._data)

    def columnCount(self, index: int):
        return len(self._data[0])
