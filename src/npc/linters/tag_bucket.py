from collections import defaultdict

from npc.characters import Character
from npc.characters.taggable_interface import Taggable

@Taggable.register
class TagBucket:
    """Class that holds tags indexed by name

    This class is meant to make tags easy to fetch by name so that linting them against a spec is easier. It
    is able to be dropped into the CharacterFactory's apply_raw_tag method in place of a Character object.
    """
    def __init__(self, character: Character = None):
        self.character = character
        self.tags = defaultdict(list)

    def accepts_tag(self, tag_name: str) -> bool:
        """Indicate that TagBucket objects accept all tags

        Args:
            tag_name (str): Tag name to test

        Returns:
            bool: True. Character objects accept all tags.
        """
        return True

    def add_tag(self, tag):
        """Add the tag to the appropriate key of our tags dict

        Adds the tag to the list in our tags dict keyed by the tag name

        Args:
            tag (Tag): Tag to add
        """
        self.tags[tag.name].append(tag)

    @property
    def type_key(self) -> str:
        """Get our character object's type key

        The type key is normally pulled from the character object. However, for compatibility with the
        character factory, None is returned instead when the type key matches the default type.

        Returns:
            str: Character's type_key, or None if it's the default
        """
        raw_key = self.character.type_key
        if raw_key == Character.DEFAULT_TYPE:
            return None
        return raw_key
