"""Repository of tag-related queries

These queries are limited to ones that do not rely on anything from the Character class. Since tags usually
belong to a character, most queries end up in the character repository instead.
"""

from sqlalchemy import select, Select, func, desc
from npc.characters import Tag

def value_counts(name: str) -> Select:
    """Create a db query to get a count of all values for a tag

    Builds a query that counts the appearances of each unique value for a tag

    Args:
        name (str): Name of the tag to check

    Returns:
        Select: Select object for the tag query
    """
    return select(Tag.value, func.count(1).label("value_count")) \
        .where(Tag.name == name) \
        .group_by(Tag.value) \
        .order_by(desc("value_count"))
