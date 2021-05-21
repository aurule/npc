from npc.character.tags import DescriptionTag

def test_saves_default_values():
    tag = DescriptionTag('type', 'asdf', '1234')
    assert 'asdf' in tag
    assert '1234' in tag

def test_header_has_no_tag_name():
    flag = DescriptionTag('something', 'asdf', '', '1234')
    header = flag.to_header()
    assert "something\nasdf\n\n1234" in header
