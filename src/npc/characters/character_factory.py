from dataclasses import dataclass
from . import Character, Tag, RawTag
from npc.campaign import Campaign
from npc.settings import TagSpec

import logging
logger = logging.getLogger(__name__)

@dataclass
class TagContext():
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

        context_stack: list[TagContext] = []
        for rawtag in tags:
            if self.handle_mapped_tag(character, rawtag):
                continue

            # if tag.name in character.campaign.meta_tags:
            #     # use helper to expand the meta-tag and extend tags with the resulting list
            #     pass

            tag_spec = self.campaign.get_tag(rawtag.name)
            tag = Tag(name = rawtag.name, value = rawtag.value)

            self.handle_tag_stack(character, tag, spec=tag_spec, stack=context_stack)

        return character

    def handle_tag_stack(self, character: Character, tag: Tag, spec: TagSpec, stack: list[TagContext]):
        """Add tag to the correct level of the stack

        If the stack is empty, tag is added directly to the character. If tag has subtags, it is then pushed
        to the stack.

        If the stack is not empty and the top of stack can accept tag as a subtag, tag is added to that parent
        tag. Also, if tag has subtags, it is then pushed to the stack itself.

        If the stack is not empty and the top of the stack cannot take tag as a subtag, that parent tag is
        popped off the stack and we recurse.

        The end result is that tag is tried against the whole stack until it's allowed as a subtag, or added
        to the character.

        Args:
            character (Character): Character object we are building
            tag (Tag): Tag to add to a parent in the stack, or to the character
            spec (TagSpec): Tag spec for the tag being added
            stack (list[TagContext]): Stack of open parent tags
        """
        if not stack:
            character.tags.append(tag)
            if spec.subtags:
                stack.append(TagContext(tag, spec.subtags))
            return

        context = stack[-1]
        if tag.name in context.subtag_names:
            context.tag.subtags.append(tag)
            if spec.in_context(context.tag.name).subtags:
                stack.append(TagContext(tag, spec.in_context(context.tag.name).subtags))
            return

        stack.pop()
        self.handle_tag_stack(character, tag, spec, stack)

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
