from . import Character, Tag
from npc.campaign import Campaign

import logging
logger = logging.getLogger(__name__)

class CharacterFactory():
    """Create Character objects from simple data"""

    def __init__(self, campaign: Campaign):
        self.campaign = campaign

    def make(
        self,
        name: str,
        *,
        type_key: str = None,
        mnemonic: str = None,
        body: str = None,
        path: str = None,
        desc: str = None,
        tags: list = None,
    ):
        """Make a Character object from passed values

        Most of the values are passed to the Character constructor verbatim, except the tags list. That is
        parsed into Tag records which are associated with the new Character.

        This method does not add the created Character or its Tags to any database. It merely returns the new
        object(s).

        Args:
            type_key (str): Type key for the character. Should appear in campaign.types.
            name (str): The character's name
            mnemonic (str): A brief reminder of the character to go in its filename (default: `None`)
            body (str): The non-tag contents of the character's file (default: `None`)
            path (str): The path to the character file location (default: `None`)
            desc (str): General purpose text in the tag area of the sheet (default: `None`)
            tags (list): List of tag data to parse and add as Tag records (default: `None`)
        """
        if type_key not in self.campaign.types:
            logger.warning(f"Character {name} has unknown type {type_key}")

        character = Character(
            type_key=type_key,
            name=name,
            mnemonic=mnemonic,
            file_body=body,
            file_path=path,
            desc=desc,
        )

        if tags:
            self.make_tags(Character, tags)

        return character

    def make_tags(self, character: Character, tags: list):
        working_tags = tags.copy()

        for tag_data in working_tags:
            if tag_data.name == "type":
                character.type_key = tag_data.value
                continue
            if tag_data.name == "realname":
                character.name = tag_data.value
                continue



        # meta-tags are broken into their set and match tags
        # TODO

        # The tags type, realname, sticky, nolint, and delist modify the Character record directly instead of
        # adding Tag records. We handle those first and remove them from the working tags list to prevent
        # processing them twice.
        if "type" in working_tags:
            character.type_key = working_tags.pop("type")
        if "realname" in working_tags:
            character.name = working_tags.pop("realname")
        character.sticky = working_tags.pop("sticky", False)
        character.nolint = working_tags.pop("nolint", False)
        character.delist = working_tags.pop("delist", False)

        # Create Tag records for all remaining tags
        tag_queue = list(tags.keys())
        subtag_context = None

        while len(tag_queue) > 0:
            return
            # most tags get stored as a Tag object
            # subtags need to be assigned to their parent
