from PySide6.QtCore import QAbstractListModel, Qt

class SystemListModel(QAbstractListModel):
    def __init__(self, settings):
        super().__init__()

        self._data = [settings.get_system(key) for key in settings.get_system_keys()]

    def data(self, index, role: int):
        match role:
            case Qt.DisplayRole:
                return self._data[index.row()].name
            case Qt.UserRole:
                return self._data[index.row()]

    def headerData(self, section: int, orientation, role: int):
        if role == Qt.DisplayRole:
            return "System"

    def rowCount(self, index: int):
        return len(self._data)
