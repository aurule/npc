from tests.fixtures import tmp_campaign

from npc.listers import CharacterLister

def test_uses_generated_suffix(tmp_campaign):
    lister = CharacterLister(tmp_campaign.characters, lang="markdown")

    assert lister.group_template_name == "group_heading.md"
