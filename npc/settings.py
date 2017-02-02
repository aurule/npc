"""
Handle settings storage and fetching

Also has a helper function to check loaded settings for faults.
"""

import json
from os import path
from datetime import datetime
from collections import OrderedDict

import npc
from npc import util
from .__version__ import __version__

class Settings:
    """
    Load and store settings

    Default settings are loaded from support/settings-default.json in the
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

    install_base = path.dirname(path.realpath(__file__))

    default_settings_path = path.join(install_base, 'support/')
    user_settings_path = path.expanduser('~/.config/npc/')
    campaign_settings_path = '.npc/'

    settings_files = ['settings.json', 'settings-changeling.json']
    settings_paths = [default_settings_path, user_settings_path, campaign_settings_path]

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
                `support/settings.json` should never be found, but will still
                be reported.
        """
        self.verbose = verbose
        self.data = util.load_json(path.join(self.default_settings_path, 'settings-default.json'))

        # massage template names into real paths
        self.data['templates'] = self._expand_filenames(base_path=self.install_base, data=self.data['templates'])

        # merge additional settings files
        for settings_path in self.settings_paths:
            for file in self.settings_files:
                try:
                    self.load_more(path.join(settings_path, file))
                except OSError as err:
                    # All of these files are optional, so normally we silently
                    # ignore these errors
                    if self.verbose:
                        util.error(err.strerror, err.filename)

    def _expand_filenames(self, base_path, data):
        """
        Recursively expand template filenames into full, canonical paths

        Assumes that every non-dict value is a path string.

        Args:
            base_path (str): Base path for relative pathing
            data (dict): Dict containing path information, possibly nested

        Returns:
            Dict with altered paths
        """
        expanded_data = {}
        for key, value in data.items():
            if isinstance(value, dict):
                expanded_data[key] = self._expand_filenames(base_path, value)
            else:
                expanded_data[key] = path.join(base_path, path.expanduser(value))

        return expanded_data

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
            loaded = util.load_json(settings_path)
        except json.decoder.JSONDecodeError as err:
            util.error(err.nicemsg)
            return

        # paths should be evaluated relative to the settings file in settings_path
        absolute_path_base = path.dirname(path.realpath(settings_path))
        if 'templates' in loaded:
            loaded['templates'] = self._expand_filenames(absolute_path_base, loaded['templates'])
        if 'support' in loaded:
            loaded['support'] = self._expand_filenames(absolute_path_base, loaded['support'])

        self.data = self._merge_settings(loaded, self.data)

    def _merge_settings(self, new_data, orig):
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
            orig (dict): Dict to receive the merge

        Returns:
            Dict containing elements from both dicts.
        """
        dest = dict(orig)

        for key, val in new_data.items():
            if key in dest:
                if isinstance(dest[key], dict):
                    dest[key] = self._merge_settings(val, dest[key])
                else:
                    dest[key] = val
            else:
                dest[key] = val

        return dest

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

        return path.join(base_path, filename)

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
            except KeyError:
                if self.verbose:
                    util.error("Key not found: {}".format(key))
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
            title=self.get('metadata.title'),
            campaign=self.get('campaign'),
            created=datetime.now().strftime(self.get('metadata.timestamp')),
            npc=__version__,
            **self.get('metadata.additional_keys.all'),
            **self.get('metadata.additional_keys.{}'.format(target_format))
        )

class InternalSettings(Settings, metaclass=util.Singleton):
    """
    Singleton settings class.

    Used as the default settings for all exposed functions in the commands
    module. Allows default settings to be used seamlessly.
    """
    pass

def lint_changeling_settings(prefs):
    """
    Check correctness of changeling-specific settings.

    To be correct, the changeling settings must have a blessing and curse for
    every seeming, and a blessing for every kith. Duplicate names between
    seemings and kiths *are not* reported.

    Args:
        prefs (Settings): Settings object to check

    Returns:
        A list of string error messages, or an empty list if no errors were
        found.
    """
    blessing_keys = set(prefs.get('changeling.blessings', {}).keys())
    curse_keys = set(prefs.get('changeling.curses', {}).keys())
    seemings = set(prefs.get('changeling.seemings', []))
    idx_kiths = prefs.get('changeling.kiths', {})
    kiths = set(util.flatten(idx_kiths.values()))

    ok_result = (blessing_keys.issuperset(seemings) and
                 curse_keys.issuperset(seemings) and
                 blessing_keys.issuperset(kiths))

    errors = []
    if not ok_result:
        errors.append("Mismatch in changeling settings:")

        if not blessing_keys.issuperset(seemings):
            errors.append("* Seemings without blessings:")
            for seeming in seemings.difference(blessing_keys):
                errors.append("  - {}".format(seeming))
        if not curse_keys.issuperset(seemings):
            errors.append("* Seemings without curses:")
            for seeming in seemings.difference(curse_keys):
                errors.append("  - {}".format(seeming))
        if not blessing_keys.issuperset(kiths):
            errors.append("* Kiths without blessings:")
            for kith in kiths.difference(blessing_keys):
                errors.append("  - {}".format(kith))

    return errors
