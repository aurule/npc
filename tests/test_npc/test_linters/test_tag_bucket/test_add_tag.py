from npc.characters import Tag

from npc.linters.tag_bucket import TagBucket

def test_puts_in_empty_list():
    bucket = TagBucket(None)
    tag = Tag(name="test", value="yes")

    bucket.add_tag(tag)

    assert tag in bucket.tags["test"]

def test_puts_in_populated_list():
    bucket = TagBucket(None)
    tag_old = Tag(name="test", value="yuppers")
    bucket.add_tag(tag_old)
    tag = Tag(name="test", value="yes")

    bucket.add_tag(tag)

    assert tag in bucket.tags["test"]
