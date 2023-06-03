from npc.settings import TagSpec
from npc.characters import Tag

from npc.validation import TagValidator

def test_replaced_by():
    spec = TagSpec(
        "test",
        {
            "replaced_by": "nopealope",
        })
    tags = [
        Tag(name="test", value="yes"),
    ]
    validator = TagValidator(spec)

    result = validator.validate(tags)

    assert "replaced" in str(result[0])

def test_replaced_by_ignores_other_errors():
    spec = TagSpec(
        "test",
        {
            "replaced_by": "nopealope",
        })
    tags = [
        Tag(name="test"),
    ]
    validator = TagValidator(spec)

    result = validator.validate(tags)

    assert len(result) == 1

def test_required():
    spec = TagSpec(
        "test",
        {
            "required": True,
        })
    tags = [
    ]
    validator = TagValidator(spec)

    result = validator.validate(tags)

    assert "required" in str(result[0])

def test_min():
    spec = TagSpec(
        "test",
        {
            "min": 2,
        })
    tags = [
        Tag(name="test", value="eh"),
    ]
    validator = TagValidator(spec)

    result = validator.validate(tags)

    assert "too few" in str(result[0])

def test_max():
    spec = TagSpec(
        "test",
        {
            "max": 1,
        })
    tags = [
        Tag(name="test", value="eh"),
        Tag(name="test", value="meh"),
    ]
    validator = TagValidator(spec)

    result = validator.validate(tags)

    assert "too many" in str(result[0])

def test_no_value():
    spec = TagSpec(
        "test",
        {
            "no_value": True,
        })
    tags = [
        Tag(name="test", value="bloop"),
    ]
    validator = TagValidator(spec)

    result = validator.validate(tags)

    assert "no value allowed" in str(result[0])

def test_bad_value():
    spec = TagSpec(
        "test",
        {
            "values": ['yes', 'no'],
        })
    tags = [
        Tag(name="test", value="eh"),
    ]
    validator = TagValidator(spec)

    result = validator.validate(tags)

    assert "unrecognized value" in str(result[0])

def test_missing_value():
    spec = TagSpec(
        "test",
        {
        })
    tags = [
        Tag(name="test"),
    ]
    validator = TagValidator(spec)

    result = validator.validate(tags)

    assert "missing value" in str(result[0])

def test_allowed_empty_value():
    spec = TagSpec(
        "test",
        {
            "allow_empty": True,
        })
    tags = [
        Tag(name="test"),
    ]
    validator = TagValidator(spec)

    result = validator.validate(tags)

    assert not result
