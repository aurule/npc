import npc
import pytest
import os

@pytest.fixture(scope="module")
def prefs():
    return npc.main.Settings(extra_paths=[])

@pytest.fixture(scope="module")
def argparser(prefs):
    return npc.main._make_parser(prefs)

class Campaign:
    def __init__(self, tmpdir, chardir):
        self.basedir = tmpdir
        self.chardir = tmpdir.mkdir(chardir)

    def get_character(self, filename):
        return self.chardir.join(filename)

    def get_character_data(self, filename):
        parseables = str(self.chardir.join(filename))
        return next(c for c in npc.parser.get_characters(search_paths=[parseables]))

    def get_absolute(self, filename):
        return str(self.basedir.join(filename))

@pytest.fixture
def campaign(tmpdir, request, prefs):
    base = os.path.dirname(os.path.realpath(__file__))
    os.chdir(str(tmpdir))
    def fin():
        os.chdir(base)
    request.addfinalizer(fin)
    return Campaign(tmpdir, prefs.get('paths.characters'))
