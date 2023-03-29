import npc
import pytest
import subprocess

def run_create(tmp_path, *extra_args):
    if not extra_args:
        extra_args = []

    npc.cli.start(['--campaign', str(tmp_path), 'changeling'] + list(extra_args))

def test_calls_correct_function(tmp_path, mocker):
    mocker.patch('npc.commands.create_character.changeling', autospec=True)

    run_create(tmp_path, 'hi', 'seeming', 'kith')

    npc.commands.create_character.changeling.assert_called_once()

class TestTemplateOption:
    def test_template_always_changeling(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        run_create(tmp_path, 'character_name', 'seeming_name', 'kith_name')

        args, kwargs = npc.commands.create_character.changeling.call_args
        assert args == ('character_name','seeming_name', 'kith_name')

class TestNameOption:
    def test_must_be_filled(self, tmp_path, mocker, capsys):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        with pytest.raises(BaseException):
            run_create(tmp_path)

            _, err = capsys.readouterr()
            assert 'name' in err

    def test_accepts_all_strings(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        run_create(tmp_path, 'character_name', 'seeming_name', 'kith_name')

        args, kwargs = npc.commands.create_character.changeling.call_args
        assert args == ('character_name','seeming_name', 'kith_name')

class TestSeemingOption:
    def test_must_be_filled(self, tmp_path, mocker, capsys):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        with pytest.raises(BaseException):
            run_create(tmp_path)

            _, err = capsys.readouterr()
            assert 'seeming' in err

    def test_accepts_all_strings(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        run_create(tmp_path, 'character_name', 'seeming_name', 'kith_name')

        args, kwargs = npc.commands.create_character.changeling.call_args
        assert args == ('character_name','seeming_name', 'kith_name')

class TestKithOption:
    def test_must_be_filled(self, tmp_path, mocker, capsys):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        with pytest.raises(BaseException):
            run_create(tmp_path)

            _, err = capsys.readouterr()
            assert 'kith' in err

    def test_accepts_all_strings(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        run_create(tmp_path, 'character_name', 'seeming_name', 'kith_name')

        args, kwargs = npc.commands.create_character.changeling.call_args
        assert args == ('character_name','seeming_name', 'kith_name')

class TestCourtOption:
    def test_defaults_to_none(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        run_create(tmp_path, 'name', 'seeming_name', 'kith_name')

        args, kwargs = npc.commands.create_character.changeling.call_args
        assert kwargs['court'] is None

    @pytest.mark.parametrize('argname', ['-c', '--court'])
    def test_accepts_short_and_long_arg(self, argname, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        run_create(tmp_path, 'name', 'seeming_name', 'kith_name', argname, 'test_court')

        args, kwargs = npc.commands.create_character.changeling.call_args
        assert kwargs['court'] == 'test_court'

class TestMotleyOption:
    def test_defaults_to_none(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        run_create(tmp_path, 'name', 'seeming_name', 'kith_name')

        args, kwargs = npc.commands.create_character.changeling.call_args
        assert kwargs['motley'] is None

    @pytest.mark.parametrize('argname', ['-m', '--motley'])
    def test_accepts_short_and_long_arg(self, argname, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        run_create(tmp_path, 'name', 'seeming_name', 'kith_name', argname, 'test_motley')

        args, kwargs = npc.commands.create_character.changeling.call_args
        assert kwargs['motley'] == 'test_motley'

class TestEntitlementOption:
    def test_defaults_to_none(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        run_create(tmp_path, 'name', 'seeming_name', 'kith_name')

        args, kwargs = npc.commands.create_character.changeling.call_args
        assert kwargs['entitlement'] is None

    @pytest.mark.parametrize('argname', ['-e', '--entitlement'])
    def test_accepts_short_and_long_arg(self, argname, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        run_create(tmp_path, 'name', 'seeming_name', 'kith_name', argname, 'test_entitlement')

        args, kwargs = npc.commands.create_character.changeling.call_args
        assert kwargs['entitlement'] == 'test_entitlement'

class TestFreeholdOption:
    def test_defaults_to_none(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        run_create(tmp_path, 'name', 'seeming_name', 'kith_name')

        args, kwargs = npc.commands.create_character.changeling.call_args
        assert kwargs['freehold'] is None

    @pytest.mark.parametrize('argname', ['-f', '--freehold'])
    def test_accepts_short_and_long_arg(self, argname, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        run_create(tmp_path, 'name', 'seeming_name', 'kith_name', argname, 'test_freehold')

        args, kwargs = npc.commands.create_character.changeling.call_args
        assert kwargs['freehold'] == 'test_freehold'

class TestGroupsOption:
    def test_defaults_to_none(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        run_create(tmp_path, 'hi', 'seeming_name', 'kith_name')

        args, kwargs = npc.commands.create_character.changeling.call_args
        assert kwargs['groups'] is None

    @pytest.mark.parametrize('argname', ['-g', '--groups'])
    def test_accepts_short_and_long_arg(self, argname, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        run_create(tmp_path, 'hi', 'seeming_name', 'kith_name', argname, 'g1')

        args, kwargs = npc.commands.create_character.changeling.call_args
        assert 'g1' in kwargs['groups']

    def test_accepts_many_names(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        run_create(tmp_path, 'hi', 'seeming_name', 'kith_name', '-g', 'g1', 'g2', 'g3')

        args, kwargs = npc.commands.create_character.changeling.call_args
        assert kwargs['groups'] == ['g1', 'g2', 'g3']

class TestDeadOption:
    def test_defaults_to_false(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        run_create(tmp_path, 'hi', 'seeming_name', 'kith_name')

        args, kwargs = npc.commands.create_character.changeling.call_args
        assert kwargs['dead'] == False

    def test_accepts_long_opt(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        run_create(tmp_path, 'hi', 'seeming_name', 'kith_name', '--dead')

        args, kwargs = npc.commands.create_character.changeling.call_args
        assert kwargs['dead'] != False

    def test_allows_no_text(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        run_create(tmp_path, 'hi', 'seeming_name', 'kith_name', '--dead')

        args, kwargs = npc.commands.create_character.changeling.call_args
        assert kwargs['dead'] == ''

    def test_allows_single_arg(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        run_create(tmp_path, 'hi', 'seeming_name', 'kith_name', '--dead', 'fifteen ways')

        args, kwargs = npc.commands.create_character.changeling.call_args
        assert kwargs['dead'] == 'fifteen ways'

class TestForeignOption:
    def test_defaults_to_false(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        run_create(tmp_path, 'hi', 'seeming_name', 'kith_name')

        args, kwargs = npc.commands.create_character.changeling.call_args
        assert kwargs['foreign'] == False

    def test_accepts_long_opt(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        run_create(tmp_path, 'hi', 'seeming_name', 'kith_name', '--foreign')

        args, kwargs = npc.commands.create_character.changeling.call_args
        assert kwargs['foreign'] != False

    def test_allows_no_text(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        run_create(tmp_path, 'hi', 'seeming_name', 'kith_name', '--foreign')

        args, kwargs = npc.commands.create_character.changeling.call_args
        assert kwargs['foreign'] == ''

    def test_allows_single_arg(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        run_create(tmp_path, 'hi', 'seeming_name', 'kith_name', '--foreign', 'over there')

        args, kwargs = npc.commands.create_character.changeling.call_args
        assert kwargs['foreign'] == 'over there'

class TestLocationOption:
    def test_defaults_to_false(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        run_create(tmp_path, 'hi', 'seeming_name', 'kith_name')

        args, kwargs = npc.commands.create_character.changeling.call_args
        assert kwargs['location'] == False

    def test_accepts_long_opt(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        run_create(tmp_path, 'hi', 'seeming_name', 'kith_name', '--location', 'here')

        args, kwargs = npc.commands.create_character.changeling.call_args
        assert kwargs['location'] == 'here'

    def test_requires_text(self, tmp_path, mocker):
        mocker.patch('npc.commands.create_character.changeling', autospec=True)

        with pytest.raises(BaseException):
            run_create(tmp_path, 'hi', 'seeming_name', 'kith_name', '--location')
