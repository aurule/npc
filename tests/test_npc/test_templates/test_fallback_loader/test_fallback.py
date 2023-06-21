from npc.templates import FallbackLoader

def test_uses_template_suffix():
    search = "notfound.html"
    loader = FallbackLoader(None)

    result = loader.fallback(search)

    assert result == "default.html"
