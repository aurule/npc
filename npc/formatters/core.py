"""
Output formatters

The submodules in this package handle the logic for creating specially formatted
output for a few different commands. Each has one or more functions named after
the command they are designed for. Functions designed to work for the same
command share most of the same arguments, though optional arguments are
sometimes available.
"""

import tempfile
from mako.template import Template
from markdown import Markdown
from functools import lru_cache

from npc.util import result

class TemplateFormatter:
    """
    Abstract formatter base class

    This class does all the work to create a character listing using Mako
    templates. It is designed to be subclassed in order to implement specific
    output formats.
    """
    def __init__(self, **kwargs):
        """
        Create a formatter

        Args:
            metadata (dict): Additional metadata to insert. Ignored unless
                metadata_format is set. The keys 'title', and 'created' will
                overwrite the generated values for those keys.
            metadata_format (string|None): Whether to include metadata, and what
                format to use. Accepts a value of 'meta'. Metadata will always
                contain a title and creation date, if included.
            sectioners (List[Sectioner]): List of sectioner objects that create
                section headings for each character. Omit to have no section
                headings.
            partial (bool): Whether to produce partial output by omitting the
                head and other tags. Only the content of the body is created.
                Does not allow metadata to be included, so the metadata_format
                and metadata args are ignored.
            update_progress (function): Callback function to track the progress of
                generating a listing. Must accept the current count and total count.
                Should print to stderr.
            prefs (Settings): Settings object. Used to get the location of
                template files.
        """

        self.metadata = kwargs.get('metadata', {})
        self.metadata_format = kwargs.get('metadata_format')
        self.sectioners = kwargs.get('sectioners', [])
        self.partial = kwargs.get('partial', False)
        self.update_progress = kwargs.get('update_progress', lambda i, t: False)
        self.prefs = kwargs.get('prefs')

        self.encoding_options = {}
        self.header_args = {
            "metadata": self.metadata
        }

        if self.sectioners:
            self.character_header_level = max(s.heading_level for s in self.sectioners) + 1
        else:
            self.character_header_level = 1

    @property
    def list_format(self):
        """
        Format key for this template formatter

        Key string to use when looking up this formatter's templates in
        settings. Must be defined by subclasses.

        Raises:
            NotImplementedError -- Subclasses are responsible for implementing this property
        """
        raise NotImplementedError

    def render(self, characters, outstream):
        """
        Create a listing

        Args:
            characters (list): Character info dicts to show
            outstream (stream): Output stream

        Returns:
            A util.Result object. Openable will not be set.
        """

        @lru_cache(maxsize=32)
        def _prefs_cache(key):
            """
            Cache template paths
            """
            return self.prefs.get(key)

        header_result = self.render_header(outstream)
        if not header_result:
            return header_result

        with tempfile.TemporaryDirectory() as tempdir:
            # directly access certain functions for speed
            _out_write = outstream.write

            total = len(characters)
            self.update_progress(0, total)
            for index, char in enumerate(characters):
                for sectioner in self.sectioners:
                    if sectioner.would_change(char):
                        sectioner.update_text(char)
                        _out_write(sectioner.render_template(self.list_format, **self.encoding_options))
                body_file = _prefs_cache("listing.templates.{list_format}.character.{type}".format(list_format=self.list_format, type=char.type_key))
                if not body_file:
                    body_file = _prefs_cache("listing.templates.{list_format}.character.default".format(list_format=self.list_format))
                if not body_file:
                    return result.ConfigError(errmsg="Cannot find default character template for {list_format} listing".format(list_format=self.list_format))

                body_template = Template(filename=str(body_file), module_directory=tempdir, **self.encoding_options)
                _out_write(body_template.render(**self.char_args(char)))
                self.update_progress(index + 1, total)

        self.render_footer(outstream)

        return result.Success()

    def render_header(self, outstream):
        """
        Render the header template

        Will return immediately without rendering if `self.partial` is true.

        Args:
            outstream (stream): Output stream

        Returns:
            A util.Result object. Openable will not be set.
        """
        if self.partial or not self.metadata_format:
            return result.Success()

        # load and render template
        header_file = self.prefs.get(
            "listing.templates.{list_format}.header.{metadata_format}".format(
                list_format=self.list_format,
                metadata_format=self.metadata_format))
        if not header_file:
            return result.OptionError(errmsg="Unrecognized metadata format '{}'".format(self.metadata_format))

        header_template = Template(filename=str(header_file), **self.encoding_options)
        outstream.write(header_template.render(**self.header_args))

        return result.Success()

    def render_footer(self, outstream):
        """
        Render the footer template

        Will return immediately without rendering if `self.partial` is true.

        Args:
            outstream (stream): Output stream

        Returns:
            None
        """
        if self.partial:
            return

        footer_template = Template(
            filename=str(self.prefs.get(
                "listing.templates.{list_format}.footer".format(
                    list_format=self.list_format))),
            **self.encoding_options)
        outstream.write(footer_template.render())

    def char_args(self, character):
        """
        Create template keyword args for a character

        These are passed directly to the character templates. Useful to override
        this if your templates take additional arguments.

        Args:
            character (Character): Character for the arguments

        Returns:
            Dict of arguments
        """
        return {
            "character": character,
            "header_level": self.character_header_level
        }

