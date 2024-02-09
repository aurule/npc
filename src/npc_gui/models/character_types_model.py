from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex

class CharacterTypesModel(QAbstractListModel):
    def __init__(self, campaign):
        super().__init__()

        self._data = list(campaign.types.values())

    def data(self, index: QModelIndex, role: int = None):
        match role:
            case Qt.DisplayRole:
                return self._data[index.row()].name
            case Qt.UserRole:
                return self._data[index.row()]

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return "Type"

    def rowCount(self, index: QModelIndex = QModelIndex()):
        return len(self._data)
