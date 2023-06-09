from npc.settings import TagSpec
from npc.settings.tags.tag_spec_class import UndefinedTagSpec
from npc.characters import Tag

from npc.validation import TagValidator

def test_replaced_by():
    spec = TagSpec("test", {"replaced_by": "nopealope"})
    tags = [Tag(name="test", value="yes")]
    validator = TagValidator(spec)

    result = validator.validate(tags)

    assert "replaced" in result[0].message

def test_replaced_by_ignores_other_errors():
    spec = TagSpec("test", {"replaced_by": "nopealope"})
    tags = [Tag(name="test")]
    validator = TagValidator(spec)

    result = validator.validate(tags)

    assert len(result) == 1

def test_required():
    spec = TagSpec("test", {"required": True})
    tags = []
    validator = TagValidator(spec)

    result = validator.validate(tags)

    assert "required" in result[0].message

def test_min():
    spec = TagSpec("test", {"min": 2})
    tags = [Tag(name="test", value="eh")]
    validator = TagValidator(spec)

    result = validator.validate(tags)

    assert "too few" in result[0].message

def test_max():
    spec = TagSpec("test", {"max": 1})
    tags = [
        Tag(name="test", value="eh"),
        Tag(name="test", value="meh"),
    ]
    validator = TagValidator(spec)

    result = validator.validate(tags)

    assert "too many" in result[0].message

def test_no_value():
    spec = TagSpec("test", {"no_value": True})
    tags = [Tag(name="test", value="bloop")]
    validator = TagValidator(spec)

    result = validator.validate(tags)

    assert "no value allowed" in result[0].message

def test_bad_value():
    spec = TagSpec("test", {"values": ['yes', 'no']})
    tags = [Tag(name="test", value="eh")]
    validator = TagValidator(spec)

    result = validator.validate(tags)

    assert "unrecognized value" in result[0].message

def test_missing_value():
    spec = TagSpec("test", {"required": False})
    tags = [Tag(name="test")]
    validator = TagValidator(spec)

    result = validator.validate(tags)

    assert "missing value" in result[0].message

def test_allowed_empty_value():
    spec = TagSpec("test", {"allow_empty": True})
    tags = [Tag(name="test")]
    validator = TagValidator(spec)

    result = validator.validate(tags)

    assert not result

def test_undefined():
    spec = UndefinedTagSpec("test")
    tags = [Tag(name="test")]
    validator = TagValidator(spec)
    result = validator.validate(tags)

    assert "no definition" in result[0].message
