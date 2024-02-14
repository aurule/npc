from ..abstract_tree import TreeItem

from npc.db import DB

class TagTreeItem(TreeItem):
    def __init__(self, parent: TreeItem = None, db: DB = None):
        super().__init__(parent)

        self.db = db if db else DB()

    def data(self, column: int):
        pass

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
        pass
