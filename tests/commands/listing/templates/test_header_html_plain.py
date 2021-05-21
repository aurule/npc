import re
import npc
from mako.template import Template

def template_output(metadata, encoding='ascii'):
    template_path = str(npc.settings.InternalSettings().get('listing.templates.html.header.plain'))
    header_template = Template(filename=template_path)
    return header_template.render(metadata=metadata, encoding=encoding)

def test_does_not_include_metadata():
    metadata = {
        "nothing": "no-one",
        "second": "thing",
    }
    output = template_output(metadata)
    assert "no-one" not in output
    assert "thing" not in output

def test_sets_encoding():
    encoding = 'asdf'
    output = template_output({}, encoding)
    assert 'charset="asdf"' in output

def test_ends_with_open_body_tag():
    output = template_output({})
    assert re.search(r'<body>\n$', output) is not None
