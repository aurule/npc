"""
HTML formatter for creating a page of characters.
"""

import html
import tempfile
from markdown import Markdown
from mako.template import Template
from operator import attrgetter

import npc
from npc import settings
from npc.util import result

SUPPORTED_METADATA_TYPES = ['meta']
"""Recognized metadata type names"""

def listing(characters, outstream, *, include_metadata=None, metadata=None, partial=False, **kwargs):
    """
    Create an html character listing

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
        sectioners (List[function]): List of functions that return a section
            heading for each character. When its return value changes, the
            section template is rendered with the new title. Omit to suppress
            sections.
        progress (function): Callback function to track the progress of
            generating a listing. Must accept the current count and total count.
            Should print to stderr.

    Returns:
        A util.Result object. Openable will not be set.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    encoding = kwargs.get('encoding', prefs.get('listing.html_encoding'))
    if not metadata:
        metadata = {}
    sectioners = kwargs.get('sectioners', [])
    update_progress = kwargs.get('progress', lambda i, t: False)

    if not len(sectioners):
        character_header_level = 1
    else:
        character_header_level = max(sectioners, key=attrgetter('heading_level')).header_level + 1

    encoding_options = {
        'output_encoding': encoding,
        'encoding_errors': 'xmlcharrefreplace'
    }

    if not partial:
        if include_metadata:
            # load and render template
            header_file = prefs.get("listing.templates.html.header.{}".format(include_metadata))
            if not header_file:
                return result.OptionError(errmsg="Unrecognized metadata format option '{}'".format(include_metadata))

            header_template = Template(filename=header_file, **encoding_options)
            outstream.write(header_template.render(encoding=encoding, metadata=metadata))
        else:
            header_template = Template(filename=prefs.get("listing.templates.html.header.plain"), **encoding_options)
            outstream.write(header_template.render(encoding=encoding))

    with tempfile.TemporaryDirectory() as tempdir:
        md_converter = Markdown(extensions=['markdown.extensions.smarty'])

        # directly access certain functions for speed
        _clean_conv = md_converter.reset
        _prefs_get = prefs.get
        _out_write = outstream.write

        total = len(characters)
        update_progress(0, total)
        for index, char in enumerate(characters):
            for sectioner in sectioners:
                if sectioner.would_change(char):
                    sectioner.update_text(char)
                    _out_write(sectioner.render_template('html', **encoding_options))
            body_file = _prefs_get("listing.templates.html.character.{}".format(char.type_key))
            if not body_file:
                body_file = _prefs_get("listing.templates.html.character.default")
            body_template = Template(filename=body_file, module_directory=tempdir, **encoding_options)
            _out_write(
                body_template.render(
                    character=char.copy_and_alter(html.escape),
                    header_level=character_header_level,
                    mdconv=_clean_conv().convert
                    ))
            update_progress(index + 1, total)

    if not partial:
        footer_template = Template(filename=prefs.get("listing.templates.html.footer"), **encoding_options)
        outstream.write(footer_template.render())
    return result.Success()

def report(tables, outstream, **kwargs):
    """
    Create one or more html tables

    Table data format:
    The tables arg must be a dictionary of collections.Counter objects indexed
    by the name of the tag whose data is stored in the Counter. The tag name
    will be titleized and used as the header for that column of the report.

    Args:
        tables (dict): Table data to use
        outstream (stream): Output stream
        prefs (Settings): Settings object. Used to get the location of template
            files.
        encoding (string): Encoding format of the output text. Overrides the
            value in settings.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    encoding = kwargs.get('encoding', prefs.get('report.html_encoding'))

    encoding_options = {
        'output_encoding': encoding,
        'encoding_errors': 'xmlcharrefreplace'
    }

    with tempfile.TemporaryDirectory() as tempdir:
        table_template = Template(
            filename=prefs.get("report.templates.html"),
            module_directory=tempdir,
            **encoding_options)

        for key, table in tables.items():
            outstream.write(table_template.render(data=table, tag=key))

    return result.Success()
