from npc.settings import Settings

def test_gets_deprecated_tags():
	settings = Settings()

	assert "hidegroup" in settings.deprecated_tags
