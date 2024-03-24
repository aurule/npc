from tests.fixtures import tmp_campaign

def test_gets_the_dir(tmp_campaign):
    root = tmp_campaign.root

    assert tmp_campaign.cache_dir == root / ".npc" / "cache"

def test_creates_the_dir(tmp_campaign):
    root = tmp_campaign.root
    target = root / ".npc" / "cache"

    tmp_campaign.cache_dir

    assert target.exists()
