from dataclasses import dataclass
from . import Character, Tag, RawTag
from npc.campaign import Campaign
from npc.settings import TagSpec

import logging
logger = logging.getLogger(__name__)

@dataclass
class TagContext():
    """Internal class used for the parent tag stack in handle_tag_stack

    Attributes:
        tag: Tag object
        subtag_names: List of valid subtag names
    """
    tag: Tag
    subtag_names: list[str]

class CharacterFactory():
    """Create Character objects from simple data"""

    def __init__(self, campaign: Campaign):
        self.campaign = campaign

    def make(
        self,
        realname: str,
        *,
        type_key: str = None,
        mnemonic: str = None,
        body: str = None,
        path: str = None,
        desc: str = None,
        tags: list[RawTag] = None,
    ):
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
        """
        def walk_tag_stack(tag: Tag):
            context = context_stack[-1]
            if context.accepts_tag(tag.name):
                context.add_tag(tag)
                if tag.spec.subtags:
                    context_stack.append(tag)
                return

            context_stack.pop()
            walk_tag_stack(tag)

        if tags is None:
            tags = []

        character = Character(
            type_key=type_key,
            realname=realname,
            mnemonic=mnemonic,
            file_body=body,
            file_path=path,
            desc=desc,
        )

        context_stack: list[Taggable] = [character]
        for rawtag in tags:
            if self.handle_mapped_tag(character, rawtag):
                continue

            # if tag.name in character.campaign.meta_tags:
            #     # use helper to expand the meta-tag and extend tags with the resulting list
            #     pass

            tag_spec = self.campaign.get_tag(rawtag.name)
            tag = Tag(name = rawtag.name, value = rawtag.value)
            tag.spec = tag_spec.in_context(context_stack[-1].name)

            walk_tag_stack(tag)

        return character

    def handle_mapped_tag(self, character: Character, tag: RawTag) -> bool:
        """Assign values of mapped tags to the right character property

        The tags listed in Character.MAPPED_TAGS are each represented by a property on the Character object.
        This method assigns those properties.

        Args:
            character (Character): The character to modify
            tag (RawTag): The tag data to apply

        Returns:
            bool: True if the tag was handled, false if not

        Raises:
            NotImplementedError: In the unexpected case of a new mapped tag that has not yet been implemented,
            this error will be raised as a safety.
        """
        if tag.name not in Character.MAPPED_TAGS:
            return False

        match tag.name:
            case "type":
                character.type_key = tag.value
            case "realname":
                character.realname = tag.value
            case "sticky":
                character.sticky = True
            case "nolint":
                character.nolint = True
            case "delist":
                character.delist = True
            case _:
                raise NotImplementedError(f"Tag {tag.name} is supposed to be mapped to a Character property, but has no implementation")

        return True
