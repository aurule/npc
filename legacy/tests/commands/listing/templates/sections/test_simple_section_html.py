import npc
from mako.template import Template

def template_output(sectioner):
    template_path = str(npc.settings.InternalSettings().get('listing.templates.html.sections.simple'))
    section_template = Template(filename=template_path)
    return section_template.render(sectioner=sectioner)

def test_generates_header_tag_for_header_level(prefs):
    sectioner = npc.formatters.sectioners.LastInitialSectioner(3, prefs)
    sectioner.current_text = 'test text'
    output = template_output(sectioner)

    assert '<h3>' in output

def test_includes_current_text(prefs):
    sectioner = npc.formatters.sectioners.LastInitialSectioner(3, prefs)
    sectioner.current_text = 'test text'
    output = template_output(sectioner)

    assert 'test text' in output

def test_formatted_output(prefs):
    sectioner = npc.formatters.sectioners.LastInitialSectioner(3, prefs)
    sectioner.current_text = 'test text'
    output = template_output(sectioner)

    assert output == '\n<h3>test text</h3>\n'
