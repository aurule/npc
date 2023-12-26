from npc.settings import MetatagSpec
from npc.characters import Tag

from npc.characters.writer.metatag_class import Metatag

def make_spec() -> MetatagSpec:
    metatag_def = {
        "desc": "A testing tag",
        "static": {
            "test": "yes"
        },
        "match": ["brains", "brawn"],
        "separator": " :: "
    }
    return MetatagSpec("monster", metatag_def)

def test_rejects_non_required_tag():
    metatag = Metatag(make_spec())
    tag = Tag(id=5, name="nope", value="nah")

    metatag.consider(tag)

    assert tag.id not in metatag.tag_ids

def test_rejects_static_with_wrong_value():
    metatag = Metatag(make_spec())
    tag = Tag(id=5, name="test", value="nope")

    metatag.consider(tag)

    assert tag.id not in metatag.tag_ids

def test_rejects_unavailable_tag():
    metatag = Metatag(make_spec())
    tag1 = Tag(id=5, name="test", value="yes")
    tag2 = Tag(id=6, name="test", value="yes")

    metatag.consider(tag1)

    assert tag2.id not in metatag.tag_ids

def test_accepts_tags_with_same_name():
    metatag_def = {
        "desc": "A testing tag",
        "static": {
            "test": "yes"
        },
        "match": ["brains", "brains", "brawn"],
        "separator": " :: "
    }
    spec = MetatagSpec("monster", metatag_def)
    metatag = Metatag(spec)
    tag1 = Tag(id=5, name="brains", value="abby")
    tag2 = Tag(id=6, name="brains", value="normal")

    metatag.consider(tag1)
    metatag.consider(tag2)

    assert tag1.id in metatag.tag_ids
    assert tag2.id in metatag.tag_ids

def test_removes_name_from_open():
    metatag = Metatag(make_spec())
    tag = Tag(id=5, name="test", value="yes")

    metatag.consider(tag)

    assert tag.name not in metatag.open_names

def test_adds_match_value():
    metatag = Metatag(make_spec())
    tag = Tag(id=5, name="brains", value="abby normal")

    metatag.consider(tag)

    assert tag.value in metatag.match_values

def test_recurses_subtags():
    metatag_def = {
        "desc": "A testing tag",
        "static": {
            "employer": "frankie"
        },
        "match": ["job"]
    }
    spec = MetatagSpec("monster", metatag_def)
    metatag = Metatag(spec)
    parent_tag = Tag(id=5, name="employer", value="frankie")
    subtag = Tag(id=6, name="job", value="tester", parent_tag_id=parent_tag.id)
    parent_tag.subtags = [subtag]

    metatag.consider(parent_tag)

    assert subtag.id in metatag.tag_ids


