from sqlalchemy import select, Select
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

def all() -> Select:
    """Create a db query to get all Character records

    This is about the simplest query possible, and exists for completeness and potential future expansion.

    Returns:
        Select: Select object for the character query
    """
    return select(Character)
