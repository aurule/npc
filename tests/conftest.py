import npc
import pytest
import os
from tests.util import fixture_dir
from distutils import dir_util

@pytest.fixture(scope="module")
def prefs():
    """Creates a non-singleton Settings object."""
    return npc.settings.Settings()

class Campaign:
    def __init__(self, tmpdir, chardir):
        self.basedir = tmpdir
        self.chardir = tmpdir.mkdir(chardir)

    def get_character(self, filename):
        """Get a file object for the given character filename"""
        return self.chardir.join(filename)

    def get_character_data(self, filename):
        """Get the parsed data from the given character filename"""
        parseables = str(self.chardir.join(filename))
        return next(c for c in npc.parser.get_characters(search_paths=[parseables]))

    def get_file(self, *fileparts):
        return self.basedir.join(*fileparts)

    def get_absolute(self, filename):
        """Get the fully qualified path to the given filename"""
        return str(self.basedir.join(filename))

    def populate_from_fixture_dir(self, fixture_path):
        """Copy the files and folders from a fixture directory into the campaign
        root.

        The path given should be relative to the npc/tests/fixtures directory in
        this package. It will be run through `fixture_dir` first.
        """
        srcpath = fixture_dir(fixture_path)
        dir_util.copy_tree(srcpath, str(self.basedir))

@pytest.fixture
def campaign(tmpdir, request, prefs):
    base = os.path.dirname(os.path.realpath(__file__))
    os.chdir(str(tmpdir))
    def fin():
        os.chdir(base)
    request.addfinalizer(fin)
    return Campaign(tmpdir, prefs.get('paths.characters'))
