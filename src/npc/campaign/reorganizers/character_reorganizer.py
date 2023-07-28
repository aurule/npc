from npc.db import DB

from .base_reorganizer import BaseReorganizer, RecordPaths

class CharacterReorganizer(BaseReorganizer):
    """Reorganizer for characters

    Gets the paths for all character files in the campaign.
    """
    def __init__(self, campaign, db: DB = None):
        super().__init__()

        self.campaign = campaign

        if not db:
            self.db = DB()
        else:
            self.db = db

    def gather_paths(self):
        pass
        # loop all characters
        # list indexed by character ID
        # each entry is a tuple of (current path, ideal path)
