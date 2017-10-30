"""Tests the linting of human-specific tags"""

import npc
import pytest
import os
from tests.util import fixture_dir

@pytest.fixture
def lint_output():
    def do_lint(charname, strict=False):
        search = fixture_dir('linter', 'characters', 'Humans', charname)
        result = npc.commands.lint(search, strict=strict)
        return "\n".join(result.printables)
    return do_lint

def test_virtue(lint_output):
    assert "Missing virtue" in lint_output('No Virtue.nwod', strict=True)

def test_vice(lint_output):
    assert "Missing vice" in lint_output('No Vice.nwod', strict=True)

