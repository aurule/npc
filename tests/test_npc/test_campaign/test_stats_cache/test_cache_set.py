from tests.fixtures import tmp_campaign

from npc.campaign.stats_cache import StatsCache

def test_saves_file(tmp_campaign):
    cache = StatsCache(tmp_campaign)

    cache.set("fiddlesticks", "somewhat")

    with cache.cache_file_path.open("r") as f:
        contents = f.read()
    assert "fiddlesticks" in contents
