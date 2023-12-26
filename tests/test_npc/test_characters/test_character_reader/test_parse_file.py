from tests.fixtures import fixture_file

from npc.characters import CharacterReader

def test_body_includes_section_name():
    file = fixture_file("sheets", "reader", "Test Mann - testing bro.npc")
    reader = CharacterReader(file)

    reader.parse_file()

    assert "--Notes--" in reader._body

def test_body_includes_remainder():
    file = fixture_file("sheets", "reader", "Test Mann - testing bro.npc")
    reader = CharacterReader(file)

    reader.parse_file()

    assert "I am a test and I'm testing your code" in reader._body

def test_tags_handles_simple_values():
    file = fixture_file("sheets", "reader", "Test Mann - testing bro.npc")
    reader = CharacterReader(file)

    reader.parse_file()

    assert reader._tags[2].value == "person"

def test_tags_handles_complex_values():
    file = fixture_file("sheets", "reader", "Test Mann - testing bro.npc")
    reader = CharacterReader(file)

    reader.parse_file()

    assert reader._tags[3].value == "The Testiest Mann Alive"

def test_tags_includes_descriptions():
    file = fixture_file("sheets", "reader", "Test Mann - testing bro.npc")
    reader = CharacterReader(file)

    reader.parse_file()

    assert reader._tags[0].value == "Test Mann is a helpful test helper."
    assert reader._tags[1].value == "He has two paragraphs of descriptive text, because why not?"

def test_tags_includes_flags():
    file = fixture_file("sheets", "reader", "Test Mann - testing bro.npc")
    reader = CharacterReader(file)

    reader.parse_file()

    assert reader._tags[4].name == "sticky"

def test_uses_defaults_for_blank_file():
    file = fixture_file("sheets", "reader", "Blank Mann - nada.npc")
    reader = CharacterReader(file)

    reader.parse_file()

    assert reader._body == ""
    assert reader._tags == []
