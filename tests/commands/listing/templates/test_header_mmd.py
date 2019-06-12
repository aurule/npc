import npc
from mako.template import Template

def template_output(metadata):
    template_path = str(npc.settings.InternalSettings().get('listing.templates.markdown.header.mmd'))
    header_template = Template(filename=template_path)
    return header_template.render(metadata=metadata)

def test_includes_metadata():
    metadata = {
        "nothing": "no-one",
        "second": "thing",
    }
    output = template_output(metadata)
    assert "Nothing: no-one" in output
    assert "Second: thing" in output

def test_titleizes_keys():
    metadata = {
        "SOMETHING": "nothing"
    }
    output = template_output(metadata)
    assert "Something: nothing" in output
