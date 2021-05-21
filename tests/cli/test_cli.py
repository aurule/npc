import npc
import pytest
import subprocess
from util import fixture_dir
from distutils import dir_util

def test_bad_path(capsys):
    npc.cli.start(['--campaign', str(fixture_dir('cli', 'nope'))])
    _, err = capsys.readouterr()

    assert 'No such file or directory' in err

def test_failed_command(tmp_path, capsys):
    srcpath = fixture_dir('cli', 'failed_command')
    dir_util.copy_tree(srcpath, str(tmp_path))

    npc.cli.start(['--campaign', str(tmp_path), 'h', 'manny'])
    _, err = capsys.readouterr()

    assert 'No such file or directory' in err

class TestBatch:
    def test_no_printing(self, tmp_path, capsys):
        npc.cli.start(['--campaign', str(tmp_path), 'init', '--dryrun', '--batch'])
        output, _ = capsys.readouterr()

        assert output == ''

    def test_no_opening(self, tmp_path, capsys):
        srcpath = fixture_dir('cli', 'batch_no_open')
        dir_util.copy_tree(srcpath, str(tmp_path))

        npc.cli.start(['--campaign', str(tmp_path), 'h', 'manny', '--batch'])
        output, _ = capsys.readouterr()

        assert output == ''
