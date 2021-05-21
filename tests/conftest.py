import npc
import pytest
import os
from pathlib import Path
from tests.util import fixture_dir
from distutils import dir_util

@pytest.fixture
def prefs():
    """Creates a non-singleton Settings object."""
    return npc.settings.Settings()

class Campaign:
    def __init__(self, tmp_path, chardir):
        self.basedir = tmp_path
        self.chardir = tmp_path / chardir
        self.chardir.mkdir()

    def get_character(self, filename):
        """Get a file object for the given character filename"""
        return self.chardir.joinpath(filename)

    def get_character_data(self, filename):
        """Get the parsed data from the given character filename"""
        parseables = str(self.chardir.joinpath(filename))
        return next(c for c in npc.parser.get_characters(search_paths=[parseables]))

    def get_file(self, *fileparts):
        return self.basedir.joinpath(*fileparts)

    def get_absolute(self, filename):
        """Get the fully qualified path to the given filename"""
        return str(self.basedir.joinpath(filename))

    def populate_from_fixture_dir(self, *fixture_path):
        """
        Copy the files and folders from a fixture directory into the campaign
        root.

        Args:
            *fixture_path (str): Path elements to combine. All should be under
                the npc/tests/fixtures directory in this package. It will be run
                through `util.fixture_dir` first.
        """
        srcpath = fixture_dir(*fixture_path)
        dir_util.copy_tree(srcpath, str(self.basedir))

    def mkdir(self, directory_name):
        """Create a directory within this campaign root"""
        self.basedir.joinpath(directory_name).mkdir()

@pytest.fixture
def campaign(tmp_path, request, prefs):
    base = Path(__file__).resolve().parent
    os.chdir(str(tmp_path))
    def fin():
        os.chdir(base)
    request.addfinalizer(fin)
    return Campaign(tmp_path, prefs.get('paths.required.characters'))
