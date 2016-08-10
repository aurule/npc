"""
Markdown formatter for creating a page of characters.
"""

import tempfile
from mako.template import Template
from .. import util, settings

def listing(characters, outstream, *, include_metadata=None, metadata=None, **kwargs):
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

    Returns:
        A util.Result object. Openable will not be set.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    if not metadata:
        metadata = {}

    if include_metadata:
        # coerce to canonical form
        if include_metadata == "yaml":
            include_metadata = "yfm"

        # load and render template
        header_file = prefs.get("templates.listing.header.{}".format(include_metadata))
        if not header_file:
            return util.Result(
                False,
                errmsg="Unrecognized metadata format option '{}'".format(include_metadata),
                errcode=6)

        header_template = Template(filename=header_file)
        outstream.write(header_template.render(metadata=metadata))

    with tempfile.TemporaryDirectory() as tempdir:
        # directly access certain functions for speed
        _prefs_get = prefs.get
        _out_write = outstream.write

        for char in characters:
            body_file = _prefs_get("templates.listing.character.markdown.{}".format(char.type_key))
            if not body_file:
                body_file = _prefs_get("templates.listing.character.markdown.default")
            body_template = Template(filename=body_file, module_directory=tempdir)
            _out_write(body_template.render(character=char))
    return util.Result(True)

def report(tables, outstream, **kwargs):
    """
    Create one or more MultiMarkdown tables

    Args:
        tables (dict): Table data to use
        outstream (stream): Output stream
        prefs (Settings): Settings object. Used to get the location of template
            files.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())

    with tempfile.TemporaryDirectory() as tempdir:
        table_template = Template(filename=prefs.get("templates.report.markdown"), module_directory=tempdir)

        for key, table in tables.items():
            outstream.write(table_template.render(data=table, tag=key))

    return util.Result(True)
