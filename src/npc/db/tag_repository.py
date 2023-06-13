from sqlalchemy import select, Select, func, desc
from npc.characters import Tag

def value_counts(name: str) -> Select:
    return select(Tag.value, func.count(1).label("value_count")) \
        .where(Tag.name == name) \
        .group_by(Tag.value) \
        .order_by(desc("value_count"))
