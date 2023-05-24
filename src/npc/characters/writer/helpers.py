from npc.settings import MetatagSpec
from npc.db.character_repository import tags_by_name
from ..character_class import Character
from ..tag_class import Tag
from .con_tag_class import ConTag
from .metatag_class import Metatag

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

    metatag = Metatag(spec)

    tag_names = spec.static.keys() + spec.match
    stmt = tags_by_name(tag_names).where(Tag.id.not_in(bad_ids))
    with db.session as session:
        result = session.scalars(stmt)
        for tag in result:
            metatag.consider(tag)

    if not metatag.satisfied():
        return (None, None)

    metatags.append(metatag)
    consumed_ids.extend(metatag.tag_ids)
    if spec.greedy:
        bad_ids.extend(consumed_ids)
        (next_metatags, next_ids) = make_metatags(spec, character, bad_ids)
        metatags.extend(next_metatags)
        consumed_ids.extend(next_ids)

    return (metatags, consumed_ids)
