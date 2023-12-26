from npc.db import DB, tag_repository, character_repository
from npc.characters import Character, Tag

def value_counts_report(tag_name: str, *, db: DB = None):
    """Get report data that counts occurrences of all unique values for the named tag

    This either runs a query on Tag, or a query on Character for tags which are technically mapped to an
    attribute.

    Args:
        tag_name (str): Name of the tag to analyze
        db (DB): Database to use for querying. Defaults to the singleton. (default: `None`)

    Returns:
        list[Row]: List of tuple-like Row objects for the results
    """
    if not db:
        db = DB()

    if tag_name in Character.MAPPED_TAGS:
        query = character_repository.attr_counts(tag_name)
    else:
        query = tag_repository.value_counts(tag_name)

    with db.session() as session:
        return session.execute(query).all()

def subtag_value_counts_report(tag_name: str, context: str, *, db: DB = None):
    """Get report data that counts occurrences of all unique values for the named subtag within the given context

    This runs a query on Tag to get the appropriate values. It does not subdivide by parent tag value.

    Args:
        tag_name (str): Name of the subtag to analyze
        context (str): Name of the context to look at
        db (DB): Database to use for querying. Defaults to the singleton. (default: `None`)

    Returns:
        list[Row]: List of tuple-like Row objects for the results
    """
    if not db:
        db = DB()

    query = tag_repository.subtag_value_counts(tag_name, context)

    with db.session() as session:
        return session.execute(query).all()
