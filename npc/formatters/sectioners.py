"""
Module for generating section headings
"""

import tempfile
from pathlib import Path
from mako.template import Template

from npc import util

def get_sectioner(key, heading_level, prefs):
    """
    Helper to get the right built-in sectioner object

    Creates a new sectioner object based on `key`. The special key 'last' will
    get a LastInitialSectioner, otherwise you'll get a TagSectioner.

    Args:
        key (str): Tag name or special word to use for the sectioner.
        heading_level (int): Level of heading this sectioner is for. Stored for
            use in templates.
        prefs (Settings): Settings object used to look up templates and tag name
            translations.

    Returns:
        A BaseSectioner sub-object depending on the key given.
    """
    if key == 'last':
        return LastInitialSectioner(heading_level, prefs)
    else:
        return TagSectioner(key, heading_level, prefs)

class BaseSectioner:
    """
    Core sectioner logic. This is an abstract class and cannot function on its
    own. Extend it to make your own sectioners.

    Each BaseSectioner holds a temporary directory object open until removal.
    This is used to cache the Mako template.

    To get the current text of the object, use `current_text`.

    The intended way to use a sectioner object is to first check if its value
    would change for a character using `would_change()`. If it would, then call
    `update_text()` and store or write the output of `render_template()`.
    """
    def __init__(self, heading_level, prefs):
        """
        Create a sectioner object.

        Args:
            heading_level (int): Level of heading this sectioner is for. Stored
                for use in templates.
            prefs (Settings): Settings object used to look up templates and tag
                name translations.
        """
        self.current_text = None
        self.heading_level = heading_level
        self.prefs = prefs

        self.tempdir = tempfile.TemporaryDirectory()
        self.templates_cache = {} # cache for template objects by format

    def __del__(self):
        """
        Destroy this sectioner object.

        Explicitly cleans up the Mako cache temporary directory.
        """
        self.tempdir.cleanup()

    @property
    def template_key(self):
        """
        Key to use in the settings to find the right template path.

        Must be within 'sections' within every key under 'listing.templates'.
        For example, the default key 'simple' must be set under
        'listing.templates.markdown.sections.simple' and
        'listing.templates.html.sections.simple'.
        """
        return 'simple'


    def text_for(self, character):
        """
        Generate text for a character.

        This method must be overridden in child sectioners. It should not modify
        `current_text`, merely generate a new string based on the given
        character object.

        Args:
            character (Character): Character object to use for generating new
                text.

        Returns:
            String of text data based on the given character.
        """
        raise NotImplementedError

    def would_change(self, character):
        """
        Whether the sectioner's text would be different for the given character

        Args:
            character (Character): Character object to test

        Returns:
            True if the output of `text_for` differs from our `current_text`.
        """
        return self.text_for(character) != self.current_text

    def update_text(self, character):
        """
        Update the stored `current_text` by generating text for the given
        character.

        Args:
            character (Character): Character object to use for generating new
                text.

        Returns:
            None
        """
        self.current_text = self.text_for(character)

    def render_template(self, output_format, **encoding_options):
        """
        Render our template.

        This just gets the template and calls `render` on it with a `sectioner`
        argument. Override this method if your sectioner has different rendering
        logic or other arguments to its template.

        Args:
            output_format (str): Name of the format to use.
            encoding_options (dict): Dictionary of Mako encoding options. Passed
                directly to the Mako `render` call.
        Returns:
            String or bytes object as rendered by Mako.
        """
        return self.template(output_format, **encoding_options).render(sectioner=self)

    def template(self, output_format, **encoding_options):
        """
        Get the Mako template for a given output format

        This method caches the template object by its output format. This means
        that once requested, the encoding options cannot be changed.

        Args:
            output_format (str): Name of the format to use. Must be present in
                the settings.
            encoding_options (dict): Dictionary of Mako encoding options.

        Returns:
            Mako Template object.
        """
        if output_format in self.templates_cache:
            return self.templates_cache[output_format]

        template_path = str(
            Path(
                self.prefs.get(
                    "listing.templates.{output_format}.sections.{template_key}".format(
                        output_format=output_format,
                        template_key=self.template_key))))
        self.templates_cache[output_format] = Template(filename=template_path, module_directory=self.tempdir.name, **encoding_options)
        return self.templates_cache[output_format]

class TagSectioner(BaseSectioner):
    """
    Tag-based sectioner

    This sectioner creates its text from the first value of the named `tag`. It
    translates that tag first if needed according to the user preferences.
    """
    def __init__(self, tag, heading_level, prefs):
        super().__init__(heading_level, prefs)

        self.tag_name = tag
        self.prefs = prefs

    def text_for(self, character):
        """
        Get text based on this object's tag.

        Args:
            character (Character): Character object to use for generating new
                text.

        Returns:
            First value for our tag in the passed character.
        """
        tag = self.prefs.translate_tag_for_character_type(character.type_key, self.tag_name)
        return character.get_first(tag, None)

class LastInitialSectioner(BaseSectioner):
    def text_for(self, character):
        """
        Get text based on the character's last initial.

        Args:
            character (Character): Character object to use for generating new
                text.

        Returns:
            First character of the last word in the character's first value for
            the name tag.
        """
        full_name = character.get_first('name')
        try:
            return None if full_name is None else full_name.split(' ')[-1][0]
        except IndexError as e:
            return None
