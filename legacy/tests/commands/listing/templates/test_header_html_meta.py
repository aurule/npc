import re
import npc
from mako.template import Template

def template_output(metadata, encoding='ascii'):
    template_path = str(npc.settings.InternalSettings().get('listing.templates.html.header.meta'))
    header_template = Template(filename=template_path)
    return header_template.render(metadata=metadata, encoding=encoding)

def test_does_not_include_metadata():
    metadata = {
        "nothing": "no-one",
        "second": "thing",
    }
    output = template_output(metadata)
    assert 'name="nothing" content="no-one"' in output
    assert 'name="second" content="thing"' in output

def test_sets_encoding():
    encoding = 'asdf'
    output = template_output({}, encoding)
    assert 'charset="asdf"' in output

def test_ends_with_open_body_tag():
    output = template_output({})
    assert re.search(r'<body>\n$', output) is not None

def test_inserts_title_metadata_separately():
    metadata = {
        "title": "test page"
    }
    output = template_output(metadata)
    assert '<title>test page</title>' in output
    assert 'name="title" content="test page"' not in output
