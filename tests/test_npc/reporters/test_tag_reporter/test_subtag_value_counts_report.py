from npc.characters import Tag, CharacterFactory, RawTag
from tests.fixtures import tmp_campaign, db

from npc.reporters.tag_reporter import subtag_value_counts_report

def seed(db, campaign):
    factory = CharacterFactory(campaign)
    char1 = factory.make("Test Mann", type_key="person", tags=[RawTag("org", "Buff"), RawTag("role", "Sure")])
    char2 = factory.make("Testier Mann", type_key="person", tags=[RawTag("org", "Buff"), RawTag("role", "Whynot")])
    char3 = factory.make("Testiest Mann", type_key="person", tags=[RawTag("group", "Burly"), RawTag("role", "Sure")])
    with db.session() as session:
        session.add(char1)
        session.add(char2)
        session.add(char3)
        session.commit()

def test_counts_subtags(tmp_campaign, db):
    seed(db, tmp_campaign)

    result = subtag_value_counts_report("role", "org", db=db)

    assert ("Sure", 1) in result
