from npc.db import DB, tag_repository
from npc.characters import Character, Tag

def value_counts_report(tag_name, db=None):
    if not db:
        db = DB()

    if tag_name in Character.MAPPED_TAGS:
        pass
        # need to look up the character attribute to use for the named tag
        # query needs to look at Character.attribute, but is otherwise very similar
    else:
        query = tag_repository.value_counts(tag_name)

    with db.session() as session:
        return session.execute(query).all()
