from tests.fixtures import tmp_campaign

from npc_cli.presenters import campaign_info

def test_includes_label(tmp_campaign):
    result = campaign_info(tmp_campaign)

    assert "Campaign Info" in result

def test_shows_name(tmp_campaign):
    result = campaign_info(tmp_campaign)

    assert tmp_campaign.name in result

def test_shows_description(tmp_campaign):
    tmp_campaign.patch_campaign_settings({"desc": "I am a test"})

    result = campaign_info(tmp_campaign)

    assert tmp_campaign.desc in result

def test_shows_system_name(tmp_campaign):
    result = campaign_info(tmp_campaign)

    assert "Generic" in result
