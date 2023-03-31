from npc.settings.helpers import merge_settings_lists

class TestNewListHasNewSimpleValue:
    old_list = [1, 2, 3, 4]
    new_list = [5]

    def test_inserts_new_value(self):
        result = merge_settings_lists(self.new_list, self.old_list)

        assert 5 in result

    def test_does_not_change_original(self):
        result = merge_settings_lists(self.new_list, self.old_list)

        assert 5 not in self.old_list
