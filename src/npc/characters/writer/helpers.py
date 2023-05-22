from ..character_class import Character
from .con_tag_class import ConTag

def viable_character(character: Character) -> bool:
    """Whether a character is capable of being written

    A character must have both an id and a realname to be written out/

    Args:
        character (Character): Character object to test

    Returns:
        bool: True if the character has the required attributes, false if not
    """
    return bool(
        character.id
        and character.realname
        and character.file_loc)

def make_contags(character: Character) -> dict:
    """Construct special tags from character attributes

    Generates ConTag objects used to emit tags which, when parsed, set an attribute on the Character object
    instead of being stored as Tag records.

    Args:
        character (Character): Character to inspect

    Returns:
        dict: ConTag object lists indexed by tag name for easy lookup
    """
    tags: dict = {
        "type": [ConTag("type", character.type_key)]
    }

    if character.realname not in character.file_path.name:
        tags["realname"] = [ConTag("realname", character.realname)]
    if character.sticky:
        tags["sticky"] = [ConTag("sticky")]
    if character.nolint:
        tags["nolint"] = [ConTag("nolint")]
    if character.delist:
        tags["delist"] = [ConTag("delist")]

    return tags
