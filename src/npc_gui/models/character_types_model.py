from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex

class CharacterTypesModel(QAbstractListModel):
    def __init__(self, campaign):
        super().__init__()

        self._data = sorted(list(campaign.types.values()), key=lambda s: str.lower(s.name))

    def data(self, index: QModelIndex, role: int = None):
        type_spec = self._data[index.row()]
        match role:
            case Qt.DisplayRole:
                return type_spec.name
            case Qt.UserRole:
                return type_spec
            case Qt.StatusTipRole:
                return type_spec.desc

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return "Type"

    def rowCount(self, index: QModelIndex = QModelIndex()):
        return len(self._data)
