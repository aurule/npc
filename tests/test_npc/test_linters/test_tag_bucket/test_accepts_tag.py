from npc.linters.tag_bucket import TagBucket

def test_always_accepts():
    bucket = TagBucket(None)

    assert bucket.accepts_tag("whocares")
