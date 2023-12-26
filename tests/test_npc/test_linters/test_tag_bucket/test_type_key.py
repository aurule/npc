from npc.characters import Character

from npc.linters.tag_bucket import TagBucket

def test_default_key_gives_none():
    character = Character(type_key=Character.DEFAULT_TYPE)
    bucket = TagBucket(character)

    assert bucket.type_key is None

def test_returns_normal_key():
    character = Character(type_key="something")
    bucket = TagBucket(character)

    assert bucket.type_key == "something"
