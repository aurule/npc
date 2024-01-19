from PySide6.QtCore import QAbstractListModel, Qt

class CharacterTypesModel(QAbstractListModel):
    def __init__(self, campaign):
        super().__init__()

        self._data = [campaign.get_type(key) for key in campaign.types]

    def data(self, index, role: int):
        match role:
            case Qt.DisplayRole:
                return self._data[index.row()].name
            case Qt.UserRole:
                return self._data[index.row()]

    def headerData(self, section: int, orientation, role: int):
        if role == Qt.DisplayRole:
            return "Type"

    def rowCount(self, index: int):
        return len(self._data)
