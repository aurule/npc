from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex

from npc.settings import Settings

class SystemListModel(QAbstractListModel):
    def __init__(self, settings: Settings):
        super().__init__()

        self._data = sorted(settings.systems, key=lambda s: str.lower(s.name))

    def data(self, index: QModelIndex, role: int = None):
        match role:
            case Qt.DisplayRole:
                return self._data[index.row()].name
            case Qt.UserRole:
                return self._data[index.row()]

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return "System"

    def rowCount(self, index: QModelIndex = QModelIndex()):
        return len(self._data)
