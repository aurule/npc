import npc
import pytest
import subprocess

def run_create(tmp_path, *extra_args):
    if not extra_args:
        extra_args = []

    npc.cli.start(['--campaign', str(tmp_path), 'human'] + list(extra_args))

def test_calls_correct_function(tmp_path, mocker):
    mocker.patch('npc.commands.create_character.standard', autospec=True)

    run_create(tmp_path, 'hi')

    npc.commands.create_character.standard.assert_called_once()

class TestTemplateOption:
    def test_template_always_human(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.standard', autospec=True)

        run_create(tmp_path, 'character_name')

        args, kwargs = npc.commands.create_character.standard.call_args
        assert args == ('character_name','human')

class TestNameOption:
    def test_must_be_filled(self, tmp_path, mocker, capsys):
        mocker.patch('npc.commands.create_character.standard', autospec=True)

        with pytest.raises(BaseException):
            run_create(tmp_path)

            _, err = capsys.readouterr()
            assert 'name' in err

    def test_accepts_all_strings(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.standard', autospec=True)

        run_create(tmp_path, 'character_name')

        args, kwargs = npc.commands.create_character.standard.call_args
        assert args == ('character_name','human')

class TestGroupsOption:
    def test_defaults_to_none(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.standard', autospec=True)

        run_create(tmp_path, 'hi')

        args, kwargs = npc.commands.create_character.standard.call_args
        assert kwargs['groups'] is None

    @pytest.mark.parametrize('argname', ['-g', '--groups'])
    def test_accepts_short_and_long_arg(self, argname, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.standard', autospec=True)

        run_create(tmp_path, 'hi', argname, 'g1')

        args, kwargs = npc.commands.create_character.standard.call_args
        assert 'g1' in kwargs['groups']

    def test_accepts_many_names(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.standard', autospec=True)

        run_create(tmp_path, 'hi', '-g', 'g1', 'g2', 'g3')

        args, kwargs = npc.commands.create_character.standard.call_args
        assert kwargs['groups'] == ['g1', 'g2', 'g3']

class TestDeadOption:
    def test_defaults_to_false(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.standard', autospec=True)

        run_create(tmp_path, 'hi')

        args, kwargs = npc.commands.create_character.standard.call_args
        assert kwargs['dead'] == False

    def test_accepts_long_opt(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.standard', autospec=True)

        run_create(tmp_path, 'hi', '--dead')

        args, kwargs = npc.commands.create_character.standard.call_args
        assert kwargs['dead'] != False

    def test_allows_no_text(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.standard', autospec=True)

        run_create(tmp_path, 'hi', '--dead')

        args, kwargs = npc.commands.create_character.standard.call_args
        assert kwargs['dead'] == ''

    def test_allows_single_arg(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.standard', autospec=True)

        run_create(tmp_path, 'hi', '--dead', 'fifteen ways')

        args, kwargs = npc.commands.create_character.standard.call_args
        assert kwargs['dead'] == 'fifteen ways'

class TestForeignOption:
    def test_defaults_to_false(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.standard', autospec=True)

        run_create(tmp_path, 'hi')

        args, kwargs = npc.commands.create_character.standard.call_args
        assert kwargs['foreign'] == False

    def test_accepts_long_opt(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.standard', autospec=True)

        run_create(tmp_path, 'hi', '--foreign')

        args, kwargs = npc.commands.create_character.standard.call_args
        assert kwargs['foreign'] != False

    def test_allows_no_text(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.standard', autospec=True)

        run_create(tmp_path, 'hi', '--foreign')

        args, kwargs = npc.commands.create_character.standard.call_args
        assert kwargs['foreign'] == ''

    def test_allows_single_arg(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.standard', autospec=True)

        run_create(tmp_path, 'hi', '--foreign', 'over there')

        args, kwargs = npc.commands.create_character.standard.call_args
        assert kwargs['foreign'] == 'over there'

class TestLocationOption:
    def test_defaults_to_false(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.standard', autospec=True)

        run_create(tmp_path, 'hi')

        args, kwargs = npc.commands.create_character.standard.call_args
        assert kwargs['location'] == False

    def test_accepts_long_opt(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.standard', autospec=True)

        run_create(tmp_path, 'hi', '--location', 'here')

        args, kwargs = npc.commands.create_character.standard.call_args
        assert kwargs['location'] == 'here'

    def test_requires_text(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.standard', autospec=True)

        with pytest.raises(BaseException):
            run_create(tmp_path, 'hi', '--location')