class MarkdownFormatter(TemplateFormatter):
    """
    Template formatter for markdown listings
    """
    def __init__(self, **kwargs):
        """
        Create a markdown formatter

        Manipulates the `metadata_format` to allow additional values than are
        defined in the settings.

        Args:
            metadata (dict): Additional metadata to insert. Ignored unless
                metadata_format is set. The keys 'title', and 'created' will
                overwrite the generated values for those keys.
            metadata_format (string|None): Whether to include metadata, and what
                format to use. Accepts a value of 'meta'. Metadata will always
                contain a title and creation date, if included.
            sectioners (List[Sectioner]): List of sectioner objects that create
                section headings for each character. Omit to have no section
                headings.
            partial (bool): Whether to produce partial output by omitting the
                head and other tags. Only the content of the body is created.
                Does not allow metadata to be included, so the metadata_format
                and metadata args are ignored.
            update_progress (function): Callback function to track the progress of
                generating a listing. Must accept the current count and total count.
                Should print to stderr.
            prefs (Settings): Settings object. Used to get the location of
                template files.
        """
        super().__init__(**kwargs)

        # coerce metadata format to canonical form
        if self.metadata_format == "yaml":
            self.metadata_format = "yfm"
        elif self.metadata_format == "multimarkdown":
            self.metadata_format = 'mmd'

    @property
    def list_format(self):
        return 'markdown'

class HtmlFormatter(TemplateFormatter):
    """
    Template formatter for html listings
    """
    def __init__(self, **kwargs):
        """
        Create an html formatter

        Args:
            metadata (dict): Additional metadata to insert. Ignored unless
                metadata_format is set. The keys 'title', and 'created' will
                overwrite the generated values for those keys.
            metadata_format (string|None): Whether to include metadata, and what
                format to use. Accepts a value of 'meta'. Metadata will always
                contain a title and creation date, if included.
            sectioners (List[Sectioner]): List of sectioner objects that create
                section headings for each character. Omit to have no section
                headings.
            partial (bool): Whether to produce partial output by omitting the
                head and other tags. Only the content of the body is created.
                Does not allow metadata to be included, so the metadata_format
                and metadata args are ignored.
            update_progress (function): Callback function to track the progress of
                generating a listing. Must accept the current count and total count.
                Should print to stderr.
            prefs (Settings): Settings object. Used to get the location of
                template files.
            encoding (string): Encoding format of the output text. Overrides the
                value in settings.
        """
        super().__init__(**kwargs)

        self.encoding = kwargs.get('encoding', self.prefs.get('listing.html_encoding'))
        self.encoding_options = {
            'output_encoding': self.encoding,
            'encoding_errors': 'xmlcharrefreplace'
        }
        self.header_args = {
            "encoding": self.encoding,
            'encoding_errors': 'xmlcharrefreplace',
            "metadata": self.metadata
        }

        self.metadata_format = kwargs.get('metadata_format', 'plain')

        self.md_converter = Markdown(extensions=['markdown.extensions.smarty'])
        self._clean_conv = self.md_converter.reset

    @property
    def list_format(self):
        return 'html'

    def char_args(self, character):
        """
        Create template keyword args for a character suitable for html templates

        These are passed directly to the character templates.

        Args:
            character (Character): Character for the arguments

        Returns:
            Dict of arguments
        """
        return {
            "character": character,
            "header_level": self.character_header_level,
            "mdconv": self._clean_conv().convert
        }
