import pytest

from npc.util.errors import SchemaError
from npc.settings.helpers import merge_settings_dicts

class TestNewDictHasNewValue:
    old_dict = {"old": True}
    new_dict = {"new": True}

    def test_returns_dict_with_both_keys(self):
        result = merge_settings_dicts(self.new_dict, self.old_dict)

        assert "new" in result

    def test_does_not_change_original(self):
        result = merge_settings_dicts(self.new_dict, self.old_dict)

        assert "new" not in self.old_dict

class TestNewDictHasNewType:
    old_dict = {"val": ["yes", "no", "maybe"]}
    new_dict = {"val": {"yes": True, "no": False, "maybe": True}}

    def test_throws_parse_error(self):
        with pytest.raises(SchemaError):
            merge_settings_dicts(self.new_dict, self.old_dict)

class TestWithSimpleValues:
    old_dict = {"val": "oldness"}
    new_dict = {"val": "newness"}

    def test_overwrites_old_value(self):
        result = merge_settings_dicts(self.new_dict, self.old_dict)

        assert result["val"] == self.new_dict["val"]

class TestWithDictValues:
    old_dict = {"val": {"old": True}}
    new_dict = {"val": {"old": False, "new": True}}

    def test_updates_existing_dict_value(self):
        result = merge_settings_dicts(self.new_dict, self.old_dict)

        assert result["val"] == self.new_dict["val"]

class TestWithListValues:
    old_dict = {"val": [1, 2, 3]}
    new_dict = {"val": [1, 2, 3, 4]}

    def test_updates_existing_list(self):
        result = merge_settings_dicts(self.new_dict, self.old_dict)

        assert result["val"] == self.new_dict["val"]
