from npc.db import DB
from npc.characters import Tag, CharacterFactory, RawTag
from tests.fixtures import tmp_campaign

from npc.reporters.tag_reporter import value_counts_report

def seed(db, campaign):
    factory = CharacterFactory(campaign)
    char1 = factory.make("Test Mann", type_key="person", tags=[RawTag("title", "The Buff")])
    char2 = factory.make("Testier Mann", type_key="person", tags=[RawTag("title", "The Buff")])
    char3 = factory.make("Testiest Mann", type_key="person", tags=[RawTag("title", "The Burly")])
    with db.session() as session:
        session.add(char1)
        session.add(char2)
        session.add(char3)
        session.commit()

def test_counts_mapped_tags_from_character(tmp_campaign):
    db = DB(clearSingleton=True)
    seed(db, tmp_campaign)

    result = value_counts_report("type", db=db)

    assert ("person", 3) in result

def test_counts_normal_tags(tmp_campaign):
    db = DB(clearSingleton=True)
    seed(db, tmp_campaign)

    result = value_counts_report("title", db=db)

    assert ("The Buff", 2) in result
