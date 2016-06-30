import json
import sys
from os import path

from . import util

class Settings:
    """Load and store settings

    Default settings are loaded from support/settings-default.json in the
    install path.

    Do not access settings values directly. Use the get() method.
    """

    install_base = path.dirname(path.realpath(__file__))

    default_settings_path = path.join(install_base, 'support/')
    user_settings_path = path.expanduser('~/.config/npc/')
    campaign_settings_path = '.npc/'

    settings_files = ['settings.json', 'settings-changeling.json']
    settings_paths = [default_settings_path, user_settings_path, campaign_settings_path]

    def __init__(self):
        self.data = util.load_json(path.join(self.default_settings_path, 'settings-default.json'))

        for k, v in self.data['templates'].items():
            self.data['templates'][k] = path.join(self.install_base, v)

        for settings_path in self.settings_paths:
            for file in self.settings_files:
                try:
                    self.load_more(path.join(settings_path, file))
                except IOError as e:
                    # all of these files are optional, so we silently ignore these errors
                    pass

    def load_more(self, settings_path):
        """Merge settings from a file

        Settings values from this file will override the defaults. Any errors
        while opening the file are suppressed and the file will simply not be
        loaded. In that case, existing values are left alone.
        """
        try:
            loaded = util.load_json(settings_path)
        except Exception as e:
            if hasattr(e, 'nicemsg'):
                sys.stderr.write(e.nicemsg + "\n")
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
        """Get a settings file path"""
        if settings_type == 'default':
            return path.join(self.default_settings_path, 'settings-default.json')

        if settings_type == 'user':
            return path.join(self.user_settings_path, 'settings.json')

        if settings_type == 'campaign':
            return path.join(self.campaign_settings_path, 'settings.json')

    def get(self, key):
        """Get the value of a settings key

        Use the period character to indicate a nested key.
        """
        key_parts = key.split('.')
        d = self.data
        for k in key_parts:
            try:
                d = d[k]
            except KeyError:
                return None
        return d

    def get_metadata(self, fmt):
        return {**self.get('additional_metadata.all'), **self.get('additional_metadata.%s' % fmt)}

def lint_changeling_settings(prefs):
    blessing_keys = set(prefs.get('changeling.blessings').keys())
    curse_keys = set(prefs.get('changeling.curses').keys())
    seemings = set(prefs.get('changeling.seemings'))
    kiths = set(prefs.get('changeling.kiths'))

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
