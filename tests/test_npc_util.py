import json
import pytest
from collections import defaultdict

import npc
from npc import util

from tests.util import fixture_dir

class TestJsonLoading:
    def test_ignore_comments(self):
        filepath = fixture_dir('util', 'load_json', 'commented.json')
        loaded = util.load_json(filepath)
        assert "freedom" in loaded["data"]

    def test_ignore_trailing_commas(self):
        filepath = fixture_dir('util', 'load_json', 'trailing_commas.json')
        loaded = util.load_json(filepath)
        assert "freedom" in loaded["data"]
        assert ", }" in loaded['list']

    def test_bad_syntax(self):
        filepath = fixture_dir('util', 'load_json', 'bad_syntax.json')
        with pytest.raises(json.decoder.JSONDecodeError) as err:
            loaded = util.load_json(filepath)
        assert "Bad syntax" in err.value.nicemsg

def test_error_printer(capsys):
    util.error("Catchphrase!")
    out, err = capsys.readouterr()
    assert out == ""
    assert err == "Catchphrase!\n"

def test_flatten():
    nested = ['some text', 5, ['yet more']]
    flatted = ['some text', 5, 'yet more']
    assert [x for x in util.flatten(nested)] == flatted

class TestFindCampaignRoot:
    def test_with_npc_dir(self, campaign):
        campaign.populate_from_fixture_dir('util', 'campaign_root', 'initialized')
        assert util.find_campaign_root() == campaign.basedir

    def test_no_npc_dir(self, campaign):
        campaign.populate_from_fixture_dir('util', 'campaign_root', 'empty')
        assert util.find_campaign_root() == campaign.basedir

def test_open_files(prefs):
    override_path = fixture_dir('util', 'open_files', 'settings-echo.json')
    prefs.load_more(override_path)
    result = util.open_files('not a real path', 'seriously, no', prefs=prefs)
    assert 'not a real path' in result.args
    assert 'seriously, no' in result.args

class TestResult:
    def test_str_success(self):
        result = util.result.Result(True)
        assert str(result) == "Success"

    def test_str_failure(self):
        result = util.result.Result(False, errmsg="There's a problem or something")
        assert str(result) == "There's a problem or something"

    @pytest.mark.parametrize('val', [True, False])
    def test_bool(self, val):
        result = util.result.Result(val)
        assert bool(result) == val

class TestMergeDicts:
    def test_none_value_sets_default(self):
        base_dict = defaultdict(list)
        util.merge_to_dict(base_dict, 'test', None)

        assert base_dict.get('test') == []

    def test_list_value_is_concatenated(self):
        base_dict = {'test': [1, 2, 3]}
        util.merge_to_dict(base_dict, 'test', [4, 5])

        assert base_dict['test'] == [1, 2, 3, 4, 5]

    def test_scalar_is_appended(self):
        base_dict = {'test': [1, 2, 3]}
        util.merge_to_dict(base_dict, 'test', 4)

        assert base_dict['test'] == [1, 2, 3, 4]

    def test_string_is_appended(self):
        base_dict = {'test': [1, 2, 3]}
        util.merge_to_dict(base_dict, 'test', 'four')

        assert base_dict['test'] == [1, 2, 3, 'four']

class SingletonClass(metaclass=util.Singleton):
    def __init__(self, word):
        self.word = word

    def get_a_thing(self):
        return self.word

class TestSingleton:
    def test_creates_one_instance(self):
        obj1 = SingletonClass('hello')
        obj2 = SingletonClass('goodbye')
        assert obj1.get_a_thing() == 'hello'
        assert obj2.get_a_thing() == 'hello'

class TestSerializeArgs:
    def test_creates_list_of_serial_args(self):
        serial, full = util.serialize_args('first', 'second', **{'first': '1', 'second': '2', 'third': '3'})
        assert serial == ['1', '2']

    def test_removes_serial_args_from_dict(self):
        serial, full = util.serialize_args('first', 'second', **{'first': '1', 'second': '2', 'third': '3'})
        assert full == {'third': '3'}

class TestListifyArgs:
    def test_modifies_named_strings(self):
        args = util.listify_args('list', **{'list': '1, 2, 3', 'not_list': 'hammer, spanner, prybar'})
        assert args['list'] == ['1', '2', '3']
        assert args['not_list'] == 'hammer, spanner, prybar'

    def test_skips_none(self):
        args = util.listify_args('list', **{'list': None, 'not_list': 'hammer, spanner, prybar'})
        assert args['list'] is None
