from npc_cli.presenters import wrapped_paragraphs

def test_yields_one_string_per_line():
    data = "asdf\nfdsa"

    result = list(wrapped_paragraphs(data))

    assert len(result) == 2
