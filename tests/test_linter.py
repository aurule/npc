import npc
import pytest
import os
from tests.util import fixture_dir

@pytest.fixture
def lint_output(capsys):
    def do_lint(charname):
        search = fixture_dir(['linter', 'characters', 'Humans', charname])
        npc.commands.lint(search)
        output, _ = capsys.readouterr()
        return output
    return do_lint

def test_requires_type(lint_output):
    assert "Missing type" in lint_output('Gotta Nada.nwod')

@pytest.mark.parametrize('charname', ['Gotta Nada.nwod', 'Gotta Type.nwod'])
def test_requires_description(lint_output, charname):
    assert "Missing description" in lint_output(charname)

class TestChangeling:
    """Tests the linting of changeling-specific tags"""

    @pytest.fixture
    def lint_output(self, capsys):
        def do_lint(charname):
            search = fixture_dir(['linter', 'characters', 'Changelings', charname])
            npc.commands.lint(search)
            output, _ = capsys.readouterr()
            return output
        return do_lint

    @pytest.mark.parametrize('charname', ['No Kith.nwod', 'No Kith Also.nwod'])
    def test_seeming_present(self, lint_output, charname):
        assert "Missing kith" in lint_output(charname)

    def test_seeming_info_present(self, lint_output):
        assert "Missing notes for Seeming" in lint_output('No Info.nwod')

    def test_seeming_info_correct(self, lint_output):
        assert "Incorrect notes for Seeming" in lint_output('Bad Info.nwod')

    def test_kith_present(self, lint_output):
        assert "Missing seeming" in lint_output('No Seeming.nwod')

    def test_kith_info_present(self, lint_output):
        assert "Missing notes for Kith" in lint_output('No Info.nwod')

    def test_kith_info_correct(self, lint_output):
        assert "Incorrect notes for Kith" in lint_output('Bad Info.nwod')

    def test_multiple_courts(self, lint_output):
        assert "Multiple courts" in lint_output('Many Courts.nwod')

    def test_multiple_motleys(self, lint_output):
        assert "Multiple motleys" in lint_output('Many Motleys.nwod')

    def test_multiple_mantles(self, lint_output):
        assert "Multiple mantle" in lint_output('Many Mantles.nwod')

    def test_wrong_mantle(self, lint_output):
        assert "Court mantle 'Winter' does not match court tag 'Summer'" in lint_output('Wrong Mantle.nwod')

    def test_goodwill_vs_court(self, lint_output):
        assert "Court goodwill listed for court tag 'Winter'" in lint_output('Goodwill.nwod')

    def test_goodwill_vs_mantle(self, lint_output):
        assert "Court goodwill listed for court mantle 'Winter'" in lint_output('Goodwill.nwod')
