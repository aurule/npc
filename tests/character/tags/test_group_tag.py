from npc.character.tags import GroupTag, Tag

class TestSavesDefaultValues:
    def test_saves_list_values(self):
        tag = GroupTag('group', 'guys', 'dolls')
        assert 'guys' in tag
        assert 'dolls' in tag

    def test_saves_keyword_values(self):
        tag = GroupTag('group', guys=Tag('rank'), dolls=Tag('rank'))
        assert 'guys' in tag
        assert 'dolls' in tag

class TestUpdate:
    def test_inserts_blank_values(self):
        tag = GroupTag('group')
        tag.update(['humans', 'monkeys'])
        assert 'humans' in tag

    def test_inserts_from_group_tag(self):
        tag = GroupTag('group')
        tag2 = GroupTag('group')
        tag2.append('funny')
        tag2['funny'].append('giggles')
        tag.update(tag2)
        assert 'funny' in tag
        assert 'giggles' in tag['funny']

    def test_leaves_old_values(self):
        tag = GroupTag('group')
        tag.update(['werewolves'])
        tag.update(['humans', 'monkeys'])
        assert 'humans' in tag
        assert 'werewolves' in tag

class TestFilled:
    def test_filled_with_values_set(self):
        tag = GroupTag('employer', 'fruitco')
        assert tag.filled
        assert tag

    def test_not_filled_with_no_values(self):
        tag = GroupTag('employer')
        assert not tag.filled
        assert not tag

class TestFilled:
    def test_present_with_values_set(self):
        tag = GroupTag('employer', 'fruitco')
        assert tag.present
        assert tag

    def test_not_present_with_no_values(self):
        tag = GroupTag('employer')
        assert not tag.present
        assert not tag

class TestValidation:
    def test_required_with_no_values_fails(self):
        tag = GroupTag('employer', required=True)
        tag.validate()
        assert not tag.valid

    def test_required_with_values_passes(self):
        tag = GroupTag('employer', 'fruitco', required=True)
        tag.validate()
        assert tag.valid

    def test_limit_zero_and_required_dont_mix(self):
        tag = GroupTag('employer', 'fruitco', required=True, limit=0)
        tag.validate()
        assert not tag.valid
        assert "Tag 'employer' is required but limited to zero values" in tag.problems

    def test_subtag_doesnt_match(self):
        bad_subtag = Tag('rank')
        tag = GroupTag('employer', subtag='job')
        tag.data['bobsburgers'] = bad_subtag
        tag.validate()
        assert not tag.valid
        assert "Tag 'employer' uses subtag 'job', but found 'rank' for 'bobsburgers'" in tag.problems

class TestAppend:
    def test_adds_value_to_keys(self):
        tag = GroupTag('employer')
        tag.append('bobsburgers')
        assert 'bobsburgers' in tag

    def test_populates_correct_subtag(self):
        tag = GroupTag('employer', subtag='job')
        tag.append('bobsburgers')
        assert tag['bobsburgers'] == Tag('job')

class TestStrictValidation:
    def test_limit_exceeded(self):
        tag = GroupTag('employer', 'fruitco', 'bobsburgers', limit=1)
        tag.validate(strict=True)
        assert not tag.valid

    def test_under_limit(self):
        tag = GroupTag('employer', 'fruitco', 'bobsburgers', limit=5)
        tag.validate(strict=True)
        assert tag.valid

    def test_negative_limit(self):
        tag = GroupTag('employer', 'fruitco', 'bobsburgers', limit=-1)
        tag.validate(strict=True)
        assert tag.valid

class TestHeader:
    def test_no_string_when_not_filled(self):
        tag = GroupTag('group')
        header = tag.to_header()
        assert not header

    def test_has_string_when_filled(self):
        tag = GroupTag('group', 'value')
        header = tag.to_header()
        assert header == '@group value'

    def test_no_hide_when_not_hidden(self):
        tag = GroupTag('type', 'value', hidden=False)
        header = tag.to_header()
        assert header == '@type value'

    def test_has_hide_when_hidden(self):
        tag = GroupTag('type', 'value', hidden=True)
        header = tag.to_header()
        assert '@hide type' in header

    def test_has_one_line_per_value(self):
        tag = GroupTag('type', 'value1', 'value2', 'value3')
        header = tag.to_header()
        assert '@type value1' in header
        assert '@type value2' in header
        assert '@type value3' in header

class TestTagSlice:
    def test_preserves_attributes(self):
        tag = GroupTag('employer', 'value1', 'value2', 'value3', required=True, hidden=True, limit=5)
        tag2 = tag.tagslice(0, 1)
        assert tag2.required == tag.required
        assert tag2.hidden == tag.hidden
        assert tag2.limit == tag.limit

    def test_applies_slice_to_data(self):
        tag = GroupTag('employer', 'value1', 'value2', 'value3')
        tag2 = tag.tagslice(1, 2)
        assert tag2.data == {'value2': Tag('rank')}

def test_first_gets_just_first_element():
    tag = GroupTag('employer', 'value1', 'value2', 'value3')
    tag2 = tag.first()
    assert tag2.data == {'value1': Tag('rank')}

def test_remaining_gets_all_other_elements():
    tag = GroupTag('employer', 'value1', 'value2', 'value3')
    tag2 = tag.remaining()
    assert tag2.data == {'value2': Tag('rank'), 'value3': Tag('rank')}

class TestContains:
    def test_wildcard_with_any_values_is_true(self):
        tag = GroupTag('group', 'value1', 'value2', 'value3')
        assert tag.contains('*')

    def test_matches_wrong_case(self):
        tag = GroupTag('group', 'value1', 'value2', 'value3')
        assert tag.contains('VALUE1')

    def test_matches_partial_values(self):
        tag = GroupTag('group', 'value1', 'value2', 'value3')
        assert tag.contains('val')

    def test_matches_subvalues(self):
        tag = GroupTag('group', 'value1', 'value2', 'value3')
        tag['value1'].append('subval1')
        assert tag.contains('subval1')

class TestFirstValue:
    def test_returns_string_if_present(self):
        tag = GroupTag('type', 'value1', 'value2')
        assert tag.first_value() == 'value1'

    def test_returns_none_if_no_values(self):
        tag = GroupTag('type')
        assert tag.first_value() is None

def test_bool_truthy_when_present():
    tag = GroupTag('type')
    assert not tag
    tag.append('human')
    assert tag

class TestHideValues:
    def test_when_hidden_removes_all_values(self):
        tag = GroupTag('group', 'value1', 'value2', 'value3', hidden=True)
        tag.hide_values()
        assert not tag

    def test_when_not_hidden_removes_nothing(self):
        tag = GroupTag('group', 'value1', 'value2', 'value3', hidden=False)
        tag.hide_values()
        assert list(tag) == ['value1', 'value2', 'value3']

    def test_hides_subtags(self):
        tag = GroupTag('group', 'value1', 'value2', 'value3', hidden=False)
        tag.subtag('value1').append('subvalue')
        tag.subtag('value1').hidden = True
        tag.hide_values()
        assert not tag.subtag('value1')

def test_touch_shows_error(capsys):
    tag = GroupTag('group')
    tag.touch()
    _, err = capsys.readouterr()
    assert "Calling touch() on non-flag class GroupTag object 'group'" in err
