"""Tests the intricacies of the build_header method"""

import re

import npc
from npc.character import *
import pytest

class TestName:
    def test_not_in_path(self):
        char = Character(name=['Hugh Mann'], path='local/storage/fake.nwod')
        header = char.build_header()
        assert "@realname Hugh Mann" in header

    def test_in_path(self):
        char = Character(name=['Hugh Mann'], path='local/storage/Hugh Mann.nwod')
        header = char.build_header()
        assert "@realname Hugh Mann" not in header

    def test_many_names(self):
        names = ['Hugh Mann', 'Mr. Big', 'Huggy Bug']
        char = Character(name=names)
        header = char.build_header()
        assert "@name {}".format(names[0]) not in header
        for name in names[1:]:
            assert "@name {}".format(name) in header

class TestChangelingHeaders:
    def test_seeming_and_kith(self):
        char = Changeling(type=['Changeling'], seeming=['Beast'], kith=['Swimmerskin'])
        header = char.build_header()
        assert "@changeling Beast Swimmerskin" in header
        assert "@type Changeling" not in header
        assert '@seeming Beast' not in header
        assert '@kith Swimmerskin' not in header

    def test_no_seeming(self):
        char = Changeling(type=['Changeling'], kith=['Swimmerskin'])
        header = char.build_header()
        assert "@type Changeling" in header
        assert "@kith Swimmerskin" in header

    def test_no_kith(self):
        char = Changeling(type=['Changeling'], seeming=['Beast'])
        header = char.build_header()
        assert "@type Changeling" in header
        assert "@seeming Beast" in header

class TestWerewolfHeaders:
    def test_no_auspice(self):
        char = Werewolf(type=['Werewolf'])
        header = char.build_header()
        assert '@type Werewolf' in header

    def test_with_auspice(self):
        char = Werewolf(type=['Werewolf'], auspice=['Cahalith'])
        header = char.build_header()
        assert '@werewolf Cahalith' in header
        assert '@type Werewolf' not in header
        assert '@auspice Cahalith' not in header

def test_rank():
    char = Character()
    char.tags('group').append('Townies')
    ranks = ['Foozer', 'Roz', 'Bazanger']
    for rank in ranks:
        char.tags('group').subtag('Townies').append(rank)
    header = char.build_header()
    for rank in ranks:
        assert '@rank {}'.format(rank) in header

def test_description():
    desc = 'Fee fie fo fum! I smell the blood of an Englishman!'
    char = Character(description=[desc])
    assert desc in char.build_header()
