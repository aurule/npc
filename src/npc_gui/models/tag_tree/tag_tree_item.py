from ..abstract_tree import TreeItem

from PySide6.QtCore import Qt

from npc.db import DB
from npc.characters import Tag
import npc.db.tag_repository as repository

class TagTreeItem(TreeItem):
    def __init__(self, tag_id: int, parent: TreeItem, db: DB = None):
        super().__init__(parent)

        self.db = db if db else DB()
        self.tag_id = tag_id
        with self.db.session() as session:
            tag = session.get(Tag, self.tag_id)
            session.commit()
        self.item_data = [tag.name, tag.value]

    def data(self, column: int, role: int = None):
        if column < 0 or column >= len(self.item_data):
            return None

        match role:
            case Qt.DisplayRole:
                self.item_data[column]
            case Qt.EditRole:
                self.item_data[column]

    def insert_children(self, position: int, count: int) -> bool:
        if position < 0 or position > len(self.child_items):
            return False

        for row in range(count):
            tag = Tag(parent_tag_id=self.tag_id)
            with self.db.session() as session:
                session.add(tag)
                session.commit()
            item = TagTreeItem(tag, parent=self, db=self.db)

            self.child_items.insert(position, item)

        return True

    def remove_children(self, position: int, count: int) -> bool:
        if position < 0 or position + count > len(self.child_items):
            return False

        for row in range(count):
            item = self.child_items.pop(position)
            with self.db.session() as session:
                session.delete(Tag, tag.id)
                session.commit()

        return True

    def set_data(self, column: int, value) -> bool:
        match column:
            case 0:
                updates = {"name": value}
            case 1:
                updates = {"value": value}
            case _:
                return False

        query = repository.update_attrs_by_id(self.tag_id, updates)
        with self.db.session() as session:
            session.execute(query)
            tag = session.get(Tag, self.tag_id)
            session.commit()
        self.item_data = [tag.name, tag.value]
        return True
