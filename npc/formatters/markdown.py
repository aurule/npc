"""
Markdown formatter for creating a page of characters.
"""

import tempfile
from mako.template import Template

import npc
from npc import settings
from npc.util import result

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
        progress (function): Callback function to track the progress of
            generating a listing. Must accept the current count and total count.
            Should print to stderr.

    Returns:
        A util.Result object. Openable will not be set.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    if not metadata:
        metadata = {}
    update_progress = kwargs.get('progress', lambda i, t: False)

    if include_metadata:
        # coerce to canonical form
        if include_metadata == "yaml":
            include_metadata = "yfm"

        # load and render template
        header_file = prefs.get("listing.templates.markdown.header.{}".format(include_metadata))
        if not header_file:
            return result.OptionError(errmsg="Unrecognized metadata format '{}'".format(include_metadata))

        header_template = Template(filename=header_file)
        outstream.write(header_template.render(metadata=metadata))

    with tempfile.TemporaryDirectory() as tempdir:
        # directly access certain functions for speed
        _prefs_get = prefs.get
        _out_write = outstream.write

        total = len(characters)
        update_progress(0, total)
        for index, char in enumerate(characters):
            body_file = _prefs_get("listing.templates.markdown.character.{}".format(char.type_key))
            if not body_file:
                body_file = _prefs_get("listing.templates.markdown.character.default")
            if not body_file:
                return result.ConfigError(errmsg="Cannot find default character template for markdown listing")

            body_template = Template(filename=body_file, module_directory=tempdir)
            _out_write(body_template.render(character=char))
            update_progress(index + 1, total)

    return result.Success()

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
        table_template = Template(filename=prefs.get("report.templates.markdown"), module_directory=tempdir)

        for key, table in tables.items():
            outstream.write(table_template.render(data=table, tag=key))

    return result.Success()
