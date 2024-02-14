from ..abstract_tree import TreeItem
from .tag_tree_item import TagTreeItem

class TagTreeHeaderItem(TreeItem):
    def __init__(self):
        super().__init__(None)

        self.item_data = ["Tag", "Value"]

    def data(self, column: int):
        if column < 0 or column >= len(self.item_data):
            return None

        return self.item_data[column]

    def insert_children(self, position: int, count: int) -> bool:
        if position < 0 or position > len(self.child_items):
            return False

        for row in range(count):
            # make a new record, assign it to item by id
            item = TagTreeItem(self)
            self.child_items.insert(position, item)

        return True

    def remove_children(self, position: int, count: int) -> bool:
        if position < 0 or position + count > len(self.child_items):
            return False

        for row in range(count):
            item = self.child_items.pop(position)
            # delete associated record

        return True

    def set_data(self, column: int, value) -> bool:
        return False