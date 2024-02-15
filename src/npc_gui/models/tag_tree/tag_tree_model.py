from npc.db import DB

from ..abstract_tree import TreeModel
from .tag_tree_header_item import TagTreeHeaderItem

class TagTreeModel(TreeModel):
    def __init__(self, character_id: int, db: DB = None, parent = None):
        super().__init__(parent)

        self.db = db if db else DB()
        self.root_item = TagTreeHeaderItem(character_id, db=db)
