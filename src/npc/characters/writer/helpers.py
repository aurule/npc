from npc.settings import MetatagSpec
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

def make_metatags(spec: MetatagSpec, character: Character, handled_ids: list[int]) -> tuple:
    bad_ids: list[int] = copy(handled_ids)
    metatags: list = []
    consumed_ids: list[int] = []

    # if spec.greedy:
    #   repeat until fail
    # else
    #   try once
    # every static entry must exist and not in metatag_consumed
    # every match entry must exist and not in metatag_consumed
    # if all exist
    #   store appropriately
    #   put tag IDs into metatag_consumed
    #   place Metatag objects into constructed_tags

    # select Tag.id from tags where name = static and id not in bad_ids
    # tags_by_name(static).where(id not in bad_ids).limit(1)
    # .scalars().first()

    # tags_by_name(static+match).where(id not in bad_ids)
    # result = session.scalars(...)
    # for tag in result:
    #   metatag.consider(tag)
    #       adds to metatag if that name is accepted and not already populated
    # if metatag.satisfied():
    #   true if all names are populated
    #   add to metatags
    #   add ids to consumed_ids
    #   if greedy:
    #       add ids to bad_ids
    #       extend metatags and consumed_ids with result of make_metatags(spec, character, bad_ids)

    return (metatags, consumed_ids)
