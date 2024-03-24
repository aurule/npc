from tests.fixtures import tmp_campaign

def test_gets_the_dir(tmp_campaign):
    root = tmp_campaign.root

    assert tmp_campaign.cache_dir == root / ".npc" / "cache"
