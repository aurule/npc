from npc.character.tags import Tag

def test_saves_default_values():
    tag = Tag('type', 'asdf', '1234')
    assert 'asdf' in tag
    assert '1234' in tag

class TestPresence:
    def test_present_with_values_set(self):
        tag = Tag('type', 'asdf')
        assert tag.present

    def test_not_present_with_no_values(self):
        tag = Tag('type')
        assert not tag.present

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
    def test_no_string_when_not_present(self):
        tag = Tag('type')
        header = tag.to_header()
        assert not header

    def test_has_string_when_present(self):
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
