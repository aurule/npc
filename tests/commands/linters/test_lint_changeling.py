"""Tests the linting of changeling-specific tags"""

import npc
import pytest
import os
from tests.util import fixture_dir

@pytest.fixture
def lint_output():
    def do_lint(charname, strict=False):
        search = fixture_dir('linter', 'characters', 'Changelings', charname)
        result = npc.commands.lint(search, strict=strict)
        return "\n".join(result.printables)
    return do_lint

@pytest.mark.parametrize('charname', ['No Kith.nwod', 'No Kith Also.nwod'])
def test_seeming_present(lint_output, charname):
    assert "Missing kith" in lint_output(charname)

def test_seeming_info_present(lint_output):
    assert "Missing notes for Seeming" in lint_output('No Info.nwod')

def test_seeming_info_correct(lint_output):
    assert "Incorrect notes for Seeming" in lint_output('Bad Info.nwod')

def test_kith_present(lint_output):
    assert "Missing seeming" in lint_output('No Seeming.nwod')

def test_kith_info_present(lint_output):
    assert "Missing notes for Kith" in lint_output('No Info.nwod')

def test_kith_info_correct(lint_output):
    assert "Incorrect notes for Kith" in lint_output('Bad Info.nwod')

def test_unknown_kith(lint_output):
    assert "Unrecognized @kith" in lint_output('Unknown Kith.nwod')

def test_multiple_courts(lint_output):
    assert "Multiple courts" in lint_output('Many Courts.nwod')

def test_multiple_motleys(lint_output):
    assert "Multiple motleys" in lint_output('Many Motleys.nwod')

def test_multiple_mantles(lint_output):
    assert "Multiple mantle" in lint_output('Many Mantles.nwod')

def test_wrong_mantle(lint_output):
    assert "Court mantle 'Winter' does not match court tag 'Summer'" in lint_output('Wrong Mantle.nwod')

def test_goodwill_vs_court(lint_output):
    assert "Court goodwill listed for court tag 'Winter'" in lint_output('Goodwill.nwod')

def test_goodwill_vs_mantle(lint_output):
    assert "Court goodwill listed for court mantle 'Winter'" in lint_output('Goodwill.nwod')

def test_court_no_mantle(lint_output):
    assert "No mantle for court 'Winter'" in lint_output('No Mantle.nwod', strict=True)

def test_unseen_sense(lint_output):
    assert "Changelings cannot have the Unseen Sense merit" in lint_output('Unseen Sense.nwod', strict=True)

def test_virtue(lint_output):
    assert "Missing virtue" in lint_output('No Virtue.nwod', strict=True)

def test_vice(lint_output):
    assert "Missing vice" in lint_output('No Vice.nwod', strict=True)
