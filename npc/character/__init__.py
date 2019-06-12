"""
Module for all character objects.
"""

from .character import Character
from .changeling import Changeling
from .werewolf import Werewolf
from .spirit import Spirit

from . import tags

def build(attributes: dict = None, other_char: Character = None):
    """
    Build a new character object with the appropriate class

    This derives the correct character class based on the type tag of either the
    other_char character object or the attributes dict, then creates a new
    character object using that class. If neither is supplied, a blank Character
    is returned.

    The character type is fetched first from other_char and only if that is not
    present is it fetched from attributes.

    Both other_char and attribuets are passed to the character constructor. See
    that for how their precedence is applied.

    If you need more control over the instantiation process, use
    character_klass_from_type and call the object manually.

    Args:
        attributes (dict): Dictionary of attributes to insert into the
            Character.
        other_char (Character): Existing character object to copy.

    Returns:
        Instantiated Character class or subclass matching the given type.
    """
    if other_char:
        klass = character_klass_from_type(other_char.type_key)
    elif attributes:
        klass = character_klass_from_type(attributes['type'][0])
    else:
        klass = Character

    return klass(other_char = other_char, attributes = attributes)

def character_klass_from_type(ctype: str):
    """
    Choose the correct character class based on type tag

    Args:
        ctype (str): Character type tag to use

    Returns:
        Character class or subclass depending on the type
    """
    if ctype:
        ctype = ctype.lower()
        if ctype == 'changeling':
            return Changeling
        if ctype == 'werewolf':
            return Werewolf
        if ctype == 'spirit':
            return Spirit

    return Character
