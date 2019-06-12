from npc.character.tags import UnknownTag

def test_saves_default_values():
    tag = UnknownTag('type', 'asdf', '1234')
    assert 'asdf' in tag
    assert '1234' in tag

def test_header_present_with_no_values():
    tag = UnknownTag('something')
    header = tag.to_header()
    assert '@something' in header

def test_present_with_no_values():
    tag = UnknownTag('something')
    assert not tag.present
    assert not tag.filled

class TestStrictValidation:
    def test_always_invalid(self):
        tag = UnknownTag('type', 'asdf', '1234')
        tag.validate(strict=True)
        assert not tag.valid
        assert "Unrecognized tag 'type'"
