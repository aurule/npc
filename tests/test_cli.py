import npc
import pytest
import subprocess
from util import fixture_dir
from distutils import dir_util

@pytest.fixture
def run():
    def do_run(*args):
        newargs = ["python3", "-m", "npc", *args]
        return subprocess.run(newargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return do_run

def test_version(run):
    procinfo = run('--version')
    assert procinfo.stdout.decode('utf-8') == "{}\n".format(npc.__version__.__version__)

def test_bad_path(run):
    procinfo = run('--campaign', fixture_dir('cli', 'nope'))
    assert 'No such file or directory' in procinfo.stderr.decode('utf-8')

def test_bad_settings(run, tmpdir):
    srcpath = fixture_dir('cli', 'bad_settings')
    dir_util.copy_tree(srcpath, str(tmpdir))
    procinfo = run('--campaign', str(tmpdir))
    assert 'Mismatch in changeling settings' in procinfo.stdout.decode('utf-8')

def test_help(run):
    procinfo = run()
    assert 'usage: npc' in procinfo.stdout.decode('utf-8')

def test_failed_command(run, tmpdir):
    srcpath = fixture_dir('cli', 'failed_command')
    dir_util.copy_tree(srcpath, str(tmpdir))
    procinfo = run('--campaign', str(tmpdir), 'h', 'manny')
    assert 'No such file or directory' in procinfo.stderr.decode('utf-8')

class TestBatch:
    def test_no_printing(self, run, tmpdir):
        procinfo = run('--batch', '--campaign', str(tmpdir), 'init', '--dryrun')
        assert procinfo.stdout == b''

    def test_no_opening(self, run, tmpdir, capsys):
        srcpath = fixture_dir('cli', 'batch_no_open')
        dir_util.copy_tree(srcpath, str(tmpdir))
        procinfo = run('--batch', '--campaign', str(tmpdir), 'h', 'manny')
        assert procinfo.stdout == b''
