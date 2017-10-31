"""Tests the linting of human-specific tags"""

import npc
import pytest
import os
import functools
from tests.util import fixture_dir

lint_strict = functools.partial(npc.linters.human.lint, strict=True)

def test_requires_path():
    character = npc.Character()
    problems = npc.linters.human.lint(character)
    assert 'Missing path' in problems

class TestStrictHumanLinting:
    def test_has_virtue(self):
        char_file = fixture_dir('linter', 'human', 'Gotta Nada.nwod')
        character = npc.parser.parse_character(char_file)
        problems = lint_strict(character)
        assert 'Missing virtue' in problems

    def test_has_vice(self):
        char_file = fixture_dir('linter', 'human', 'Gotta Nada.nwod')
        character = npc.parser.parse_character(char_file)
        problems = lint_strict(character)
        assert 'Missing vice' in problems
