from npc.settings.helpers import merge_tags_lists

class TestNewListHasNewSimpleValue:
    old_list = [1, 2, 3, 4]
    new_list = [5]

    def test_inserts_new_value(self):
        result = merge_tags_lists(self.new_list, self.old_list)

        assert 5 in result

    def test_does_not_change_original(self):
        result = merge_tags_lists(self.new_list, self.old_list)

        assert 5 not in self.old_list

class TestNewListHasNewTagDict:
    old_list = [{"name": "age"}]
    new_list = [{"name": "class"}]

    def test_inserts_new_tag(self):
        result = merge_tags_lists(self.new_list, self.old_list)

        assert len(result) == 2

class TestNewListHasAlteredTag:
    old_list = [{"name": "age"}]
    new_list = [{"name": "age", "max": 1}]

    def test_updates_existing_tag(self):
        result = merge_tags_lists(self.new_list, self.old_list)

        assert result[0] == self.new_list[0]
