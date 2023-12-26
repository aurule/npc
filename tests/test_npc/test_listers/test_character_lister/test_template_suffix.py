from tests.fixtures import tmp_campaign

from npc.listers import CharacterLister

def test_gets_supported_suffix(tmp_campaign):
    lister = CharacterLister(tmp_campaign.characters, lang="markdown")

    assert lister.template_suffix == "md"

def test_returns_unsupported_suffix(tmp_campaign):
    lister = CharacterLister(tmp_campaign.characters, lang="test")

    assert lister.template_suffix == "test"
