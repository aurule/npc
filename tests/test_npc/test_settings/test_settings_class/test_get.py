from npc.settings import Settings

def test_returns_simple_key_value():
    settings = Settings()
    settings.merge_settings({"valid": True})

    result = settings.get("valid", "fail")

    assert result != "fail"

def test_returns_nested_key_value():
    settings = Settings()

    result = settings.get("npc.version", "fail")

    assert result != "fail"

def test_returns_default_with_missing_key():
    settings = Settings()

    result = settings.get("npc.nopealope", "missing")

    assert result == "missing"
