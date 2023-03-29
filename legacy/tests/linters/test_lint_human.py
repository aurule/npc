"""Tests the linting of human-specific tags"""

import npc
import pytest
from util import fixture_dir

def lint_human(filename, **kwargs):
    prefs = npc.settings.Settings()
    char_file = fixture_dir('linter', 'human', filename)
    character = npc.parser.parse_character(char_file)
    problems = npc.linters.human.lint(character, **kwargs)
    return problems

def test_requires_path():
    character = npc.character.Character()
    problems = npc.linters.human.lint(character)
    assert 'Missing path' in problems

class TestViceAndVirtue:
    @pytest.mark.parametrize("strict,is_problem", [
                             (True, False),
                             (False, False),
                             ])
    def test_has_virtue(self, prefs, strict, is_problem):
        problems = lint_human('Has Virtue.nwod', strict=strict)
        assert ('Missing virtue' in problems) == is_problem

    @pytest.mark.parametrize("strict,is_problem", [
                             (True, True),
                             (False, False),
                             ])
    def test_missing_virtue(self, prefs, strict, is_problem):
        problems = lint_human('Gotta Nada.nwod', strict=strict)
        assert ('Missing virtue' in problems) == is_problem

    @pytest.mark.parametrize("strict,is_problem", [
                             (True, False),
                             (False, False),
                             ])
    def test_has_vice(self, prefs, strict, is_problem):
        problems = lint_human('Has Vice.nwod', strict=strict)
        assert ('Missing vice' in problems) == is_problem

    @pytest.mark.parametrize("strict,is_problem", [
                             (True, True),
                             (False, False),
                             ])
    def test_missing_vice(self, prefs, strict, is_problem):
        problems = lint_human('Gotta Nada.nwod', strict=strict)
        assert ('Missing vice' in problems) == is_problem
