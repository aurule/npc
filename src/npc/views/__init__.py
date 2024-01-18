"""Module for read-only views into campaign data

View objects are only available for specific objects, usually ones backed by the
internal database. They are *not* automatically updated when the underlying data
changes.
"""

from .character_view import CharacterView
from .group_view import GroupView
from .tag_view import TagView
from .tag_view_collection import TagViewCollection

def get(klass_name: str):
    """Get the view class for a named data class

    Args:
        klass_name (str): Name of the data class

    Returns:
        class: View class for the named data class, or None
    """
    match klass_name:
        case "Character":
            return CharacterView
        case "Group":
            return GroupView
        case "Tag":
            return TagView
        case _:
            return None
