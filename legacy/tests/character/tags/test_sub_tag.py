from npc.character.tags import SubTag

class TestHeader:
    def test_no_string_when_not_filled(self):
        tag = SubTag('rank')
        header = tag.to_header('group', 'Beach Boys')
        assert not header

    def test_has_string_when_filled(self):
        tag = SubTag('rank', 'value')
        header = tag.to_header('group', 'Beach Boys')
        assert header == '@rank value'

    def test_no_hide_when_not_hidden(self):
        tag = SubTag('rank', 'value', hidden=False)
        header = tag.to_header('group', 'Beach Boys')
        assert header == '@rank value'

    def test_has_hide_when_hidden(self):
        tag = SubTag('rank', 'value', hidden=True)
        header = tag.to_header('group', 'Beach Boys')
        assert '@hide group >> Beach Boys >> subtags' in header

    def test_hides_values_when_marked(self):
        tag = SubTag('rank', 'value1', 'value2', hidden=False)
        tag.hide_value('value2')
        header = tag.to_header('group', 'Beach Boys')
        assert '@hide group >> Beach Boys >> value2' in header
