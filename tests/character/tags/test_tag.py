from npc.character.tags import Tag

def test_saves_default_values():
    tag = Tag('type', 'asdf', '1234')
    assert 'asdf' in tag
    assert '1234' in tag

class TestUpdate:
    def test_inserts_new_values(self):
        tag = Tag('type')
        tag.update(['human', 'monkey'])
        assert 'human' in tag

    def test_overwrites_old_values(self):
        tag = Tag('type')
        tag.update(['werewolf'])
        tag.update(['human', 'monkey'])
        assert 'human' in tag
        assert 'werewolf' not in tag

def test_append_ignores_empty_values():
    tag = Tag('type')
    tag.append(' \t ')
    assert tag.filled is False

def test_filled_data_ignores_empties():
    tag = Tag('type')
    tag.append(' \t ')
    tag.append('human')
    assert tag.filled_data == ['human']

class TestFilled:
    def test_filled_with_values_set(self):
        tag = Tag('type', 'asdf')
        assert tag.filled
        assert tag

    def test_not_filled_with_no_values(self):
        tag = Tag('type')
        assert not tag.filled
        assert not tag

class TestPresent:
    def test_present_with_values_set(self):
        tag = Tag('type', 'asdf')
        assert tag.present
        assert tag

    def test_not_present_with_no_values(self):
        tag = Tag('type')
        assert not tag.present
        assert not tag

class TestValidation:
    def test_required_with_no_values_fails(self):
        tag = Tag('type', required=True)
        tag.validate()
        assert not tag.valid

    def test_required_with_values_passes(self):
        tag = Tag('type', 'asdf', required=True)
        tag.validate()
        assert tag.valid

    def test_limit_zero_and_required_dont_mix(self):
        tag = Tag('type', 'asdf', required=True, limit=0)
        tag.validate()
        assert not tag.valid
        assert "Tag 'type' is required but limited to zero values" in tag.problems

class TestStrictValidation:
    def test_limit_exceeded(self):
        tag = Tag('type', 'asdf', '1234', limit=1)
        tag.validate(strict=True)
        assert not tag.valid

    def test_under_limit(self):
        tag = Tag('type', 'asdf', '1234', limit=5)
        tag.validate(strict=True)
        assert tag.valid

    def test_negative_limit(self):
        tag = Tag('type', 'asdf', '1234', limit=-1)
        tag.validate(strict=True)
        assert tag.valid

class TestHeader:
    def test_no_string_when_not_filled(self):
        tag = Tag('type')
        header = tag.to_header()
        assert not header

    def test_has_string_when_filled(self):
        tag = Tag('type', 'value')
        header = tag.to_header()
        assert header == '@type value'

    def test_no_hide_when_not_hidden(self):
        tag = Tag('type', 'value', hidden=False)
        header = tag.to_header()
        assert header == '@type value'

    def test_has_hide_when_hidden(self):
        tag = Tag('type', 'value', hidden=True)
        header = tag.to_header()
        assert '@hide type' in header

    def test_has_one_line_per_value(self):
        tag = Tag('type', 'value1', 'value2', 'value3')
        header = tag.to_header()
        assert '@type value1' in header
        assert '@type value2' in header
        assert '@type value3' in header

class TestTagSlice:
    def test_preserves_attributes(self):
        tag = Tag('type', 'value1', 'value2', 'value3', required=True, hidden=True, limit=5)
        tag2 = tag.tagslice(0, 1)
        assert tag2.required == tag.required
        assert tag2.hidden == tag.hidden
        assert tag2.limit == tag.limit

    def test_applies_slice_to_data(self):
        tag = Tag('type', 'value1', 'value2', 'value3')
        tag2 = tag.tagslice(1, 2)
        assert tag2.data == ['value2']

def test_first_gets_just_first_element():
    tag = Tag('type', 'value1', 'value2', 'value3')
    tag2 = tag.first()
    assert tag2.data == ['value1']

def test_remaining_gets_all_other_elements():
    tag = Tag('type', 'value1', 'value2', 'value3')
    tag2 = tag.remaining()
    assert tag2.data == ['value2', 'value3']

class TestContains:
    def test_wildcard_with_any_values_is_true(self):
        tag = Tag('type', 'value1', 'value2', 'value3')
        assert tag.contains('*')

    def test_matches_wrong_case(self):
        tag = Tag('type', 'value1', 'value2', 'value3')
        assert tag.contains('VALUE1')

    def test_matches_partial_values(self):
        tag = Tag('type', 'value1', 'value2', 'value3')
        assert tag.contains('val')

class TestFirstValue:
    def test_returns_string_if_present(self):
        tag = Tag('type', 'value1', 'value2')
        assert tag.first_value() == 'value1'

    def test_returns_none_if_no_values(self):
        tag = Tag('type')
        assert tag.first_value() is None

def test_bool_truthy_when_present():
    tag = Tag('type')
    assert not tag
    tag.append('human')
    assert tag

class TestHideValues:
    def test_when_hidden_removes_all_values(self):
        tag = Tag('type', 'value1', 'value2', 'value3', hidden=True)
        tag.hide_values()
        assert not tag

    def test_when_not_hidden_removes_nothing(self):
        tag = Tag('type', 'value1', 'value2', 'value3', hidden=False)
        tag.hide_values()
        assert tag.data == ['value1', 'value2', 'value3']
