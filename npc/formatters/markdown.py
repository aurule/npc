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
        partial (bool): Whether to produce partial output by omitting the
            header and footer. Does not allow metadata to be included, so the
            include_metadata and metadata args are ignored.
        prefs (Settings): Settings object. Used to get the location of template
            files.
        sectioner (function): Function that returns a section heading for each
            character. When its return value changes, the section template is
            rendered with the new title. Omit to suppress sections.
        progress (function): Callback function to track the progress of
            generating a listing. Must accept the current count and total count.
            Should print to stderr.

    Returns:
        A util.Result object. Openable will not be set.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    if not metadata:
        metadata = {}
    sectioner = kwargs.get('sectioner', lambda c: '')
    update_progress = kwargs.get('progress', lambda i, t: False)

    if not partial:
        if include_metadata:
            # coerce to canonical form
            if include_metadata == "yaml":
                include_metadata = "yfm"
            elif include_metadata == "multimarkdown":
                include_metadata = 'mmd'

            # load and render template
            header_file = prefs.get("listing.templates.markdown.header.{}".format(include_metadata))
            if not header_file:
                return result.OptionError(errmsg="Unrecognized metadata format '{}'".format(include_metadata))

            header_template = Template(filename=header_file)
            outstream.write(header_template.render_unicode(metadata=metadata))

    with tempfile.TemporaryDirectory() as tempdir:
        # directly access certain functions for speed
        _prefs_get = prefs.get
        _out_write = outstream.write

        section_title = ''
        section_template = Template(
            filename=_prefs_get("listing.templates.markdown.section"),
            module_directory=tempdir)
        total = len(characters)
        update_progress(0, total)
        for index, char in enumerate(characters):
            if sectioner(char) != section_title:
                section_title = sectioner(char)
                _out_write(
                    section_template.render_unicode(
                        title=section_title))
            body_file = _prefs_get("listing.templates.markdown.character.{}".format(char.type_key))
            if not body_file:
                body_file = _prefs_get("listing.templates.markdown.character.default")
            if not body_file:
                return result.ConfigError(errmsg="Cannot find default character template for markdown listing")

            body_template = Template(filename=body_file, module_directory=tempdir)
            _out_write(body_template.render_unicode(character=char))
            update_progress(index + 1, total)

    if not partial:
        footer_template = Template(filename=prefs.get("listing.templates.markdown.footer"))
        outstream.write(footer_template.render_unicode())
    return result.Success()

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
        table_template = Template(filename=prefs.get("report.templates.markdown"), module_directory=tempdir)

        for key, table in tables.items():
            outstream.write(table_template.render(data=table, tag=key))

    return result.Success()
