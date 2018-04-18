"""Tests the linting of human-specific tags"""

import npc
import pytest
import os
import functools
from tests.util import fixture_dir

def test_requires_path():
    character = npc.Character()
    problems = npc.linters.human.lint(character)
    assert 'Missing path' in problems

class TestViceAndVirtue:
    @pytest.mark.parametrize("strict,is_problem", [
                             (True, False),
                             (False, False),
                             ])
    def test_has_virtue(self, prefs, strict, is_problem):
        char_file = fixture_dir('linter', 'human', 'Has Virtue.nwod')
        character = npc.parser.parse_character(char_file)
        problems = npc.linters.human.lint(character, strict=strict)
        assert ('Missing virtue' in problems) == is_problem

    @pytest.mark.parametrize("strict,is_problem", [
                             (True, True),
                             (False, False),
                             ])
    def test_missing_virtue(self, prefs, strict, is_problem):
        char_file = fixture_dir('linter', 'human', 'Gotta Nada.nwod')
        character = npc.parser.parse_character(char_file)
        problems = npc.linters.human.lint(character, strict=strict)
        assert ('Missing virtue' in problems) == is_problem

    @pytest.mark.parametrize("strict,is_problem", [
                             (True, False),
                             (False, False),
                             ])
    def test_has_vice(self, prefs, strict, is_problem):
        char_file = fixture_dir('linter', 'human', 'Has Vice.nwod')
        character = npc.parser.parse_character(char_file)
        problems = npc.linters.human.lint(character, strict=strict)
        assert ('Missing vice' in problems) == is_problem

    @pytest.mark.parametrize("strict,is_problem", [
                             (True, True),
                             (False, False),
                             ])
    def test_missing_vice(self, prefs, strict, is_problem):
        char_file = fixture_dir('linter', 'human', 'Gotta Nada.nwod')
        character = npc.parser.parse_character(char_file)
        problems = npc.linters.human.lint(character, strict=strict)
        assert ('Missing vice' in problems) == is_problem
