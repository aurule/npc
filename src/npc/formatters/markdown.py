"""
Markdown formatter for creating a page of characters.
"""

import tempfile
from mako.template import Template

import npc
from npc import settings
from npc.util import result

SUPPORTED_METADATA_TYPES = ['yaml', 'yfm', 'multimarkdown', 'mmd']
"""Recognized metadata type names"""

def listing(characters, outstream, *, metadata=None, partial=False, **kwargs):
    """
    Create a markdown character listing

    Args:
        characters (list): Character info dicts to show
        outstream (stream): Output stream
        metadata_format (string|None): Whether to include metadata, and what
            format to use. Accepts values of 'mmd', 'yaml', or 'yfm'. Metadata
            will always include a title and creation date.
        metadata (dict): Additional metadata to insert. Ignored unless
            metadata_format is set. The keys 'title', and 'created' will
            overwrite the generated values for those keys.
        partial (bool): Whether to produce partial output by omitting the
            header and footer. Does not allow metadata to be included, so the
            metadata_format and metadata args are ignored.
        prefs (Settings): Settings object. Used to get the location of template
            files.
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

    renderer = npc.formatters.MarkdownFormatter(
        metadata=metadata,
        sectioners=kwargs.get('sectioners', []),
        update_progress=kwargs.get('update_progress', lambda i, t: False),
        partial=partial,
        metadata_format=kwargs.get('metadata_format'),
        prefs=prefs
    )

    return renderer.render(characters, outstream)

def report(tables, outstream, **kwargs):
    """
    Create one or more MultiMarkdown tables

    Table data format:
    The tables arg must be a dictionary of collections.Counter objects indexed
    by the name of the tag whose data is stored in the Counter. The tag name
    will be titleized and used as the header for that column of the report.

    Args:
        tables (dict): Table data to use. Tables has a very particular format.
        outstream (stream): Output stream
        prefs (Settings): Settings object. Used to get the location of template
            files.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())

    with tempfile.TemporaryDirectory() as tempdir:
        table_template = Template(filename=str(prefs.get("report.templates.markdown")), module_directory=tempdir)

        for key, table in tables.items():
            outstream.write(table_template.render(data=table, tag=key))

    return result.Success()
