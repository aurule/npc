from click import get_app_dir

from npc.settings import app_settings

def test_creates_settings_with_detected_user_dir():
    settings = app_settings()

    assert str(settings.personal_dir) == get_app_dir("NPC")
