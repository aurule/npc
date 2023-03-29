import npc
import pytest
import subprocess

def run_session(tmp_path, *extra_args):
    if not extra_args:
        extra_args = []

    npc.cli.start(['--campaign', str(tmp_path), 'session'] + list(extra_args))

def test_calls_correct_function(tmp_path, mocker):
    mocker.patch('npc.commands.story.session', autospec=True)

    run_session(tmp_path)

    npc.commands.story.session.assert_called_once()
