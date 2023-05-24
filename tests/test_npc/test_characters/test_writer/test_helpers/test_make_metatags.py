import pytest
from npc.settings import MetatagSpec
from npc.characters import Character, Tag, CharacterFactory
from npc.db import DB

from npc.characters.writer.helpers import make_metatags

def test_returns_matching_metatag():
    metatag_def = {
        "desc": "A testing tag",
        "static": {
            "test": "yes"
        },
        "match": ["brains", "brawn"],
    }
    metaspec = MetatagSpec("monster", metatag_def)
    character = Character(realname="bumblor", type_key="person", file_loc="/dev/null")
    tag1 = Tag(id=1, name="test", value="yes")
    tag2 = Tag(id=2, name="brains", value="abby normal")
    tag3 = Tag(id=3, name="brawn", value="chonk")
    character.tags = [tag1, tag2, tag3]
    db = DB(clearSingleton=True)
    with db.session() as session:
        session.add(character)
        session.commit()

    result_tags = make_metatags(metaspec, character, [], db=db)

    assert result_tags[0].spec.name == "monster"

def test_returns_used_ids():
    metatag_def = {
        "desc": "A testing tag",
        "static": {
            "test": "yes"
        },
        "match": ["brains", "brawn"],
    }
    metaspec = MetatagSpec("monster", metatag_def)
    character = Character(realname="bumblor", type_key="person", file_loc="/dev/null")
    tag1 = Tag(id=1, name="test", value="yes")
    tag2 = Tag(id=2, name="brains", value="abby normal")
    tag3 = Tag(id=3, name="brawn", value="chonk")
    character.tags = [tag1, tag2, tag3]
    db = DB(clearSingleton=True)
    with db.session() as session:
        session.add(character)
        session.commit()

    result_tags = make_metatags(metaspec, character, [], db=db)

    result_ids = result_tags[0].tag_ids
    assert 1 in result_ids
    assert 2 in result_ids
    assert 3 in result_ids

def test_returns_multiple_metatags_when_greedy():
    metatag_def = {
        "desc": "A testing tag",
        "static": {
            "test": "yes"
        },
        "match": ["brains", "brawn"],
        "greedy": True,
    }
    metaspec = MetatagSpec("monster", metatag_def)
    character = Character(realname="bumblor", type_key="person", file_loc="/dev/null")
    tag1 = Tag(id=1, name="test", value="yes")
    tag2 = Tag(id=2, name="brains", value="abby normal")
    tag3 = Tag(id=3, name="brawn", value="chonk")
    tag4 = Tag(id=4, name="test", value="yes")
    tag5 = Tag(id=5, name="brains", value="mega")
    tag6 = Tag(id=6, name="brawn", value="meh")
    character.tags = [tag1, tag2, tag3, tag4, tag5, tag6]
    db = DB(clearSingleton=True)
    with db.session() as session:
        session.add(character)
        session.commit()

    result_tags = make_metatags(metaspec, character, [], db=db)

    assert result_tags[1].spec.name == "monster"

def test_returns_used_ids_from_multiple():
    metatag_def = {
        "desc": "A testing tag",
        "static": {
            "test": "yes"
        },
        "match": ["brains", "brawn"],
        "greedy": True,
    }
    metaspec = MetatagSpec("monster", metatag_def)
    character = Character(realname="bumblor", type_key="person", file_loc="/dev/null")
    tag1 = Tag(id=1, name="test", value="yes")
    tag2 = Tag(id=2, name="brains", value="abby normal")
    tag3 = Tag(id=3, name="brawn", value="chonk")
    tag4 = Tag(id=4, name="test", value="yes")
    tag5 = Tag(id=5, name="brains", value="mega")
    tag6 = Tag(id=6, name="brawn", value="meh")
    character.tags = [tag1, tag2, tag3, tag4, tag5, tag6]
    db = DB(clearSingleton=True)
    with db.session() as session:
        session.add(character)
        session.commit()

    result_tags = make_metatags(metaspec, character, [], db=db)

    result_ids = result_tags[0].tag_ids
    assert 1 in result_ids
    assert 2 in result_ids
    assert 3 in result_ids

    result_ids = result_tags[1].tag_ids
    assert 4 in result_ids
    assert 5 in result_ids
    assert 6 in result_ids
