"""Tests the lint command"""

import npc
import pytest
from tests.util import fixture_dir

# returns openables and printables from the underlying linter
# report option suppresses openables

def test_returns_linter_artifacts():
    result = npc.commands.lint(fixture_dir('linter'))
    assert len(result.openable) > 0
    assert len(result.printables) > 0

def test_report_suppresses_openables():
    result = npc.commands.lint(fixture_dir('linter'), report=True)
    assert len(result.openable) == 0
    assert len(result.printables) > 0
