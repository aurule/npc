"""
HTML formatter for creating a page of characters.
"""

import codecs
import html
import tempfile
from markdown import Markdown
from mako.template import Template
from .. import util, settings

def listing(characters, outstream, *, include_metadata=None, metadata=None, partial=False, **kwargs):
    """
    Create a markdown character listing

    Args:
        characters (list): Character info dicts to show
        outstream (stream): Output stream
        include_metadata (string|None): Whether to include metadata, and what
            format to use. Accepts values of 'mmd', 'yaml', or 'yfm'. Metadata
            will always include a title and creation date.
        metadata (dict): Additional metadata to insert. Ignored unless
            include_metadata is set. The keys 'title', and 'created' will
            overwrite the generated values for those keys.
        prefs (Settings): Settings object. Used to get the location of template
            files.
        partial (bool): Whether to produce partial output by omitting the head
            and other tags. Only the content of the body tag is created.
            Does not allow metadata to be included, the include_metadata and
            metadata args are ignored.
        encoding (string): Encoding format of the output text. Overrides the
            value in settings.
        sectioner (function): Function that returns a section heading for each
            character. When its return value changes, the section template is
            rendered with the new title. Omit to suppress sections.

    Returns:
        A util.Result object. Openable will not be set.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    encoding = kwargs.get('encoding', prefs.get('html_encoding'))
    if not metadata:
        metadata = {}
    sectioner = kwargs.get('sectioner', lambda c: '')

    # Get a stream writer that automatically encodes special characters
    modstream = codecs.getwriter(encoding)(outstream, errors='xmlcharrefreplace')

    if not partial:
        if include_metadata:
            # load and render template
            header_file = prefs.get("templates.listing.header.{}".format(include_metadata))
            if not header_file:
                return util.Result(
                    False,
                    errmsg="Unrecognized metadata format option '{}'".format(include_metadata),
                    errcode=6)

            header_template = Template(filename=header_file)
            modstream.write(header_template.render(metadata=metadata))
        else:
            header_template = Template(filename=prefs.get("templates.listing.header.plain"))
            modstream.write(header_template.render(encoding=encoding))

    with tempfile.TemporaryDirectory() as tempdir:
        md_converter = Markdown(extensions=['markdown.extensions.extra', 'markdown.extensions.smarty'])

        # directly access certain functions for speed
        _clean_conv = md_converter.reset
        _prefs_get = prefs.get
        _mod_write = modstream.write

        section_title = ''
        section_template = Template(
            filename=_prefs_get("templates.listing.section.html"),
            module_directory=tempdir)
        for char in characters:
            if sectioner(char) != section_title:
                section_title = sectioner(char)
                _mod_write(
                    _clean_conv().convert(
                        section_template.render(
                            title=section_title)))
            body_file = _prefs_get("templates.listing.character.html.{}".format(char.type_key))
            if not body_file:
                body_file = _prefs_get("templates.listing.character.html.default")
            body_template = Template(filename=body_file, module_directory=tempdir)
            _mod_write(
                _clean_conv().convert(
                    body_template.render(
                        character=char.copy_and_alter(html.escape))))
    if not partial:
        modstream.write("</body>\n</html>\n")
    return util.Result(True)

def report(tables, outstream, **kwargs):
    """
    Create one or more html tables

    Args:
        tables (dict): Table data to use
        outstream (stream): Output stream
        prefs (Settings): Settings object. Used to get the location of template
            files.
        encoding (string): Encoding format of the output text. Overrides the
            value in settings.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    encoding = kwargs.get('encoding', prefs.get('html_encoding'))

    modstream = codecs.getwriter(encoding)(outstream, errors='xmlcharrefreplace')

    with tempfile.TemporaryDirectory() as tempdir:
        table_template = Template(filename=prefs.get("templates.report.html"), module_directory=tempdir)

        for key, table in tables.items():
            modstream.write(table_template.render(data=table, tag=key))

    return util.Result(True)
