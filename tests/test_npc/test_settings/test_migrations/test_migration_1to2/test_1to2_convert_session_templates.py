from tests.fixtures import tmp_campaign

from npc.settings import Settings
from npc.util import DataStore

from npc.settings.migrations.migration_1to2 import Migration1to2

class TestConvertsSession:
    def test_no_key_no_file_skips(self, tmp_campaign):
        migration = Migration1to2(tmp_campaign.settings)
        old_data = DataStore()

        new_data = migration.convert_session_templates("campaign", old_data)

        assert not new_data.get("campaign.session.filename_pattern")
        assert not new_data.get("campaign.session.file_contents")

    def test_no_key_yes_file_skips(self, tmp_campaign):
        old_template = tmp_campaign.settings_dir / "session NN.md"
        old_template.touch()
        migration = Migration1to2(tmp_campaign.settings)
        old_data = DataStore()

        new_data = migration.convert_session_templates("campaign", old_data)

        assert not new_data.get("campaign.session.filename_pattern")
        assert not new_data.get("campaign.session.file_contents")

    def test_yes_key_no_file_skips(self, tmp_campaign):
        migration = Migration1to2(tmp_campaign.settings)
        old_data = DataStore()
        old_data.set("story.templates.session", "session NN.md")

        new_data = migration.convert_session_templates("campaign", old_data)

        assert new_data.get("campaign.session.filename_pattern")
        assert not new_data.get("campaign.session.file_contents")

    def test_sets_file_name(self, tmp_campaign):
        old_template = tmp_campaign.settings_dir / "session NN.md"
        with old_template.open('w') as f:
            f.write("test things")
        migration = Migration1to2(tmp_campaign.settings)
        old_data = DataStore()
        old_data.set("story.templates.session", "session NN.md")

        new_data = migration.convert_session_templates("campaign", old_data)

        assert new_data.get("campaign.session.filename_pattern")

    def test_subs_num_placeholder(self, tmp_campaign):
        old_template = tmp_campaign.settings_dir / "session NN.md"
        with old_template.open('w') as f:
            f.write("test things")
        migration = Migration1to2(tmp_campaign.settings)
        old_data = DataStore()
        old_data.set("story.templates.session", "session NN.md")

        new_data = migration.convert_session_templates("campaign", old_data)

        assert new_data.get("campaign.session.filename_pattern") == "session ((NN)).md"

    def test_saves_contents(self, tmp_campaign):
        old_template = tmp_campaign.settings_dir / "session NN.md"
        with old_template.open('w') as f:
            f.write("test things")
        migration = Migration1to2(tmp_campaign.settings)
        old_data = DataStore()
        old_data.set("story.templates.session", "session NN.md")

        new_data = migration.convert_session_templates("campaign", old_data)

        assert new_data.get("campaign.session.file_contents") == "test things"

class TestConvertsPlot:
    def test_no_key_no_file_skips(self, tmp_campaign):
        migration = Migration1to2(tmp_campaign.settings)
        old_data = DataStore()

        new_data = migration.convert_session_templates("campaign", old_data)

        assert not new_data.get("campaign.plot.filename_pattern")
        assert not new_data.get("campaign.plot.file_contents")

    def test_no_key_yes_file_skips(self, tmp_campaign):
        old_template = tmp_campaign.settings_dir / "plot NN.md"
        old_template.touch()
        migration = Migration1to2(tmp_campaign.settings)
        old_data = DataStore()

        new_data = migration.convert_session_templates("campaign", old_data)

        assert not new_data.get("campaign.plot.filename_pattern")
        assert not new_data.get("campaign.plot.file_contents")

    def test_yes_key_no_file_skips(self, tmp_campaign):
        migration = Migration1to2(tmp_campaign.settings)
        old_data = DataStore()
        old_data.set("story.templates.plot", "plot NN.md")

        new_data = migration.convert_session_templates("campaign", old_data)

        assert new_data.get("campaign.plot.filename_pattern")
        assert not new_data.get("campaign.plot.file_contents")

    def test_sets_file_name(self, tmp_campaign):
        old_template = tmp_campaign.settings_dir / "plot NN.md"
        with old_template.open('w') as f:
            f.write("test things")
        migration = Migration1to2(tmp_campaign.settings)
        old_data = DataStore()
        old_data.set("story.templates.plot", "plot NN.md")

        new_data = migration.convert_session_templates("campaign", old_data)

        assert new_data.get("campaign.plot.filename_pattern")

    def test_subs_num_placeholder(self, tmp_campaign):
        old_template = tmp_campaign.settings_dir / "plot NN.md"
        with old_template.open('w') as f:
            f.write("test things")
        migration = Migration1to2(tmp_campaign.settings)
        old_data = DataStore()
        old_data.set("story.templates.plot", "plot NN.md")

        new_data = migration.convert_session_templates("campaign", old_data)

        assert new_data.get("campaign.plot.filename_pattern") == "plot ((NN)).md"

    def test_saves_contents(self, tmp_campaign):
        old_template = tmp_campaign.settings_dir / "plot NN.md"
        with old_template.open('w') as f:
            f.write("test things")
        migration = Migration1to2(tmp_campaign.settings)
        old_data = DataStore()
        old_data.set("story.templates.plot", "plot NN.md")

        new_data = migration.convert_session_templates("campaign", old_data)

        assert new_data.get("campaign.plot.file_contents") == "test things"
