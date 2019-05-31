from npc.character.tags import Flag

def test_present_with_no_values():
    flag = Flag('wanderer')
    flag.touch()
    assert flag.present

def test_header_present_with_no_values():
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
