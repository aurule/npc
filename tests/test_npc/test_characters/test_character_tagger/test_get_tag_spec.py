from tests.fixtures import tmp_campaign
from npc.characters import Character
from npc.settings.tags import UndefinedTagSpec, TagSpec

from npc.characters import CharacterTagger

class TestWithoutType():
    def test_does_not_resolve_type_specific_tag(self, tmp_campaign):
        tmp_campaign.patch_campaign_settings({"system": "nwod"})
        character = Character()
        tagger = CharacterTagger(tmp_campaign, character)

        tag_spec = tagger.get_tag_spec("seeming")

        assert isinstance(tag_spec, UndefinedTagSpec)

    def test_resolves_global_tag(self, tmp_campaign):
        tmp_campaign.patch_campaign_settings({"system": "nwod"})
        character = Character()
        tagger = CharacterTagger(tmp_campaign, character)

        tag_spec = tagger.get_tag_spec("age")

        assert isinstance(tag_spec, TagSpec)

    def test_treats_default_type_as_unset(self, tmp_campaign):
        tmp_campaign.patch_campaign_settings({"system": "nwod"})
        character = Character(type_key=Character.DEFAULT_TYPE)
        tagger = CharacterTagger(tmp_campaign, character)

        tag_spec = tagger.get_tag_spec("seeming")

        assert isinstance(tag_spec, UndefinedTagSpec)

class TestWithType():
    def test_resolves_type_specific_tag(self, tmp_campaign):
        tmp_campaign.patch_campaign_settings({"system": "nwod"})
        character = Character(type_key="changeling")
        tagger = CharacterTagger(tmp_campaign, character)

        tag_spec = tagger.get_tag_spec("seeming")

        assert isinstance(tag_spec, TagSpec)

    def test_resolves_global_tag(self, tmp_campaign):
        tmp_campaign.patch_campaign_settings({"system": "nwod"})
        character = Character(type_key="changeling")
        tagger = CharacterTagger(tmp_campaign, character)

        tag_spec = tagger.get_tag_spec("age")

        assert isinstance(tag_spec, TagSpec)
