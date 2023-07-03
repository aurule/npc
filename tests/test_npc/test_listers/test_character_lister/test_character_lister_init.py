from tests.fixtures import tmp_campaign

from npc.listers import CharacterLister

def test_uses_passed_lang(tmp_campaign):
    lister = CharacterLister(tmp_campaign.characters, lang="test")

    assert lister.lang == "test"

def test_uses_settings_lang(tmp_campaign):
    tmp_campaign.patch_campaign_settings({"characters": {"listing": {"format": "test"}}})

    lister = CharacterLister(tmp_campaign.characters)

    assert lister.lang == "test"
