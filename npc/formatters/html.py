"""
HTML formatter for creating a page of characters.
"""

import tempfile
from mako.template import Template

import npc
from npc import settings
from npc.util import result

SUPPORTED_METADATA_TYPES = ['meta']
"""Recognized metadata type names"""

def listing(characters, outstream, *, metadata=None, partial=False, **kwargs):
    """
    Create an html character listing

    Args:
        characters (list): Character info dicts to show
        outstream (stream): Output stream
        metadata_format (string|None): Whether to include metadata, and what
            format to use. Accepts a value of 'meta'. Metadata will always
            contain a title and creation date, if included.
        metadata (dict): Additional metadata to insert. Ignored unless
            metadata_format is set. The keys 'title', and 'created' will
            overwrite the generated values for those keys.
        partial (bool): Whether to produce partial output by omitting the head
            and other tags. Only the content of the body tag is created.
            Does not allow metadata to be included, so the metadata_format and
            metadata args are ignored.
        prefs (Settings): Settings object. Used to get the location of template
            files.
        encoding (string): Encoding format of the output text. Overrides the
            value in settings.
        sectioners (List[BaseSectioner]): List of BaseSectioner objects to
            render section templates based on character attributes. Omit to
            suppress sections.
        progress (function): Callback function to track the progress of
            generating a listing. Must accept the current count and total count.
            Should print to stderr.

    Returns:
        A util.Result object. Openable will not be set.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    if metadata is None:
        metadata = {}

    renderer = npc.formatters.HtmlFormatter(
        metadata=metadata,
        sectioners=kwargs.get('sectioners', []),
        update_progress=kwargs.get('update_progress', lambda i, t: False),
        partial=partial,
        metadata_format=kwargs.get('metadata_format'),
        encoding=kwargs.get('encoding', prefs.get('listing.html_encoding')),
        prefs=prefs
    )

    return renderer.render(characters, outstream)

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
