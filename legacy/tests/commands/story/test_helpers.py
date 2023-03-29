import re

import npc
from npc.commands import story

class TestRegexFromTemplate:
    def test_ignores_case(self):
        regex = story.regex_from_template('asdf')
        assert regex.match('ASDF')

    def test_captures_first_number(self):
        regex = story.regex_from_template('asdf NNN NNN')
        match = regex.match('asdf 53 42')
        assert match.group('number') == '53'

    def test_enforces_bounds(self):
        """The regex should match to the start and end of a filename"""
        regex = story.regex_from_template('asdf NNN')
        match = regex.match('asdf 53 42')
        assert match == None
