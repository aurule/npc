"""Tests the linting of changeling-specific tags"""

import npc
import pytest
from util import fixture_dir

def lint_changeling(filename, **kwargs):
    prefs = npc.settings.Settings()
    char_file = fixture_dir('linter', 'changeling', filename)
    character = npc.parser.parse_character(char_file)
    problems = npc.linters.changeling.lint(character, sk_data=prefs.get('changeling'), **kwargs)
    return '/'.join(problems)

def test_no_path():
    prefs = npc.settings.Settings()
    character = npc.character.Character({"type": ['changeling'], "kith": ['nope'], "seeming": ['nope']})
    problems = npc.linters.changeling.lint(character, sk_data=prefs.get('changeling'))
    assert problems

class TestSeeming:
    def test_no_tag(self):
        problems = lint_changeling('No Seeming or Kith.nwod')
        assert not problems

    def test_known_seeming(self):
        problems = lint_changeling('Known Seeming.nwod')
        assert "Unrecognized @seeming" not in problems

    def test_unknown_seeming(self):
        problems = lint_changeling('Unknown Seeming.nwod')
        assert "Unrecognized @seeming" in problems

    def test_seeming_info_present(self):
        problems = lint_changeling('Has Info.nwod')
        assert "Seeming stats do not match @seeming tags" not in problems

    def test_seeming_info_not_present(self):
        problems = lint_changeling('No Info.nwod')
        assert "Seeming stats do not match @seeming tags" in problems

    def test_seeming_info_correct(self):
        problems = lint_changeling('Has Info.nwod')
        assert "Incorrect notes for Seeming" not in problems

    def test_seeming_info_incorrect(self):
        problems = lint_changeling('Bad Info.nwod')
        assert "Incorrect notes for Seeming" in problems

class TestKith:
    def test_no_tag(self):
        problems = lint_changeling('No Seeming or Kith.nwod')
        assert not problems

    def test_known_kith(self):
        problems = lint_changeling('Known Kith.nwod')
        assert "Unrecognized @kith" not in problems

    def test_unknown_kith(self):
        problems = lint_changeling('Unknown Kith.nwod')
        assert "Unrecognized @kith" in problems

    def test_kith_info_present(self):
        problems = lint_changeling('Has Info.nwod')
        assert "Kith stats do not match @kith tags" not in problems

    def test_kith_info_not_present(self):
        problems = lint_changeling('No Info.nwod')
        assert "Kith stats do not match @kith tags" in problems

    def test_kith_info_correct(self):
        problems = lint_changeling('Has Info.nwod')
        assert "Incorrect notes for Kith" not in problems

    def test_kith_info_incorrect(self):
        problems = lint_changeling('Bad Info.nwod')
        assert "Incorrect notes for Kith" in problems

class TestMantle:
    def test_allows_one_mantle(self):
        problems = lint_changeling('One Mantle.nwod')
        assert "Multiple mantle" not in problems

    def test_multiple_mantles(self):
        problems = lint_changeling('Many Mantles.nwod')
        assert "Multiple mantle" in problems

    def test_mantle_merit_matches_tag(self):
        problems = lint_changeling('Right Mantle.nwod')
        assert "Court mantle 'Winter' does not match" not in problems

    def test_mantle_merit_does_not_match_tag(self):
        problems = lint_changeling('Wrong Mantle.nwod')
        assert "Court mantle 'Winter' does not match" in problems

class TestGoodwill:
    def test_goodwill_for_other_court_tag(self):
        problems = lint_changeling('Goodwill for Other.nwod')
        assert "Court goodwill listed for court tag" not in problems

    def test_goodwill_for_same_court_tag(self):
        problems = lint_changeling('Goodwill for Same.nwod')
        assert "Court goodwill listed for court tag" in problems

    def test_goodwill_for_other_court_merit(self):
        problems = lint_changeling('Goodwill for Other.nwod')
        assert "Court goodwill listed for court mantle" not in problems

    def test_goodwill_for_same_court_merit(self):
        problems = lint_changeling('Goodwill for Same.nwod')
        assert "Court goodwill listed for court mantle" in problems

class TestStrict:
    @pytest.mark.parametrize("strict,is_problem", [
                             (True, False),
                             (False, False),
                             ])
    def test_court_with_mantle(self, strict, is_problem):
        problems = lint_changeling('Right Mantle.nwod', strict=strict)
        assert ("No mantle for court" in problems) == is_problem

    @pytest.mark.parametrize("strict,is_problem", [
                             (True, True),
                             (False, False),
                             ])
    def test_court_without_mantle(self, strict, is_problem):
        problems = lint_changeling('No Mantle.nwod', strict=strict)
        assert ("No mantle for court" in problems) == is_problem

    @pytest.mark.parametrize("strict,is_problem", [
                             (True, False),
                             (False, False),
                             ])
    def test_without_unseen_sense(self, strict, is_problem):
        problems = lint_changeling('No Unseen.nwod', strict=strict)
        assert ("Changelings cannot have the Unseen Sense merit" in problems) == is_problem

    @pytest.mark.parametrize("strict,is_problem", [
                             (True, True),
                             (False, False),
                             ])
    def test_with_unseen_sense(self, strict, is_problem):
        problems = lint_changeling('Has Unseen.nwod', strict=strict)
        assert ("Changelings cannot have the Unseen Sense merit" in problems) == is_problem

class TestViceAndVirtue:
    @pytest.mark.parametrize("strict,is_problem", [
                             (True, False),
                             (False, False),
                             ])
    def test_has_virtue(self, prefs, strict, is_problem):
        problems = lint_changeling('Has Virtue.nwod', strict=strict)
        assert ('Missing virtue' in problems) == is_problem

    @pytest.mark.parametrize("strict,is_problem", [
                             (True, True),
                             (False, False),
                             ])
    def test_missing_virtue(self, prefs, strict, is_problem):
        problems = lint_changeling('Gotta Nada.nwod', strict=strict)
        assert ('Missing virtue' in problems) == is_problem

    @pytest.mark.parametrize("strict,is_problem", [
                             (True, False),
                             (False, False),
                             ])
    def test_has_vice(self, prefs, strict, is_problem):
        problems = lint_changeling('Has Vice.nwod', strict=strict)
        assert ('Missing vice' in problems) == is_problem

    @pytest.mark.parametrize("strict,is_problem", [
                             (True, True),
                             (False, False),
                             ])
    def test_missing_vice(self, prefs, strict, is_problem):
        problems = lint_changeling('Gotta Nada.nwod', strict=strict)
        assert ('Missing vice' in problems) == is_problem
