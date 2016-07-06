import json
import sys
from os import path

from . import util

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

    def __init__(self, verbose = False):
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

        for k, v in self.data['templates'].items():
            self.data['templates'][k] = path.join(self.install_base, v)

        for settings_path in self.settings_paths:
            for file in self.settings_files:
                try:
                    self.load_more(path.join(settings_path, file))
                except OSError as e:
                    # All of these files are optional, so normally we silently
                    # ignore these errors
                    if self.verbose:
                        util.error(e.strerror, e.filename)

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
        except json.decoder.JSONDecodeError as e:
            util.error(e.nicemsg)
            return

        def evaluate_paths(base, loaded, key):
            if key in loaded:
                loaded[key] = {k: path.join(absolute_path_base, path.expanduser(v)) for k, v in loaded[key].items()}

        # paths should be evaluated relative to the settings file in settings_path
        absolute_path_base = path.dirname(path.realpath(settings_path))
        evaluate_paths(absolute_path_base, loaded, 'support')
        evaluate_paths(absolute_path_base, loaded, 'templates')

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

        for k, v in new_data.items():
            if k in dest:
                if isinstance(dest[k], dict):
                    dest[k] = self._merge_settings(v, dest[k])
                else:
                    dest[k] = v
            else:
                dest[k] = v

        return dest

    def get_settings_path(self, settings_type):
        """
        Get a settings file path

        Args:
            settings_type (str): Settings path to get. One of 'default', 'user', or 'campaign'.

        Returns
            Path of the named settings file.
        """
        if settings_type == 'default':
            return path.join(self.default_settings_path, 'settings-default.json')

        if settings_type == 'user':
            return path.join(self.user_settings_path, 'settings.json')

        if settings_type == 'campaign':
            return path.join(self.campaign_settings_path, 'settings.json')

    def get(self, key, default = None):
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
        d = self.data
        for k in key_parts:
            try:
                d = d[k]
            except KeyError:
                if self.verbose:
                    util.error("Key not found: %s" % key)
                return default
        return d

    def get_metadata(self, fmt):
        return {**self.get('additional_metadata.all'), **self.get('additional_metadata.%s' % fmt)}

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
        True if the changeling settings are OK, False if there were errors.
        Errors are printed to stderr.
    """
    blessing_keys = set(prefs.get('changeling.blessings', {}).keys())
    curse_keys = set(prefs.get('changeling.curses', {}).keys())
    seemings = set(prefs.get('changeling.seemings', []))
    kiths = set(prefs.get('changeling.kiths', []))

    ok = (blessing_keys.issuperset(seemings) and
            curse_keys.issuperset(seemings) and
            blessing_keys.issuperset(kiths))

    if not ok:
        util.error("Mismatch in changeling settings")

        if not blessing_keys.issuperset(seemings):
            util.error("    Seemings without blessings:")
            for s in seemings.difference(blessing_keys):
                util.error("        %s" % s)
        if not curse_keys.issuperset(seemings):
            util.error("    Seemings without curses:")
            for s in seemings.difference(curse_keys):
                util.error("        %s" % s)
        if not blessing_keys.issuperset(kiths):
            util.error("    Kiths without blessings:")
            for k in kiths.difference(blessing_keys):
                util.error("        %s" % k)

    return ok
