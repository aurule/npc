from . import Character, Tag, RawTag
from npc.settings.tags import Metatag, UndefinedTagSpec

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
        desc: str = None,
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
            file_path=path,
            desc=desc,
        )

        context_stack = [character]
        for rawtag in tags:
            context_stack = self.apply_raw_tag(rawtag, character, context_stack)

        return character

    def apply_raw_tag(self, rawtag: RawTag, character: Character, stack: list) -> list:
        """Apply a RawTag to the given character

        Calls out to handle_mapped_stack, expand_metatag, and insert_tag_record to deal with the various
        cases of tag type.

        Args:
            rawtag (RawTag): Tag name and value object
            character (Character): Character object to apply the tag to
            stack (list): List of Tag objects, with the character at index 0.

        Returns:
            list: Potentially different list of Tag objects similar to stack
        """
        context_stack = stack.copy()

        if self.handle_mapped_tag(rawtag, character):
            return context_stack

        if rawtag.name in self.campaign.metatags:
            metatag = self.campaign.metatags.get(rawtag.name)
            return self.expand_metatag(metatag, rawtag.value, character, context_stack)

        tag_spec = self.get_tag_spec(rawtag.name, character)
        tag = Tag(name = rawtag.name, value = rawtag.value)
        tag.spec = tag_spec.in_context(context_stack[-1].name)
        return self.insert_tag_record(tag, character, context_stack)

    def get_tag_spec(self, tag_name: str, character: Character):
        """Get the most accurate tag spec for current character state

        If the character has a type, then we can use that to resolve type-specific tags. Otherwise, we fall
        back on campaign tags.

        Args:
            tag_name (str): Name of the tag to get
            character (Character): Character for the tag

        Returns:
            TagSpec: Spec of the tag
        """
        if character.type_key:
            return self.campaign.get_type_tag(tag_name, character.type_key)
        return self.campaign.get_tag(tag_name)

    def handle_mapped_tag(self, tag: RawTag, character: Character) -> bool:
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

    def expand_metatag(self, metatag: Metatag, metatag_value: str, character: Character, stack: list) -> list:
        def try_contexts(spec):
            for rawtag in reversed(stack):
                if spec.in_context(rawtag.name):
                    return spec.in_context(rawtag.name)
            return UndefinedTagSpec(spec.name)

        def find_matching_value(spec, working_value):
            for value in spec.values:
                if working_value.startswith(value):
                    return value

        context_stack = stack.copy()
        for name, value in metatag.static.items():
            context_stack = self.apply_raw_tag(RawTag(name, value), character, context_stack)

        working_value = metatag_value

        for name in metatag.match:
            spec = self.get_tag_spec(name, character)
            spec = try_contexts(spec)
            matching_value = find_matching_value(spec, working_value)
            if matching_value:
                context_stack = self.apply_raw_tag(RawTag(name, matching_value), character, context_stack)
                working_value = working_value.removeprefix(matching_value).lstrip(metatag.separator)
                continue

            value_parts = working_value.partition(metatag.separator)
            context_stack = self.apply_raw_tag(RawTag(name, value_parts[0]), character, context_stack)
            working_value = value_parts[2]

        return context_stack

    def insert_tag_record(self, tag: Tag, character: Character, stack: list) -> list:
        context_stack = stack.copy()

        context = context_stack[-1]
        if context.accepts_tag(tag.name):
            context.add_tag(tag)
            if tag.spec.subtags:
                context_stack.append(tag)
            return context_stack

        context_stack.pop()
        return self.insert_tag_record(tag, character, context_stack)
