import npc
import argparse
import pytest

def test_creation():
    assert type(npc.cli._make_parser()) is argparse.ArgumentParser
