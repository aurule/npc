import npc
import pytest
import subprocess

def run_latest(tmp_path, *extra_args):
    if not extra_args:
        extra_args = []

    npc.cli.start(['--campaign', str(tmp_path), 'latest'] + list(extra_args))

def test_calls_correct_function(tmp_path, mocker):
    mocker.patch('npc.commands.story.latest', autospec=True)

    run_latest(tmp_path)

    npc.commands.story.latest.assert_called_once()

class TestThingTypeOption:
    def test_defaults_to_both(self, tmp_path, mocker):
        mocker.patch('npc.commands.story.latest', autospec=True)

        run_latest(tmp_path)

        args, kwargs = npc.commands.story.latest.call_args
        assert args == ('both',)

    @pytest.mark.parametrize('thingtype', ['both', 'session', 'plot'])
    def test_accepts_correct_thingtypes(self, thingtype, tmp_path, mocker):
        mocker.patch('npc.commands.story.latest', autospec=True)

        run_latest(tmp_path, thingtype)

        args, kwargs = npc.commands.story.latest.call_args
        assert args == (thingtype,)

    def test_rejects_unknown_thingtypes(self, tmp_path, mocker, capsys):
        mocker.patch('npc.commands.story.latest', autospec=True)

        with pytest.raises(BaseException):
            run_latest(tmp_path, 'fakething')

            _, err = capsys.readouterr()
            assert 'fakething' in err
