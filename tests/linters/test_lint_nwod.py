"""Tests the helpers for linting generic nwod characters"""

import npc
import pytest
from util import fixture_dir

def test_has_virtue():
    char_file = fixture_dir('linter', 'nwod', 'Has Virtue.nwod')
    with open(char_file, 'r') as char_file:
        problems = npc.linters.nwod.lint_vice_virtue(char_file.read())
        assert 'Missing virtue' not in problems

def test_missing_virtue():
    char_file = fixture_dir('linter', 'nwod', 'Gotta Nada.nwod')
    with open(char_file, 'r') as char_file:
        problems = npc.linters.nwod.lint_vice_virtue(char_file.read())
        assert 'Missing virtue' in problems

def test_has_vice():
    char_file = fixture_dir('linter', 'nwod', 'Has Vice.nwod')
    with open(char_file, 'r') as char_file:
        problems = npc.linters.nwod.lint_vice_virtue(char_file.read())
        assert 'Missing virtue' not in problems

def test_missing_vice():
    char_file = fixture_dir('linter', 'nwod', 'Gotta Nada.nwod')
    with open(char_file, 'r') as char_file:
        problems = npc.linters.nwod.lint_vice_virtue(char_file.read())
        assert 'Missing vice' in problems
