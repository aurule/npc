"""Repository of character-related queries

These queries get data that's related to a character or its tags.
"""

from sqlalchemy import select, Select, Exists, func, desc
from sqlalchemy.orm import selectinload
from npc.characters import Tag, Character

def tag_values_by_name(character: Character, *names: str) -> Select:
    """Create a database query to get values for a single character's tags

    Builds a DB query for the named tags, scoped to the character. This query only returns tag values.

    Args:
        character (Character): Character containing the tags to query
        names (Tuple[str]): Tag names to include in the query

    Returns:
        Select: Select object for a tag value query
    """
    return select(Tag.value) \
        .where(Tag.name.in_(names)) \
        .filter(Tag.character_id == character.id) \
        .order_by(Tag.id)

def tags_by_name(character: Character, *names: str) -> Select:
    """Create a db query to get Tag records from a character, filtered by name

    Builds a query for the named tags, scoped to the character. Best used with the scalars() method to get a
    list of Tag objects instead of single-element tuples.

    Args:
        character (Character): Character containing the tags to query
        names (Tuple[str]): Tag names to include in the query

    Returns:
        Select: Select object for the tag query
    """
    return tags(character).where(Tag.name.in_(names))

def tags(character: Character) -> Select:
    """Create a db query to get all Tag records for a character

    Builds a query for all tags, scoped to the given character. Best used with the scalars() method to get a
    list of Tag objects instead of single-element tuples.

    Args:
        character (Character): Character containing the tags to query

    Returns:
        Select: Select object for the tag query
    """
    return select(Tag) \
        .filter(Tag.character_id == character.id) \
        .order_by(Tag.id)

def has_tags(character: Character, *names: str) -> Select:
    """Create a db query to get whether the named Tag records exist for a character

    Builds an existence query for the named tags, scoped to the character. Best used with the scalar() method
    to get a single boolean-esque value.

    Args:
        character (Character): Character containing the tags to query
        names (Tuple[str]): Tag names to include in the query

    Returns:
        Select: Select object for the tag existence query
    """
    exists_test: Exists = tags_by_name(character, *names).exists()
    return select(func.count(1)).where(exists_test)

def all() -> Select:
    """Create a db query to get all Character records

    This is about the simplest query possible, and exists for completeness and potential future expansion.

    Returns:
        Select: Select object for the character query
    """
    return select(Character)

def with_tags() -> Select:
    """Create a db query to get all Character records and eager-load their tags

    Returns:
        Select: Select object for the character query with eager loading of the tags relationship
    """
    return all() \
        .options(selectinload(Character.tags))

def get(id: int) -> Select:
    """Create a db query to get a single Character record

    Args:
        id (int): ID of the character record to get

    Returns:
        Select: Select object for the character query
    """
    return select(Character) \
        .where(Character.id == id)

def attr_counts(name: str) -> Select:
    """Create a db query to get a count for all values of an attribute

    Builds a query that counts the appearances of each value of an attribute

    Args:
        name (str): Name of the attribute to count. Must appear in Character.MAPPED_TAGS

    Returns:
        Select: Select object for the character query
    """
    attr = getattr(Character, Character.MAPPED_TAGS.get(name))
    return select(attr, func.count(1).label("attr_count")) \
        .group_by(attr) \
        .order_by(desc("attr_count"))
