from tests.fixtures import tmp_campaign

from npc.listers import CharacterLister

def test_uses_passed_lang(tmp_campaign):
    lister = CharacterLister(tmp_campaign.characters, lang="test")

    assert lister.lang == "test"

def test_uses_settings_lang(tmp_campaign):
    tmp_campaign.patch_campaign_settings({"characters": {"listing": {"format": "test"}}})

    lister = CharacterLister(tmp_campaign.characters)

    assert lister.lang == "test"

def test_uses_passed_groups(tmp_campaign):
    lister = CharacterLister(tmp_campaign.characters, group_by=["test"])

    assert lister.group_by == ["test"]

def test_uses_settings_groups(tmp_campaign):
    tmp_campaign.patch_campaign_settings({"characters": {"listing": {"group_by": ["test"]}}})

    lister = CharacterLister(tmp_campaign.characters)

    assert lister.group_by == ["test"]

def test_uses_passed_sorts(tmp_campaign):
    lister = CharacterLister(tmp_campaign.characters, sort_by=["test"])

    assert lister.sort_by == ["test"]

def test_uses_settings_sorts(tmp_campaign):
    tmp_campaign.patch_campaign_settings({"characters": {"listing": {"sort_by": ["test"]}}})

    lister = CharacterLister(tmp_campaign.characters)

    assert lister.sort_by == ["test"]

def test_uses_passed_header_level(tmp_campaign):
    lister = CharacterLister(tmp_campaign.characters, base_header_level=3)

    assert lister.base_header_level == 3

def test_uses_settings_header_level(tmp_campaign):
    tmp_campaign.patch_campaign_settings({"characters": {"listing": {"base_header_level": 3}}})

    lister = CharacterLister(tmp_campaign.characters)

    assert lister.base_header_level == 3
