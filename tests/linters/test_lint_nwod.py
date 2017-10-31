import npc
import pytest
import os
from tests.util import fixture_dir

def test_has_virtue():
    char_file = fixture_dir('linter', 'nwod', 'Gotta Nada.nwod')
    with open(char_file, 'r') as char_file:
        problems = npc.linters.nwod.lint_vice_virtue(char_file.read())
        assert 'Missing virtue' in problems

def test_has_vice():
    char_file = fixture_dir('linter', 'nwod', 'Gotta Nada.nwod')
    with open(char_file, 'r') as char_file:
        problems = npc.linters.nwod.lint_vice_virtue(char_file.read())
        assert 'Missing vice' in problems
