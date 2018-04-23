import npc
import pytest
import subprocess
from util import fixture_dir
from distutils import dir_util

def test_bad_path(capsys):
    npc.cli.start(['--campaign', fixture_dir('cli', 'nope')])
    _, err = capsys.readouterr()

    assert 'No such file or directory' in err

def test_failed_command(tmpdir, capsys):
    srcpath = fixture_dir('cli', 'failed_command')
    dir_util.copy_tree(srcpath, str(tmpdir))

    npc.cli.start(['--campaign', str(tmpdir), 'h', 'manny'])
    _, err = capsys.readouterr()

    assert 'No such file or directory' in err

class TestBatch:
    def test_no_printing(self, tmpdir, capsys):
        npc.cli.start(['--campaign', str(tmpdir), 'init', '--dryrun', '--batch'])
        output, _ = capsys.readouterr()

        assert output == ''

    def test_no_opening(self, tmpdir, capsys):
        srcpath = fixture_dir('cli', 'batch_no_open')
        dir_util.copy_tree(srcpath, str(tmpdir))

        npc.cli.start(['--campaign', str(tmpdir), 'h', 'manny', '--batch'])
        output, _ = capsys.readouterr()

        assert output == ''
