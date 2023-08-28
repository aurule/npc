from tests.fixtures import tmp_campaign

def test_true_with_lower_version(tmp_campaign):
    tmp_campaign.settings.versions["campaign"] = "1.9.8"

    assert tmp_campaign.outdated

def test_false_with_equal_version(tmp_campaign):
    assert tmp_campaign.settings.versions["package"] == tmp_campaign.settings.versions["campaign"]

    assert not tmp_campaign.outdated

def test_true_with_missing_version(tmp_campaign):
    tmp_campaign.settings.versions["campaign"] = None

    assert tmp_campaign.outdated
