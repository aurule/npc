from npc.db import DB, character_repository
from npc.campaign import Pathfinder

from .base_reorganizer import BaseReorganizer
from .relocation_class import Relocation

class CharacterReorganizer(BaseReorganizer):
    """Reorganizer for characters

    Gets the paths for all character files in the campaign.
    """
    def __init__(self, campaign, db: DB = None, exists: bool = True):
        """Create a new CharacterReorganizer

        Args:
            campaign (Campaign): Campaign this is for
            db (DB): Database to use. Defaults to global singleton (default: `None`)
            exists (bool): Whether to limit ideal paths to existing directories (default: `True`)
        """
        super().__init__()

        self.campaign = campaign
        self.db = db if db else DB()
        self.exists = exists
        self.pathfinder = Pathfinder(self.campaign, self.db)

    def gather_paths(self):
        """Gather the ideal paths for character records

        Iterates each character and uses our pathfinder to generate an ideal path. The current path is just
        the record's file_path, so that needs to be populated correctly beforehand.
        """
        for character in self.campaign.characters.all():
            ideal_path = self.pathfinder.build_character_path(character, exists=self.exists)
            ideal_filename = self.pathfinder.make_filename(character)
            self.add_relocation(character.id, character.file_path, ideal_path / ideal_filename)

    def after_move(self, relocation: Relocation):
        """Update the character's path after it's been moved

        Args:
            relocation (Relocation): The relocation that was just executed.
        """
        query = character_repository.update_attrs_by_id(relocation.id,
                                                        {"file_loc": str(relocation.ideal_path)})
        self.campaign.characters.apply_query(query)
