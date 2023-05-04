from tests.fixtures import tmp_campaign
from npc.characters import Character
from npc.settings.tags import UndefinedTagSpec, TagSpec

from npc.characters import CharacterFactory

class TestWithoutType():
    def test_does_not_resolve_type_specific_tag(self, tmp_campaign):
        tmp_campaign.patch_campaign_settings({"system": "nwod"})
        factory = CharacterFactory(tmp_campaign)
        character = Character()

        tag_spec = factory.get_tag_spec("seeming", character)

        assert isinstance(tag_spec, UndefinedTagSpec)

    def test_resolves_global_tag(self, tmp_campaign):
        tmp_campaign.patch_campaign_settings({"system": "nwod"})
        factory = CharacterFactory(tmp_campaign)
        character = Character()

        tag_spec = factory.get_tag_spec("age", character)

        assert isinstance(tag_spec, TagSpec)

class TestWithType():
    def test_resolves_type_specific_tag(self, tmp_campaign):
        tmp_campaign.patch_campaign_settings({"system": "nwod"})
        factory = CharacterFactory(tmp_campaign)
        character = Character(type_key="changeling")

        tag_spec = factory.get_tag_spec("seeming", character)

        assert isinstance(tag_spec, TagSpec)

    def test_resolves_global_tag(self, tmp_campaign):
        tmp_campaign.patch_campaign_settings({"system": "nwod"})
        factory = CharacterFactory(tmp_campaign)
        character = Character(type_key="changeling")

        tag_spec = factory.get_tag_spec("age", character)

        assert isinstance(tag_spec, TagSpec)
