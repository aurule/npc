from tests.fixtures import tmp_campaign

from npc.settings.tags import TagSpec
from npc.characters import Character, Tag
from npc.campaign import Campaign
from npc.settings.tags import make_tags

from npc.linters import CharacterLinter

def test_gathers_tag_errors(tmp_campaign):
    linter = CharacterLinter(None, tmp_campaign)
    spec = TagSpec("test", {"required": True})
    tags = []

    linter.validate_spec(spec, tags)

    assert "required" in linter.errors[0].message

tag_defs = {
    "first": {
        "desc": "First tag",
        "subtags": {
            "primero": {
                "desc": "First of firsts",
                "max": 1,
            },
            "segundo": {
                "desc": "Second of firsts",
                "max": 1,
                "subtags": {
                    "tercero": {
                        "desc": "First of seconds",
                        "max": 1,
                    }
                }
            }
        }
    }
}

def test_gathers_errors_for_first_subtag(tmp_campaign):
    tmp_campaign.patch_campaign_settings({"tags": tag_defs})
    linter = CharacterLinter(None, tmp_campaign)
    tags = [
        Tag(
            name="first",
            value="the first one",
            subtags=[
                Tag(name="primero", value="yesplz"),
                Tag(name="primero", value="noplz"),
            ]
        )
    ]
    spec = tmp_campaign.get_tag("first")

    linter.validate_spec(spec, tags)

    assert "primero" == linter.errors[0].tag_name
    assert "too many" in linter.errors[0].message

def test_gathers_errors_for_second_subtag(tmp_campaign):
    tmp_campaign.patch_campaign_settings({"tags": tag_defs})
    linter = CharacterLinter(None, tmp_campaign)
    tags = [
        Tag(
            name="first",
            value="the first one",
            subtags=[
                Tag(name="segundo", value="yesplz"),
                Tag(name="segundo", value="noplz"),
            ]
        )
    ]
    spec = tmp_campaign.get_tag("first")

    linter.validate_spec(spec, tags)

    assert "segundo" == linter.errors[0].tag_name
    assert "too many" in linter.errors[0].message

def test_gathers_errors_for_nested_subtag(tmp_campaign):
    tmp_campaign.patch_campaign_settings({"tags": tag_defs})
    linter = CharacterLinter(None, tmp_campaign)
    tags = [
        Tag(name="first",
            value="the first one",
            subtags=[
                Tag(name="segundo",
                    value="yesplz",
                    subtags=[
                        Tag(name="tercero", value="yesplz"),
                        Tag(name="tercero", value="noplz"),
                    ]
                )
            ]
        )
    ]
    spec = tmp_campaign.get_tag("first")

    linter.validate_spec(spec, tags)

    assert "tercero" == linter.errors[0].tag_name
    assert "too many" in linter.errors[0].message
