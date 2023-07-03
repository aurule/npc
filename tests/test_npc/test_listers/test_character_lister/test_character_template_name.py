from tests.fixtures import tmp_campaign

from npc.listers import CharacterLister

def test_uses_generated_suffix(tmp_campaign):
    lister = CharacterLister(tmp_campaign.characters, lang="markdown")

    assert ".md" in lister.character_template_name("tester")

def test_uses_character_type(tmp_campaign):
    lister = CharacterLister(tmp_campaign.characters, lang="markdown")

    assert "tester" in lister.character_template_name("tester")
