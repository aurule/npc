"""Tests the intricacies of the build_header method"""

import re

import npc
from npc.character import *
import pytest

def test_faketype_replaces_type():
    c1 = Character(type=['vampire'], faketype=['human'])
    c1.sanitize()
    assert c1.tags('type').first_value() == 'human'

def test_hidden_tags_are_removed():
    c1 = Character(type=['human'], location=['France'])
    c1.tags('location').hidden = True
    c1.sanitize()
    assert not c1.tags('location').present

def test_hidden_flags_are_removed():
    c1 = Character(type=['human'], foreign=['France'])
    c1.tags('foreign').hidden = True
    c1.sanitize()
    assert not c1.tags('foreign').present

def test_missing_type_gets_default():
    c1 = Character()
    c1.sanitize()
    assert c1.tags('type').first_value() == 'Unknown'
