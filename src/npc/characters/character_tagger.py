from . import Character, Tag, RawTag
from .taggable_interface import Taggable
from npc.settings.tags import MetatagSpec, UndefinedTagSpec, TagSpec

import logging
logger = logging.getLogger(__name__)

class CharacterTagger():
    """Apply tags to a character record

    This handles all of the logic for creating tag records associated with a character. This includes
    expanding metatags, handling subtags, and tracking each tag's hidden state.
    """

    def __init__(self, campaign, character: Character):
        self.campaign = campaign
        self.character = character
        self.context_stack: list[Taggable] = [character]
        self.hidden: list[str] = list()

    def apply_tags(self, rawtags: list[RawTag]):
        """Apply a list of raw tags to our character

        The raw tag objects are parsed in order, as subtag handling is strictly order-dependent. This method
        does not insert the created tag objects into the database.

        Args:
            rawtags (list[RawTag]): List of raw tag objects to apply to our character
        """

        data_tags = self.encode_hide_tags(rawtags)

        for rawtag in data_tags:
            self.apply_raw_tag(rawtag)

    def encode_hide_tags(self, rawtags: list[RawTag]) -> list[RawTag]:
        """Store and remove any hide tags for later handling

        Hide tags are not stored as literal tags. Instead, they cause the "hidden" attr of other tags to be
        set. This method returns a list of raw tags with the hide tags filtered out and added to an internal
        list of hidden tag data.

        Args:
            rawtags (list[RawTag]): List of raw tags to process

        Returns:
            list[RawTag]: List of raw tags with hide tags removed
        """
        data_tags = list()

        for rawtag in rawtags:
            if rawtag.name == "hide":
                self.hidden.append(self.build_hide_value(rawtag.value))
            else:
                data_tags.append(rawtag)

        return data_tags

    def build_hide_value(self, value: str) -> str:
        """Create the canonical hide value from a hide tag

        The canonical value for a hide tag removes all whitespace around the >> delimeters and appends "all"
        if an explicit value is not given.

        Args:
            value (str): Value of the hide tag to be modified

        Returns:
            str: Modified hide tag value
        """
        parts = [v.strip() for v in value.split(">>")]
        if len(parts) % 2 != 0:
            parts.append("all")
        return ">>".join(parts)

    def tag_is_hidden(self, tag: Tag) -> str:
        """Get whether a tag is hidden

        Compares the tag against a constructed key based on the tags in the context stack. If a hidden value
        ending with the tag's name and "all" or its name and value is found, the tag is considered hidden.

        Args:
            tag (Tag): Tag to test

        Returns:
            str: "all" if the tag is entirely hidden, "one" if just this instance is hidden, or None if it is not hidden
        """
        if not self.hidden:
            return None

        parts = []
        for parent in self.context_stack[1:]:
            parts.append(parent.name)
            parts.append(parent.value)

        all_key = ">>".join(parts + [tag.name, "all"])
        if all_key in self.hidden:
            return "all"

        one_key = ">>".join(parts + [tag.name, tag.value])
        if one_key in self.hidden:
            return "one"

        return None

    def apply_raw_tag(self, rawtag: RawTag, *, mapped: bool = True):
        """Apply a RawTag to our character

        Calls out to other methods to deal with the various cases of tag type.

        The mapped arg should normally be True. When False, a tag object will be created for tags which are
        normally represented by attributes on the character object. The only time to set it to False is if you
        want to represent all possible tag-like data from the character file, like for linting. Setting
        mapped to False does *not* prevent expansion of metatags.

        Args:
            rawtag (RawTag): Raw tag name and value object
            mapped (bool): Whether to map certain tags onto character attrs instead of making tag objects (default True)
        """
        if mapped and self.handle_mapped_tag(rawtag):
            return

        if rawtag.name in self.campaign.metatags:
            metatag = self.campaign.metatags.get(rawtag.name)
            self.expand_metatag(metatag, rawtag.value)
            return

        tag_spec = self.get_tag_spec(rawtag.name)

        tag = Tag(name = rawtag.name, value = rawtag.value)
        if hidden_value := self.tag_is_hidden(tag):
            tag.hidden = hidden_value
        tag.spec = tag_spec.in_context(self.context_stack[-1].name, UndefinedTagSpec(rawtag.name))
        if tag.spec.no_value:
            tag.value = None
        self.insert_tag_record(tag)

    def get_tag_spec(self, tag_name: str) -> TagSpec:
        """Get the most accurate tag spec for current character state

        If the character has a type_key attribute, then we can use that to resolve type-specific tags.
        Otherwise, we fall back on campaign tags.

        Args:
            tag_name (str): Name of the tag to get

        Returns:
            TagSpec: Spec of the tag
        """
        if self.character.type_key and self.character.type_key != Character.DEFAULT_TYPE:
            return self.campaign.get_type_tag(tag_name, self.character.type_key)
        return self.campaign.get_tag(tag_name)

    def handle_mapped_tag(self, tag: RawTag) -> bool:
        """Assign values of mapped tags to the right character property

        The tags listed in Character.MAPPED_TAGS are each represented by a property on the Character object.
        This method assigns those properties.

        Args:
            tag (RawTag): The tag data to apply
        """
        attr_name = Character.MAPPED_TAGS.get(tag.name)
        match tag.name:
            case "type" | "realname":
                setattr(self.character, attr_name, tag.value)
            case "sticky" | "nolint" | "delist":
                setattr(self.character, attr_name, True)
            case "description":
                if not getattr(self.character, attr_name):
                    setattr(self.character, attr_name, tag.value)
                else:
                    setattr(self.character, attr_name, f"{self.character.desc}\n\n{tag.value}")
            case _:
                return False

        return True

    def expand_metatag(self, metatag: MetatagSpec, metatag_value: str):
        """Turn a metatag into one or more normal tags

        Static tags are emitted as-is. Match tags are assigned values either based on their values list, or by
        splitting the metatag's own value using its separator.

        Args:
            metatag (MetatagSpec): MetatagSpec object to use for creating tags
            metatag_value (str): Raw value for the metatag, applied to match tags
        """
        def try_contexts(spec):
            for rawtag in reversed(self.context_stack):
                if context := spec.in_context(rawtag.name):
                    return context
            return UndefinedTagSpec(spec.name)

        def find_matching_value(spec, working_value):
            for value in spec.values:
                if working_value.startswith(value):
                    return value

        for name, value in metatag.static.items():
            self.apply_raw_tag(RawTag(name, value))

        working_value = metatag_value

        for name in metatag.match:
            spec = self.get_tag_spec(name)
            spec = try_contexts(spec)
            if matching_value := find_matching_value(spec, working_value):
                self.apply_raw_tag(RawTag(name, matching_value))
                working_value = working_value.removeprefix(matching_value).lstrip(metatag.separator)
                continue

            value_parts = working_value.partition(metatag.separator)
            self.apply_raw_tag(RawTag(name, value_parts[0]))
            working_value = value_parts[2]

    def insert_tag_record(self, tag: Tag):
        """Insert a tag into the first accepting container on the context stack

        The internal context stack is a list of Taggable objects. This tries to insert tag into the last entry
        of the list. If that fails, it pops and tries again. It's important that the 0 entry of the stack list
        accepts all tags, or there may be errors raised when the pop call fails.

        Args:
            tag (Tag): Tag object to add
        """
        context = self.context_stack[-1]
        if context.accepts_tag(tag.name):
            context.add_tag(tag)
            try:
                if tag.spec.subtags:
                    self.context_stack.append(tag)
            except AttributeError:
                pass
            return self.context_stack

        self.context_stack.pop()
        return self.insert_tag_record(tag)
