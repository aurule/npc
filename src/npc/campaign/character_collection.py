from functools import cached_property

from .pathfinder_class import Pathfinder
from npc.characters import Character, CharacterFactory, CharacterReader, CharacterWriter
from npc.db import DB, character_repository

class CharacterCollection():
    """Class for a group of Character objects, backed by a database

    Manages the loading, creation, and fetching of Characters
    """

    def __init__(self, campaign, *, db: DB = None):
        if db:
            self.db = db
        else:
            self.db = DB()

        self.campaign = campaign
        self.root = campaign.characters_dir

    def refresh(self):
        def allowed(path):
            if path.suffix not in self.allowed_suffixes:
                return False

            # if self.campaign.ignore in path.parents:
            #     return False

            return True

        valid_exts = self.allowed_suffixes
        for character_path in self.root.glob("**/*"):
            if not allowed(character_path):
                continue

            reader = CharacterReader(character_path)
            self.create(
                realname = reader.name(),
                mnemonic = reader.mnemonic(),
                body = reader.body(),
                tags = reader.tags(),
            )

    @cached_property
    def allowed_suffixes(self) -> set[str]:
        """Get the file suffixes that are allowed by this campaign

        The .npc suffix is always present. Suffixes used by each type's default sheet are also included.

        Returns:
            set[str]: Set of suffix strings
        """
        return {".npc"}.union({spec.default_sheet_suffix for spec in self.campaign.types.values()})

    def create(self, **kwargs) -> int:
        """Make and save a new character object

        The character object is created using the given kwargs and immediately persisted to the database.

        Returns:
            int: ID of the newly created character
        """
        factory = CharacterFactory(self.campaign)
        character = factory.make(**kwargs)

        with self.db.session() as session:
            session.add(character)
            session.commit()

        return character.id

    def write(self, character: Character = None):
        writer = CharacterWriter(self.campaign, db=self.db)
        # write the character object to its destination file
        # if it has no path, use pathfinder to make one
        # pathfinder = Pathfinder(self.campaign, db=self.db)

    def get(self, character_id: int) -> Character:
        pass
        # get a character by ID, or None if not found
