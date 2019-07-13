from npc.character.tags import Flag

def test_present_with_no_values():
    flag = Flag('wanderer')
    flag.touch()
    assert flag.present

def test_not_filled_with_no_values():
    flag = Flag('wanderer')
    flag.touch()
    assert not flag.filled

def test_header_filled_with_no_values():
    flag = Flag('wanderer')
    flag.touch()
    header = flag.to_header()
    assert '@wanderer' in header

class TestValidation:
    def test_required_with_no_values_passes(self):
        tag = Flag('type', required=True)
        tag.touch()
        tag.validate()
        assert tag.valid

    def test_required_with_values_passes(self):
        tag = Flag('type', 'asdf', required=True)
        tag.validate()
        assert tag.valid

    def test_limit_zero_and_required_are_fine(self):
        tag = Flag('type', 'asdf', required=True, limit=0)
        tag.validate()
        assert tag.valid

    def test_hidden_values_must_exist(self):
        tag = Flag('type', 'value1')
        tag.hide_value('value2')
        tag.validate()
        assert not tag.valid
        assert "Value 'value2' for tag 'type' cannot be hidden, because it does not exist" in tag.problems

class TestStrictValidation:
    def test_limit_exceeded(self):
        tag = Flag('type', 'asdf', '1234', limit=1)
        tag.validate(strict=True)
        assert not tag.valid

    def test_under_limit(self):
        tag = Flag('type', 'asdf', '1234', limit=5)
        tag.validate(strict=True)
        assert tag.valid

    def test_negative_limit(self):
        tag = Flag('type', 'asdf', '1234', limit=-1)
        tag.validate(strict=True)
        assert tag.valid

class TestUpdate:
    def test_update_with_boolean_assigns_presence(self):
        tag = Flag('wanderer')
        tag.update(True)
        assert tag.present

    def test_update_from_flag_copies_presence(self):
        copyable = Flag('wanderer')
        copyable.touch()
        tag = Flag('wanderer')
        tag.update(copyable)
        assert tag.present

    def test_update_from_flag_copies_data(self):
        copyable = Flag('wanderer')
        copyable.append('lost')
        tag = Flag('wanderer')
        tag.update(copyable)
        assert tag.data == ['lost']

def test_append_marks_presence_true():
    tag = Flag('wanderer')
    tag.append('')
    assert tag.present

def test_clear_resets_presence():
    tag = Flag('wanderer')
    tag.touch()
    assert tag.present
    tag.clear()
    assert not tag.present

def test_bool_truthy_when_present():
    tag = Flag('foreign')
    assert not tag
    tag.touch()
    assert tag
