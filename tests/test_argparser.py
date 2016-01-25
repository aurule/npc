import npc
import argparse
import pytest

def test_creation(prefs):
    assert type(npc.main._make_parser(prefs)) is argparse.ArgumentParser
