from PySide6.QtCore import QAbstractListModel, Qt

from npc.characters import Character

class TagItemsModel(QAbstractListModel):
    def __init__(self, campaign):
        super().__init__()

        mapped_tags = set(Character.MAPPED_TAGS.keys())
        def valid_tag(tag_spec):
            return (
                tag_spec.name not in mapped_tags
                and not tag_spec.long
                and not tag_spec.replaced_by
                and not tag_spec.needs_context
            )

        self._data = sorted([spec for spec in campaign.tags.values() if valid_tag(spec)], key=lambda s: str.lower(s.name))

    def data(self, index, role: int):
        match role:
            case Qt.DisplayRole:
                return self._data[index.row()].name
            case Qt.EditRole:
                return self._data[index.row()].name
            case Qt.UserRole:
                return self._data[index.row()]

    def headerData(self, section: int, orientation, role: int):
        if role == Qt.DisplayRole:
            return "Type"

    def rowCount(self, index: int):
        return len(self._data)
