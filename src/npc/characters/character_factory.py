from . import Character, RawTag
from .character_tagger import CharacterTagger

import logging
logger = logging.getLogger(__name__)

class CharacterFactory():
    """Create Character objects from simple data"""

    def __init__(self, campaign):
        self.campaign = campaign

    def make(
        self,
        realname: str,
        *,
        type_key: str = None,
        mnemonic: str = None,
        body: str = None,
        path: str = None,
        desc: str = "",
        tags: list[RawTag] = None,
    ) -> Character:
        """Make a Character object from passed values

        Most of the values are passed to the Character constructor verbatim, except the tags list. That is
        parsed into Tag records which are associated with the new Character.

        This method does not add the created Character or its Tags to any database. It merely returns the new
        object(s).

        Args:
            type_key (str): Type key for the character. Should appear in campaign.types.
            realname (str): The character's name
            mnemonic (str): A brief reminder of the character to go in its filename (default: `None`)
            body (str): The non-tag contents of the character's file (default: `None`)
            path (str): The path to the character file location (default: `None`)
            desc (str): General purpose text in the tag area of the sheet (default: `None`)
            tags (list[RawTag]): List of tag data to parse and add as Tag records (default: `None`)

        Returns:
            Character: Character object with tags and properties filled in
        """
        if tags is None:
            tags = []

        character = Character(
            type_key=type_key,
            realname=realname,
            mnemonic=mnemonic,
            file_body=body,
            desc=desc,
            delist=False,
            nolint=False,
            sticky=False,
        )
        character.file_path = path

        tagger = CharacterTagger(self.campaign, character)
        tagger.apply_tags(tags)

        return character
