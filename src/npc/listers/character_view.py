from npc.characters import Character
from .tag_view_collection import TagViewCollection

class CharacterView:
    """A static representation of a character's values and tags

    This class dynamically creates attributes for each tag name during initialization. This lets templates
    easily access tag values. With the similar setup of the TagView class, this allows for a fluent-style
    interface within templates.

    Examples:
        character.realname                  # Fred
        character.org.first()               # Mars Bank, Ltd.
        character.org.first().role.all()    # Teller, Janitor, ...
        character.org.rest()                # Olympus Mons Bowling Club, ...
    """
    def __init__(self, character: Character):
        self.type: str = character.type_key
        self.description: str = character.desc or ""
        self.realname: str = character.realname or ""
        self.mnemonic: str = character.mnemonic or ""

        for tag in character.tags:
            if tag.name == "faketype":
                self.type = tag.value
                continue
            if not hasattr(self, tag.name):
                setattr(self, tag.name, TagViewCollection())
            getattr(self, tag.name).append_tag(tag)

    def __str__(self) -> str:
        """Return a printable representation of this view

        Since this object is meant to be used in templates, this default string implementation returns the
        realname of the view's associated character.

        Returns:
            str: Our realname string
        """
        return self.realname

    def has(self, tag_name: str) -> bool:
        """Get whether a named tag is present

        This is just a convenience wrapper around hasattr.

        Args:
            tag_name (str): Name of the tag to check

        Returns:
            bool: True if this character has at least one tag with the given name, false otherwise
        """
        return hasattr(self, tag_name)
