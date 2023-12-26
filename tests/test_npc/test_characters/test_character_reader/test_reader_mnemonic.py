from npc.characters import CharacterReader

def test_starts_after_sep(tmp_path):
    file = tmp_path / "test name - test mnemonic.npc"
    file.touch()
    reader = CharacterReader(file)

    result = reader.mnemonic()

    assert result == "test mnemonic"

def test_no_sep_no_mnemonic(tmp_path):
    file = tmp_path / "test name.npc"
    file.touch()
    reader = CharacterReader(file)

    result = reader.mnemonic()

    assert result == ""
