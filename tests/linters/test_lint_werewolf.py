"""Tests the linting of werewolf-specific tags"""

import npc
import pytest
from tests.util import fixture_dir

def lint_werewolf(filename, **kwargs):
    prefs = npc.settings.Settings()
    char_file = fixture_dir('linter', 'werewolf', filename)
    character = npc.parser.parse_character(char_file)
    problems = npc.linters.werewolf.lint(character, prefs=prefs, **kwargs)
    return problems

def test_requires_path(prefs):
    character = npc.character.Werewolf()
    problems = npc.linters.werewolf.lint(character, prefs=prefs)
    assert 'Missing path' in problems

class TestViceAndVirtue:
    @pytest.mark.parametrize("strict,is_problem", [
                             (True, False),
                             (False, False),
                             ])
    def test_has_virtue(self, strict, is_problem):
        problems = lint_werewolf('Has Virtue.nwod', strict=strict)
        assert ('Missing virtue' in problems) == is_problem

    @pytest.mark.parametrize("strict,is_problem", [
                             (True, True),
                             (False, False),
                             ])
    def test_missing_virtue(self, strict, is_problem):
        problems = lint_werewolf('Gotta Nada.nwod', strict=strict)
        assert ('Missing virtue' in problems) == is_problem

    @pytest.mark.parametrize("strict,is_problem", [
                             (True, False),
                             (False, False),
                             ])
    def test_has_vice(self, strict, is_problem):
        problems = lint_werewolf('Has Vice.nwod', strict=strict)
        assert ('Missing vice' in problems) == is_problem

    @pytest.mark.parametrize("strict,is_problem", [
                             (True, True),
                             (False, False),
                             ])
    def test_missing_vice(self, strict, is_problem):
        problems = lint_werewolf('Gotta Nada.nwod', strict=strict)
        assert ('Missing vice' in problems) == is_problem

def test_tribe_not_recognized():
    problems = lint_werewolf('Bad Tribe.nwod')
    assert "Unrecognized tribe 'Go Pats'" in problems

class TestAuspiceNotPresent:
    def test_moon_tribe_adds_error(self):
        problems = lint_werewolf('No Auspice.nwod')
        assert "Missing auspice" in problems

class TestAuspicePresent:
    def test_pure_tribe_adds_error(self):
        problems = lint_werewolf('Pure with Auspice.nwod')
        assert "Auspice present, but werewolf is Pure" in problems

    def test_pure_tribe_adds_error(self):
        problems = lint_werewolf('Bad Auspice.nwod')
        assert "Unrecognized auspice 'Crazy Town'" in problems
