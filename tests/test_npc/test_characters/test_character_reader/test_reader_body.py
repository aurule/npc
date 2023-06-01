from tests.fixtures import fixture_file

from npc.characters import CharacterReader

def test_parses_on_call():
    file = fixture_file("sheets", "reader", "Test Mann - testing bro.npc")
    reader = CharacterReader(file)

    assert "--Notes--" in reader.body()

def test_allows_manual_parsing_on_call():
    file = fixture_file("sheets", "reader", "Test Mann - testing bro.npc")
    reader = CharacterReader(file)

    reader.parse_file()

    assert "--Notes--" in reader.body()
