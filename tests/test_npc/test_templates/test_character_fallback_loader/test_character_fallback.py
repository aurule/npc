from tests.fixtures import tmp_campaign

from npc.templates import CharacterFallbackLoader

def test_uses_given_stem(tmp_campaign):
    search = "notfound.html"
    loader = CharacterFallbackLoader(tmp_campaign)

    result = loader.fallback(search)

    assert result == "character.html"
