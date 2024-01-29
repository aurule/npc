from PySide6.QtCore import QAbstractListModel, Qt

from npc.characters import Character

class TagItemsModel(QAbstractListModel):
    def __init__(self, campaign):
        super().__init__()

        excluded_tags = list(Character.MAPPED_TAGS.keys())
        self._data = [campaign.get_tag(tag_name) for tag_name in sorted(campaign.tags.keys()) if tag_name not in excluded_tags]

    def data(self, index, role: int):
        match role:
            case Qt.DisplayRole:
                return self._data[index.row()].name
            case Qt.EditRole:
                return self._data[index.row()].name
            case Qt.UserRole:
                return self._data[index.row()]
            # case Qt.AccessibleDescriptionRole:
            #     return "separator"
            #     to add a fancy separator item

    def headerData(self, section: int, orientation, role: int):
        if role == Qt.DisplayRole:
            return "Type"

    def rowCount(self, index: int):
        return len(self._data)
