import pytest
from io import StringIO
from importlib import resources
from shutil import copy
from tests.fixtures import tmp_campaign, db
from npc.campaign import Campaign

from npc.listers import CharacterLister

def files_and_expected() -> list:
    files = resources.files("tests.test_npc.test_listers.test_character_lister.character_lister_output")
    return [f for f in files.iterdir() if f.suffix == '.npc']

def get_expected(output_format, target_file) -> str:
    all_files = resources.files("tests.test_npc.test_listers.test_character_lister.character_lister_output")
    suffix = "." + CharacterLister.LANG_SUFFIXES[output_format]
    file = all_files.joinpath(target_file.with_suffix(suffix))
    if not file.exists():
        return ""
    return file.read_text()

@pytest.mark.parametrize("output_format", CharacterLister.SUPPORTED_LANGUAGES)
@pytest.mark.parametrize("character_file", files_and_expected())
def test_character_files_output(db, tmp_campaign, output_format, character_file):
    copy(character_file, tmp_campaign.characters_dir)
    tmp_campaign.characters.db = db
    tmp_campaign.characters.refresh()
    lister = CharacterLister(tmp_campaign.characters, lang=output_format)
    lister_output = StringIO()

    lister.list(target=lister_output)

    expected_output = get_expected(output_format, character_file)
    if not expected_output:
        pytest.xfail("No expected output available")
    print(f"File: {character_file.name}",
          "===Expected===",
          expected_output,
          "===Received===",
          lister_output.getvalue(),
          sep="\n")
    assert expected_output in lister_output.getvalue()
