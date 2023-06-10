from tests.fixtures import tmp_campaign

from npc.characters import Tag
from npc.linters.tag_bucket import TagBucket
from npc.settings.tags import TagSpec

from npc.linters import CharacterLinter

def test_checks_required_tags(tmp_campaign):
    specs = [TagSpec("test", {"required": True})]
    bucket = TagBucket()
    linter = CharacterLinter(None, tmp_campaign)

    linter.check_tags(bucket, specs)

    err = linter.errors[0]
    assert err.tag_name == "test"
    assert "required" in err.message

def test_checks_deprecated_tags(tmp_campaign):
    specs = []
    bucket = TagBucket()
    bucket.add_tag(Tag(name="hidegroup", value="nopealope"))
    linter = CharacterLinter(None, tmp_campaign)

    linter.check_tags(bucket, specs)

    err = linter.errors[0]
    assert err.tag_name == "hidegroup"
    assert "deprecated" in err.message

def test_checks_remaining_tags(tmp_campaign):
    specs = [TagSpec("test", {"max": 1})]
    bucket = TagBucket()
    bucket.add_tag(Tag(name="test", value="first"))
    bucket.add_tag(Tag(name="test", value="second"))
    linter = CharacterLinter(None, tmp_campaign)

    linter.check_tags(bucket, specs)

    err = linter.errors[0]
    assert err.tag_name == "test"
    assert "too many" in err.message

def test_checks_unknown_tags(tmp_campaign):
    specs = []
    bucket = TagBucket()
    bucket.add_tag(Tag(name="test", value="nope"))
    linter = CharacterLinter(None, tmp_campaign)

    linter.check_tags(bucket, specs)

    err = linter.errors[0]
    assert err.tag_name == "test"
    assert "no definition" in err.message

def test_checks_required_once(tmp_campaign):
    specs = [TagSpec("test", {
        "required": True,
        "values": ["yes", "no", "stahp"]
    })]
    bucket = TagBucket()
    linter = CharacterLinter(None, tmp_campaign)

    linter.check_tags(bucket, specs)

    assert len(linter.errors) == 2

def test_checks_deprecated_once(tmp_campaign):
    specs = []
    bucket = TagBucket()
    bucket.add_tag(Tag(name="hidegroup", value="nopealope"))
    linter = CharacterLinter(None, tmp_campaign)

    linter.check_tags(bucket, specs)

    assert len(linter.errors) == 1
