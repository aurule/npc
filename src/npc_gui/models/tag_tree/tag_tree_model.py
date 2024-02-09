from PySide6.QtCore import (
    QModelIndex, Qt, QAbstractItemModel
)

from npc.db import DB

from ..abstract_tree import TreeModel
from .tag_tree_header_item import TagTreeHeaderItem

class TagTreeModel(TreeModel):
    def __init__(self, taggable_type: str, taggable_id: int, db: DB = None, parent = None):
        super().__init__(parent)

        self.db = db if db else DB()
        self.root_item = TagTreeHeaderItem()

        # create items from taggable.tags
        # parents = [self.root_item]
        # for tag in taggable.tags:
        #     pass
            # tag item for each tag id
            # in each tag item, its setup should create children as needed for its subtags
