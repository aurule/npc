from npc.characters import CharacterReader

def test_stops_at_sep(tmp_path):
    file = tmp_path / "test name - test mnemonic.npc"
    file.touch()
    reader = CharacterReader(file)

    result = reader.name()

    assert result == "test name"

def test_no_sep_stops_at_ext(tmp_path):
    file = tmp_path / "test name.npc"
    file.touch()
    reader = CharacterReader(file)

    result = reader.name()

    assert result == "test name"
