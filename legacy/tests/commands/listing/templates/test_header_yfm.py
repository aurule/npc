import re
import npc
from mako.template import Template

def template_output(metadata):
    template_path = str(npc.settings.InternalSettings().get('listing.templates.markdown.header.yfm'))
    header_template = Template(filename=template_path)
    return header_template.render(metadata=metadata)

def test_includes_metadata():
    metadata = {
        "nothing": "no-one",
        "second": "thing",
    }
    output = template_output(metadata)
    assert "nothing: no-one" in output
    assert "second: thing" in output

def test_wraps_metadata_in_dashes():
    metadata = {
        "nothing": "no-one",
        "second": "thing",
    }
    output = template_output(metadata)
    assert re.match(r'---.*---\n', output, re.DOTALL) is not None
