from tests.fixtures import db
from npc.characters import Character, Tag

from npc.characters.writer.helpers import make_hide_tags

def test_makes_hide_all_top_level(db):
    character = Character(realname="bumblor", type_key="person", file_loc="/dev/null")
    tag1 = Tag(id=1, name="test", value="yes")
    tag2 = Tag(id=2, name="brains", value="abby normal", hidden="all")
    tag3 = Tag(id=3, name="brawn", value="chonk")
    character.tags = [tag1, tag2, tag3]
    with db.session() as session:
        session.add(character)
        session.commit()

    result_tags = make_hide_tags(character, db=db)

    assert result_tags[0].value == "brains"

def test_makes_hide_all_nested(db):
    character = Character(realname="bumblor", type_key="person", file_loc="/dev/null")
    tag1 = Tag(id=1, name="test", value="yes")
    tag2 = Tag(id=2, name="brains", value="abby normal")
    tag3 = Tag(id=3, name="nerd", value="nah", hidden="all", parent_tag_id=2)
    tag3 = Tag(id=4, name="brawn", value="chonk")
    character.tags = [tag1, tag2, tag3]
    with db.session() as session:
        session.add(character)
        session.commit()

    result_tags = make_hide_tags(character, db=db)

    assert result_tags[0].value == "brains >> abby normal >> nerd"

def test_makes_hide_one_top_level(db):
    character = Character(realname="bumblor", type_key="person", file_loc="/dev/null")
    tag1 = Tag(id=1, name="test", value="yes")
    tag2 = Tag(id=2, name="brains", value="abby normal", hidden="one")
    tag3 = Tag(id=3, name="brawn", value="chonk")
    character.tags = [tag1, tag2, tag3]
    with db.session() as session:
        session.add(character)
        session.commit()

    result_tags = make_hide_tags(character, db=db)

    assert result_tags[0].value == "brains >> abby normal"

def test_makes_hide_one_nested(db):
    # TODO make nerd a subtag of brains
    character = Character(realname="bumblor", type_key="person", file_loc="/dev/null")
    tag1 = Tag(id=1, name="test", value="yes")
    tag2 = Tag(id=2, name="brains", value="abby normal")
    tag3 = Tag(id=3, name="nerd", value="nah", hidden="one", parent_tag_id=2)
    tag3 = Tag(id=4, name="brawn", value="chonk")
    character.tags = [tag1, tag2, tag3]
    with db.session() as session:
        session.add(character)
        session.commit()

    result_tags = make_hide_tags(character, db=db)

    assert result_tags[0].value == "brains >> abby normal >> nerd >> nah"
