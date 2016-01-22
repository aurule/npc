import npc
import pytest
import os

@pytest.fixture(scope="module")
def prefs():
    return npc.main.Settings(extra_paths=[])

@pytest.fixture(scope="module")
def parser(prefs):
    return npc.main._make_parser(prefs)

@pytest.fixture
def campaign(tmpdir, request):
    base = os.path.dirname(os.path.realpath(__file__))
    os.chdir(str(tmpdir))
    def fin():
        os.chdir(base)
    request.addfinalizer(fin)
    return tmpdir
