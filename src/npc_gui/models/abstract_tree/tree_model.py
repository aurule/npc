from PySide6.QtCore import (
    QModelIndex, Qt, QAbstractItemModel
)

from .tree_item import TreeItem

class TreeModel(QAbstractItemModel):
    """Abstract class for modeling tree data

    This model assumes that the root item is the container for header data. As
    such, subclasses should correctly populate root_item to reflect their header
    labels.
    """
    def __init__(self, parent = None):
        super().__init__(parent)

        self.root_item = None

    def insertRows(self, position: int, rows: int, parent: QModelIndex = QModelIndex()) -> bool:
        """Insert one or more rows into the parent's children

        This calls the parent item's own insert_children method, so position
        will be relative to the number of child items the parent reports.

        Args:
            position (int): Position within the parent's children to add the rows
            rows (int): Number of rows to add
            parent (QModelIndex): Index of the parent item (default: `QModelIndex()`)

        Returns:
            bool: True if the rows were inserted, False if not
        """
        parent_item: TreeItem = self.get_item(parent)
        if not parent_item:
            return False

        self.beginInsertRows(parent, position, position + rows - 1)
        success: bool = parent_item.insert_children(position, rows)
        self.endInsertRows()

        return success

    def removeRows(self, position: int, rows: int, parent: QModelIndex = QModelIndex()) -> bool:
        """Remove one or more rows from the given parent's children

        This calls the parent item's own remove_children method, so position
        will be relative to the number of child items the parent reports.

        Args:
            position (int): Position within the parent's children to begin removing items
            rows (int): Number of rows to remove
            parent (QModelIndex): Index of the parent item (default: `QModelIndex()`)

        Returns:
            bool: True if the rows were removed, False if not
        """
        parent_item: TreeItem = self.get_item(parent)
        if not parent_item:
            return False

        self.beginRemoveRows(parent, position, position + rows - 1)
        success: bool = parent_item.remove_children(position, rows)
        self.endRemoveRows()

        return success

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.root_item.data(section)

        return None

    def data(self, index: QModelIndex, role: int = None):
        if not index.isValid():
            return None

        return self.get_item(index).data(index.column(), role)

    def columnCount(self, parent: QModelIndex = None) -> int:
        return self.root_item.column_count()

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEditable | QAbstractItemModel.flags(self, index)

    def get_item(self, index: QModelIndex = QModelIndex()) -> TreeItem:
        if index.isValid():
            item: TreeItem = index.internalPointer()
            if item:
                return item

        return self.root_item

    def index(self, row: int, column: int, parent: QModelIndex = QModelIndex()) -> QModelIndex:
        if parent.isValid() and parent.column() != 0:
            return QModelIndex()

        parent_item: TreeItem = self.get_item(parent)
        if not parent_item:
            return QModelIndex()

        child_item: TreeItem = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)

        return QModelIndex()

    def parent(self, index: QModelIndex = QModelIndex()) -> QModelIndex:
        if not index.isValid():
            return QModelIndex()

        child_item: TreeItem = self.get_item(index)
        if child_item:
            parent_item: TreeItem = child_item.parent()
        else:
            parent_item = None

        if parent_item == self.root_item or not parent_item:
            return QModelIndex()

        return self.createIndex(parent_item.child_number(), 0, parent_item)

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid() and parent.column() > 0:
            return 0

        parent_item: TreeItem = self.get_item(parent)
        if not parent_item:
            return 0
        return parent_item.child_count()

    def setData(self, index: QModelIndex, value, role: int) -> bool:
        if role != Qt.EditRole:
            return False

        item: TreeItem = self.get_item(index)
        result: bool = item.set_data(index.column(), value)

        if result:
            self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])

        return result

    def _repr_recursion(self, item: TreeItem, indent: int = 0) -> str:
        result = " " * indent + repr(item) + "\n"
        for child in item.child_items:
            result += self._repr_recursion(child, indent + 2)
        return result

    def __repr__(self) -> str:
        return self._repr_recursion(self.root_item)
