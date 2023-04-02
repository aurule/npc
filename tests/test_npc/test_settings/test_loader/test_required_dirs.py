from npc.settings import Settings

def test_has_no_extra_paths():
	settings = Settings()

	assert len(settings.required_dirs) == 3

def test_includes_characters_path():
	settings = Settings()

	assert settings.get("campaign.characters.path") in settings.required_dirs

def test_includes_session_path():
	settings = Settings()

	assert settings.get("campaign.session.path") in settings.required_dirs

def test_includes_plot_path():
	settings = Settings()

	assert settings.get("campaign.plot.path") in settings.required_dirs
