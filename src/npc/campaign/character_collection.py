from .pathfinder_class import Pathfinder
from npc.characters import Character, CharacterFactory, CharacterReader, CharacterWriter
from npc.db import DB, character_repository

class CharacterCollection():
    """Class for a group of Character objects, backed by a database

    Manages the loading, creation, and fetching of Characters
    """

    def __init__(self, campaign, *, db: DB = None):
        if not db:
            db = DB()

        self.campaign = campaign
        self.root = campaign.characters_dir

    def create(self, **args) -> Character:
        factory = CharacterFactory(self.campaign)
        # create and store a character object for this campaign

    def write(self, character: Character = None):
        writer = CharacterWriter(self.campaign, db=self.db)
        # write the character object to its destination file
        # if it has no path, use pathfinder to make one
        # pathfinder = Pathfinder(self.campaign, db=self.db)

    def get(self, character_id: int) -> Character:
        pass
        # get a character by ID, or None if not found
