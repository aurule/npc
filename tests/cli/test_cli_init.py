import npc
import pytest
import subprocess

def run_init(tmp_path, *extra_args):
    if not extra_args:
        extra_args = []

    npc.cli.start(['--campaign', str(tmp_path), 'init'] + list(extra_args))

def test_calls_correct_function(tmp_path, mocker):
    mocker.patch('npc.commands.init', autospec=True)

    run_init(tmp_path)

    npc.commands.init.assert_called_once()

class TestCampaignNameArg:
    def test_defaults_to_false(self, tmp_path, mocker):
        mocker.patch('npc.commands.init', autospec=True)

        run_init(tmp_path)

        args, kwargs = npc.commands.init.call_args
        assert kwargs['campaign_name'] is None

    @pytest.mark.parametrize('argname', ['-n', '--name'])
    def test_accepts_short_and_long_arg(self, argname, tmp_path, mocker):
        mocker.patch('npc.commands.init', autospec=True)

        run_init(tmp_path, argname, 'test campaign')

        args, kwargs = npc.commands.init.call_args
        assert kwargs['campaign_name'] == 'test campaign'

class TestTypesFlag:
    def test_defaults_to_false(self, tmp_path, mocker):
        mocker.patch('npc.commands.init', autospec=True)

        run_init(tmp_path)

        args, kwargs = npc.commands.init.call_args
        assert kwargs['create_types'] == False

    @pytest.mark.parametrize('argname', ['-t', '--types'])
    def test_accepts_short_and_long_arg(self, argname, tmp_path, mocker):
        mocker.patch('npc.commands.init', autospec=True)

        run_init(tmp_path, argname)

        args, kwargs = npc.commands.init.call_args
        assert kwargs['create_types'] == True

class TestAllFoldersFlag:
    def test_defaults_to_false(self, tmp_path, mocker):
        mocker.patch('npc.commands.init', autospec=True)

        run_init(tmp_path)

        args, kwargs = npc.commands.init.call_args
        assert kwargs['create_all'] == False

    @pytest.mark.parametrize('argname', ['-a', '--all'])
    def test_accepts_short_and_long_arg(self, argname, tmp_path, mocker):
        mocker.patch('npc.commands.init', autospec=True)

        run_init(tmp_path, argname)

        args, kwargs = npc.commands.init.call_args
        assert kwargs['create_all'] == True

class TestVerboseFlag:
    def test_defaults_to_false(self, tmp_path, mocker):
        mocker.patch('npc.commands.init', autospec=True)

        run_init(tmp_path)

        args, kwargs = npc.commands.init.call_args
        assert kwargs['verbose'] == False

    @pytest.mark.parametrize('argname', ['-v', '--verbose'])
    def test_accepts_short_and_long_arg(self, argname, tmp_path, mocker):
        mocker.patch('npc.commands.init', autospec=True)

        run_init(tmp_path, argname)

        args, kwargs = npc.commands.init.call_args
        assert kwargs['verbose'] == True

class TestDryrunFlag:
    def test_defaults_to_false(self, tmp_path, mocker):
        mocker.patch('npc.commands.init', autospec=True)

        run_init(tmp_path)

        args, kwargs = npc.commands.init.call_args
        assert kwargs['dryrun'] == False

    @pytest.mark.parametrize('argname', ['--dryrun'])
    def test_accepts_long_arg(self, argname, tmp_path, mocker):
        mocker.patch('npc.commands.init', autospec=True)

        run_init(tmp_path, argname)

        args, kwargs = npc.commands.init.call_args
        assert kwargs['dryrun'] == True
