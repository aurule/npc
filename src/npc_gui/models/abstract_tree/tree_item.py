from abc import ABC, abstractmethod

class TreeItem(ABC):
    """Abstract class for a row in a tree view
    """
    def __init__(self, parent: "TreeItem" = None):
        self.parent_item = parent
        self.child_items = []
        self.item_data = []

    @abstractmethod
    def data(self, column: int):
        """Get the data for this item at the given column

        Args:
            column (int): Column number to get data for

        Returns:
            any: The data at the given column, or None if there is no available data
        """

    @abstractmethod
    def insert_children(self, position: int, count: int) -> bool:
        """Insert new child items starting at the given position

        This method must create one or more new tree items, each with empty
        data, and insert them into self.child_items starting at the given index.

        Args:
            position (int): Position within child_items to insert the new items
            count (int): Number of new items to create

        Returns:
            bool: True if the items were inserted, False if not
        """

    @abstractmethod
    def remove_children(self, position: int, count: int) -> bool:
        """Remove child items starting at the given position

        This method must remove one or more existing tree items from
        self.child_items, starting at the given index.

        Args:
            position (int): Position within child_items to begin removing items
            count (int): Number of child items to remove

        Returns:
            bool: True if the items were removed, False if not
        """

    @abstractmethod
    def set_data(self, column: int, value) -> bool:
        """Set the data for this item at the specified column

        [description]

        Args:
            column (int): [description]
            value ([type]): [description]

        Returns:
            bool: True if the data was set, False if not
        """

    def child(self, number: int) -> 'TreeItem':
        if number < 0 or number >= len(self.child_items):
            return None
        return self.child_items[number]

    def last_child(self):
        return self.child_items[-1] if self.child_items else None

    def child_count(self) -> int:
        return len(self.child_items)

    def child_number(self) -> int:
        if self.parent_item:
            return self.parent_item.child_items.index(self)
        return 0

    def column_count(self) -> int:
        return len(self.item_data)

    def parent(self):
        return self.parent_item

    def __repr__(self) -> str:
        result = f"<treeitem.TreeItem at 0x{id(self):x}"
        for d in self.item_data:
            result += f' "{d}"' if d else " <None>"
        result += f", {len(self.child_items)} children>"
        return result
