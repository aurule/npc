"""
Markdown formatter for creating a page of characters.

Has a single entry point `dump`.
"""

import codecs
import html
import markdown
import tempfile
from .. import util
from mako.template import Template

def dump(characters, outstream, *, include_metadata=None, metadata=None, prefs=None):
    """
    Create a markdown character listing

    Args:
        characters (list): Character info dicts to show
        outstream (stream): Output stream
        include_metadata (string|None): Whether to include metadata, and what
            format to use.What kind of metadata to include, if any. Accepts
            values of 'mmd', 'yaml', or 'yfm'. Metadata will always include a
            title and creation date.
        metadata (dict): Additional metadata to insert. Ignored unless
            include_metadata is set. The keys 'title', and 'created' will
            overwrite the generated values for those keys.
        prefs (Settings): Settings object. Used to get the location of template
            files.

    Returns:
        A util.Result object. Openable will not be set.
    """
    if not metadata:
        metadata = {}

    # encode as ascii unless our stream has an opinion
    try:
        encoding = outstream.encoding
    except AttributeError:
        encoding = 'ascii'

    modstream = codecs.getwriter(encoding)(outstream, errors='xmlcharrefreplace')

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
        modstream.write("<!DOCTYPE html>\n<html>\n<head></head>\n<body>\n")

    with tempfile.TemporaryDirectory() as tempdir:
        md = markdown.Markdown(extensions=['markdown.extensions.extra'])
        for char in characters:
            body_file = prefs.get("templates.listing.character.html.{}".format(char.get_type_key()))
            if not body_file:
                body_file = prefs.get("templates.listing.character.html.default")
            body_template = Template(filename=body_file, module_directory=tempdir)
            modstream.write(
                md.reset().convert(
                    body_template.render(
                        character=char.copy_and_alter(html.escape))
                ))
    modstream.write("</body>\n</html>\n")
    return util.Result(True)
