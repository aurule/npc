from npc.settings import MetatagSpec
from npc.db import DB
from npc.db.character_repository import tags_by_name, tags
from npc.characters.character_class import Character
from npc.characters.tag_class import Tag
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
        dict: ConTag object lists indexed by tag name for easy lookup. Each list should only ever have a
        single value.
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

def make_hide_tags(character: Character, *, db: DB = None) -> list[ConTag]:
    """Construct special @hide tags from tag hidden attributes

    Generates ConTag objects used to emit hide tags which affect the hidden attribute of tag records.

    Args:
        character (Character): Character whose tags will be inspected
        db (DB): Database to use for fetching the character's tag records (default: `None`)

    Returns:
        set[ConTag]: [description]
    """
    def build_hides(examined_tags: list[Tag], preamble: str = "") -> set[ConTag]:
        hide_tags = set()

        for tag in examined_tags:
            match tag.hidden:
                case "all":
                    hide_tags.add(ConTag("hide", preamble + tag.name))
                case "one":
                    hide_tags.add(ConTag("hide", f"{preamble}{tag.name} >> {tag.value}"))
                case _:
                    hide_tags = hide_tags.union(build_hides(tag.subtags, preamble + f"{tag.name} >> {tag.value} >> "))

        return hide_tags

    if not db:
        db = DB()

    stmt = tags(character)
    with db.session() as session:
        result = session.scalars(stmt)
        hide_tags = build_hides(result)

    return list(hide_tags)

def make_metatags(spec: MetatagSpec, character: Character, handled_ids: list[int], *, db: DB = None) -> list:
    """Construct one or more Metatag objects using the given spec and character

    Args:
        spec (MetatagSpec): Spec to apply
        character (Character): Character to use for tags
        handled_ids (list[int]): List of tag IDs to exclude
        db (DB): Database object for the tag query (default: `None`)

    Returns:
        list: [description]
    """
    if not db:
        db = DB()

    metatags: list = []

    metatag = Metatag(spec)

    contag_lists = make_contags(character).values()
    for contag_list in contag_lists:
        for contag in contag_list:
            metatag.consider(contag)

    stmt = tags_by_name(character, *spec.required_tag_names).where(Tag.id.not_in(handled_ids))
    with db.session() as session:
        result = session.scalars(stmt)
        for tag in result:
            metatag.consider(tag)

    if not metatag.satisfied():
        return metatags

    metatags.append(metatag)
    if spec.greedy:
        next_metatags = make_metatags(spec, character, handled_ids + metatag.tag_ids)
        metatags.extend(next_metatags)

    return metatags
