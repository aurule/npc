import npc
import pytest
import subprocess

def run_settings(tmp_path, *extra_args):
    if not extra_args:
        extra_args = []

    npc.cli.start(['--campaign', str(tmp_path), 'settings'] + list(extra_args))

def test_calls_correct_function(tmp_path, mocker):
    mocker.patch('npc.commands.open_settings', autospec=True)

    run_settings(tmp_path, 'user')

    npc.commands.open_settings.assert_called_once()

class TestLocationOption:
    def test_must_be_filled(self, tmp_path, mocker, capsys):
        mocker.patch('npc.commands.open_settings', autospec=True)

        with pytest.raises(BaseException):
            run_settings(tmp_path)

            _, err = capsys.readouterr()
            assert 'location' in err

    def test_rejects_unknown_locations(self, tmp_path, mocker, capsys):
        mocker.patch('npc.commands.open_settings', autospec=True)

        with pytest.raises(BaseException):
            run_settings(tmp_path, 'badlocation')

            _, err = capsys.readouterr()
            assert 'location' in err

    @pytest.mark.parametrize('location', ['user', 'campaign'])
    def test_accepts_valid_locations(self, location, tmp_path, mocker):
        mocker.patch('npc.commands.open_settings', autospec=True)

        run_settings(tmp_path, location)

        args, kwargs = npc.commands.open_settings.call_args
        assert args == (location,)

class TestSettingsTypeOption:
    def test_defaults_to_none(self, tmp_path, mocker):
        mocker.patch('npc.commands.open_settings', autospec=True)

        run_settings(tmp_path, 'user')

        args, kwargs = npc.commands.open_settings.call_args
        assert kwargs['settings_type'] is None

    def test_rejects_unknown_settings_types(self, tmp_path, mocker, capsys):
        mocker.patch('npc.commands.open_settings', autospec=True)

        with pytest.raises(BaseException):
            run_settings(tmp_path, 'user', '-t', 'badtype')

            _, err = capsys.readouterr()
            assert 'badtype' in err

    @pytest.mark.parametrize('settings_type', ['base', 'changeling'])
    def test_accepts_valid_locations(self, settings_type, tmp_path, mocker):
        mocker.patch('npc.commands.open_settings', autospec=True)

        run_settings(tmp_path, 'user', '-t', settings_type)

        args, kwargs = npc.commands.open_settings.call_args
        assert kwargs['settings_type'] == settings_type

    @pytest.mark.parametrize('argname', ['-t', '--type'])
    def test_accepts_short_and_long_arg(self, argname, tmp_path, mocker):
        mocker.patch('npc.commands.open_settings', autospec=True)

        run_settings(tmp_path, 'user', argname, 'base')

        args, kwargs = npc.commands.open_settings.call_args
        assert kwargs['settings_type'] == 'base'

class TestShowDefaultsFlag:
    def test_defaults_to_false(self, tmp_path, mocker):
        mocker.patch('npc.commands.open_settings', autospec=True)

        run_settings(tmp_path, 'user')

        args, kwargs = npc.commands.open_settings.call_args
        assert kwargs['show_defaults'] == False

    @pytest.mark.parametrize('argname', ['-d', '--defaults'])
    def test_accepts_short_and_long_arg(self, argname, tmp_path, mocker):
        mocker.patch('npc.commands.open_settings', autospec=True)

        run_settings(tmp_path, 'user', argname)

        args, kwargs = npc.commands.open_settings.call_args
        assert kwargs['show_defaults'] == True

