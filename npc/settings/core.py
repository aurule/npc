"""
Handle settings storage and fetching

Also has a helper function to check loaded settings for faults.
"""

from datetime import datetime
from collections import OrderedDict
from copy import deepcopy
from pathlib import Path

import npc
from npc import util
from npc.linters.settings import lint

class Settings:
    """
    Load and store settings

    Default settings are loaded from settings/settings-default.json in the
    install path. Additional settings are loaded from the paths in
    `settings_paths`.

    Do not access settings values directly. Use the get() method.

    Attributes:
        install_base (str): Directory path containing this file
        default_settings_path (str): Path to the default settings file
        user_settings_path (str): Path to the user settings directory for the
            current user. Only correct on *nix systems.
        campaign_settings_path (str): Path to the campaign settings directory.
        settings_files (list): List of allowed settings file names.
        settings_paths (list): List of allowed settings paths.
        data (dict): Dictionary of settings data. Should not be referenced
            directly. Instead, use the get() method.
    """

    def __init__(self, verbose=False):
        """
        Loads all settings files.

        The default settings are loaded first, followed by user settings and
        finally campaign settings. Keys from later files overwrite those from
        earlier files.

        Only the default settings need to exist. If a different file cannot be
        found or opened, it will be silently ignored without crashing.

        Args:
            verbose (bool): Whether to show additional error messages that are
                usually ignored. These involve unloadable optional settings
                files and keys that cannot be found. The file
                `settings/settings.json` should never be found, but will still
                be reported.
        """

        self.module_base = Path(__file__).parent
        self.install_base = Path(self.module_base).parent

        self.default_settings_path = self.module_base
        self.user_settings_path = Path('~/.config/npc/').expanduser()
        self.campaign_settings_path = Path('.npc/')

        self.settings_files = [
            'settings.json',
            'settings-changeling.json',
            'settings-werewolf.json',
            'settings-gui.json'
        ]
        self.settings_paths = [self.default_settings_path, self.user_settings_path, self.campaign_settings_path]

        self.verbose = verbose
        loaded_data = util.load_json(self.default_settings_path.joinpath('settings-default.json'))

        # massage template names into real paths
        self.data = self._expand_templates(base_path=self.install_base, settings_data=loaded_data)

        # merge additional settings files
        for settings_path in self.settings_paths:
            for file in self.settings_files:
                try:
                    self.load_more(settings_path.joinpath(file))
                except OSError as err:
                    # All of these files are optional, so normally we silently
                    # ignore these errors
                    if self.verbose:
                        util.print_err(err.strerror, err.filename)

    def _expand_templates(self, base_path, settings_data):
        """
        Expand all known template paths in a settings file

        Args:
            base_path (str): Base path for relative pathing
            settings_data (dict): Full settings data

        Returns:
            Dict of settings data with expanded template paths
        """

        def expand_filenames(data):
            def expanded_path(value):
                return base_path.joinpath(value).expanduser().resolve()

            outdata = {}
            for key, value in data.items():
                if isinstance(value, dict):
                    outdata[key] = expand_filenames(value)
                elif isinstance(value, list):
                    outdata[key] = [expanded_path(v) for v in value]
                else:
                    outdata[key] = expanded_path(value)
            return outdata

        def get(data, key, default=None):
            key_parts = key.split('.')
            current_data = data
            for k in key_parts:
                try:
                    current_data = current_data[k]
                except (KeyError, TypeError):
                    return default
            return current_data

        working_data = deepcopy(settings_data)

        # types.*.sheet_template
        for typekey, _ in get(working_data, 'types', {}).items():
            type_path = get(working_data, "types.{}.sheet_template".format(typekey))
            if type_path:
                working_data['types'][typekey]['sheet_template'] = base_path.joinpath(type_path).expanduser()

        # story.templates.*
        story_templates = get(working_data, 'story.templates')
        if story_templates:
            working_data['story']['templates'] = expand_filenames(story_templates)

        # report.templates.*
        report_templates = get(working_data, 'report.templates')
        if report_templates:
            working_data['report']['templates'] = expand_filenames(report_templates)

        # listing.templates.*
        listing_templates = get(working_data, 'listing.templates')
        if listing_templates:
            working_data['listing']['templates'] = expand_filenames(listing_templates)

        return working_data

    def load_more(self, settings_path):
        """
        Load additional settings from a file

        Settings values from this file will override the defaults. Any errors
        while opening the file are suppressed and the file will simply not be
        loaded. In that case, existing values are left alone.

        Args:
            settings_path (str): Path to the new json file to load
        """
        try:
            loaded = util.load_settings(settings_path)
        except util.errors.ParseError as err:
            util.print_err(err.strerror)
            return

        # paths should be evaluated relative to the settings file in settings_path
        absolute_path_base = Path(settings_path).resolve().parent
        loaded = self._expand_templates(absolute_path_base, loaded)

        self._merge_settings(loaded)

    def update_key(self, key, value):
        """
        Change the value of a single settings key

        Args:
            key (str): Period-delimited key to update
            value (any): New value to store in the key
        """
        key_parts = key.split('.')
        for k in reversed(key_parts):
            value = {k: value}

        self._merge_settings(value)

    def _merge_settings(self, new_data):
        """
        Merge data from one dict into another.

        Keys in new_data that are not present in orig are added. Keys in orig
        and not in new_data remain untouched.

        Keys in both new_data and orig are compared. If orig[key] is a dict,
        then new_data[key] is assumed to also be a dict. Those two dicts are
        then merged and that result inserted in place of orig[key]. If orig[key]
        is not a dict, then the value of new_data[key] replaces it.

        Args:
            new_data (dict): Dict to merge

        Returns:
            Dict containing elements from both dicts.
        """
        def merge_dict(new_data, orig):
            dest = dict(orig)

            for key, val in new_data.items():
                if key in dest:
                    if isinstance(dest[key], dict):
                        dest[key] = merge_dict(val, dest[key])
                    else:
                        dest[key] = val
                else:
                    dest[key] = val

            return dest

        self.data = merge_dict(new_data, self.data)

    def get_settings_path(self, location, settings_type=None):
        """
        Get a settings file path

        Does not check that the path goes to a settings file that will actually
        be loaded. If a settings type is given that is not supported by default,
        it will need to be loaded manually.

        Args:
            location (str): Settings path to get. One of 'default', 'user', or
                'campaign'.
            settings_type (str): Type of settings file to get. If set to 'base'
                or left unspecified, the normal settings file is used.

        Returns
            Path of the named settings file.
        """
        if location == 'default':
            base_path = self.default_settings_path
        if location == 'user':
            base_path = self.user_settings_path
        if location == 'campaign':
            base_path = self.campaign_settings_path

        if settings_type and settings_type != 'base':
            filename = "settings-{}.json".format(settings_type)
        else:
            if location == 'default':
                filename = 'settings-default.json'
            else:
                filename = 'settings.json'

        return base_path.joinpath(filename)

    def get(self, key, default=None):
        """
        Get the value of a settings key

        Use the period character to indicate a nested key. So, the key
        "alpha.beta.charlie" is looked up like
        `data['alpha']['beta']['charlie']`.

        Args:
            key (str): Key to get from settings.
            default (any): Value to return when key isn't found.

        Returns:
            The value in that key, or None if the key could not be resolved.
        """
        key_parts = key.split('.')
        current_data = self.data
        for k in key_parts:
            try:
                current_data = current_data[k]
            except (KeyError, TypeError):
                if self.verbose:
                    util.print_err("Key not found: {}".format(key))
                return default
        return current_data

    def get_metadata(self, target_format):
        """
        Get the metadata hash for a given output format

        Merges default keys with the keys in "all" and finally the keys in the
        named format.

        Default keys:
            title: Configured metadata title
            campaign: Configured name of the campaign
            created: Timestamp when the metadata was fetched, formatted as per
                settings
            npc: Version of NPC which created this metadata

        Args:
            target_format (str): Format identifier. Must appear in the settings
                files.

        Returns:
            Dict of metadata keys and values.
        """
        return OrderedDict(
            title=self.get('listing.metadata.title'),
            campaign=self.get('campaign_name'),
            created=datetime.now().strftime(self.get('listing.metadata.timestamp')),
            npc=npc.__version__.__version__,
            **self.get('listing.metadata.universal.additional_keys'),
            **self.get('listing.metadata.{}.additional_keys'.format(target_format))
        )

    def get_type_paths(self):
        """
        Get all of the folder names for each defined character type.

        Yields:
            List of configured path names
        """
        for _, data in self.get('types').items():
            yield data['type_path']

    def get_available_types(self):
        """
        Get a list of all configured type names

        Returns:
            List of strings, one for each configured type
        """
        return self.get('types').keys()

    def get_ignored_paths(self, command_name):
        """
        Get a list of paths that should be ignored, based on the named command

        Args:
            command_name (str): Name of the command being run. Used to look up
                command-specific ignored paths

        Returns:
            List of string paths
        """
        command_ignores = self.get("paths.ignore.{command_name}".format(command_name=command_name), [])
        global_ignores = self.get('paths.ignore.always', [])
        return command_ignores + global_ignores

    def translate_tag_for_character_type(self, char_type, tag_name):
        """
        Translate a type-dependent tag into the corresponding tag for the
        character's type.

        Args:
            type (string): Type to use
            tag_name (string): Name of the tag to translate
        """
        return self.get(
            'types.{char_type}.tag_names.{tag_name}'.format(
                char_type=char_type,
                tag_name=tag_name),
            tag_name)


class InternalSettings(Settings, metaclass=util.Singleton):
    """
    Singleton settings class.

    Used as the default settings for all exposed functions in the commands
    module. Allows default settings to be used seamlessly.
    """
    pass

def lint_settings(prefs):
    """
    Check the correctness of all loaded settings.

    Uses the linters.settings package to do the work.

    Args:
        prefs (Settings): Settings object to check

    Returns:
        A list of string error messages, or an empty list if no errors were
        found.
    """
    return lint(prefs)
