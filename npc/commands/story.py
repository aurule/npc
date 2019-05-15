"""
Commands related to story files instead of characters
"""

import re
from os import scandir
from pathlib import Path
from shutil import copy as shcopy

from npc import settings
from npc.util import result, flatten, print_err

SEQUENCE_KEYWORD = 'NNN'
COPY_KEYWORD = '((COPY))'

def session(**kwargs):
    """
    Create the files for a new game session.

    Finds the plot and session log files for the last session, copies the plot,
    and creates a new empty session log. If the latest plot file is ahead of
    the latest session, a new plot file will *not* be created. Likewise if the
    latest session file is ahead, a new session file will *not* be created.

    Args:
        prefs (Settings): Settings object to use. Uses internal settings by
            default.

    Returns:
        Result object. Openable will contain the current and previous session
        log and plot planning files.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    plot_dir = Path(prefs.get('paths.required.plot'))
    session_dir = Path(prefs.get('paths.required.session'))

    if not plot_dir.exists():
        return result.FSError(errmsg="Cannot access plot path '{}'".format(plot_dir))

    if not session_dir.exists():
        return result.FSError(errmsg="Cannot access session path '{}'".format(session_dir))

    plot_template = prefs.get('story.templates.plot')
    if SEQUENCE_KEYWORD not in str(plot_template):
        return result.ConfigError(errmsg="Plot template has no number placeholder ({})".format(SEQUENCE_KEYWORD))
    plot_regex = regex_from_template(plot_template)
    latest_plot = latest_file(plot_dir, plot_regex)

    session_template = prefs.get('story.templates.session')
    if SEQUENCE_KEYWORD not in str(session_template):
        return result.ConfigError(errmsg="Session template has no number placeholder ({})".format(SEQUENCE_KEYWORD))
    session_regex = regex_from_template(session_template)
    latest_session = latest_file(session_dir, session_regex)

    new_number = min(latest_plot.number, latest_session.number) + 1

    def copy_templates(dest_dir, templates):
        """
        Create new story files from templates.

        This is responsible for creating the new file name based on
        `new_number`, loading the template contents, substituting the "NNN" and
        "((COPY))" keywords, and writing the result to the new file.
        """

        def old_file_contents(old_file_path):
            """
            Get the previous file's contents.


            """
            try:
                with open(old_file_path, 'r') as old_file:
                    return old_file.read()
            except (FileNotFoundError, IsADirectoryError):
                return ''

        for template_path in templates:
            if SEQUENCE_KEYWORD not in str(template_path):
                print_err("Template {} has no number placeholder ({})".format(template_path, SEQUENCE_KEYWORD))
                continue

            new_file_name = template_path.name.replace(SEQUENCE_KEYWORD, str(new_number))
            destination = dest_dir.joinpath(new_file_name)
            if destination.exists():
                continue

            with open(template_path, 'r') as f:
                data = f.read()

            data = data.replace(SEQUENCE_KEYWORD, str(new_number))
            if COPY_KEYWORD in data:
                file_regex = regex_from_template(template_path)
                old_file_path = latest_file(dest_dir, file_regex).path
                data = data.replace(COPY_KEYWORD, old_file_contents(old_file_path))

            with open(destination, 'w') as f:
                f.write(data)

    plot_templates = flatten([
        prefs.get('story.templates.plot'),
        prefs.get('story.templates.plot_extras')
    ])
    copy_templates(plot_dir, plot_templates)

    session_templates = flatten([
        prefs.get('story.templates.session'),
        prefs.get('story.templates.session_extras')
    ])
    copy_templates(session_dir, session_templates)

    openable = [
        str(latest_file(session_dir, session_regex).path),
        str(latest_file(plot_dir, plot_regex).path)
    ]
    old_session_name = session_template.name.replace(SEQUENCE_KEYWORD, str(new_number - 1))
    old_session = session_dir.joinpath(old_session_name)
    if old_session.exists():
        openable.append(str(old_session))
    old_plot_name = plot_template.name.replace(SEQUENCE_KEYWORD, str(new_number - 1))
    old_plot = plot_dir.joinpath(old_plot_name)
    if old_plot.exists():
        openable.append(str(old_plot))

    return result.Success(openable=openable)

def latest(thingtype='', **kwargs):
    """
    Open the latest plot and/or session file

    Args:
        thingtype (str): Type of the things to return. Use "session" to get the
            latest session file, "plot" to get the latest plot, and anything
            else to get all plot and session files.
        prefs (Settings): Settings object to use. Uses internal settings by
            default.

    Returns:
        Result object. Openable will contain the path(s) to the requested file(s).
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    plot_dir = Path(prefs.get('paths.required.plot'))
    session_dir = Path(prefs.get('paths.required.session'))

    if not plot_dir.exists():
        return result.FSError(errmsg="Cannot access plot path '{}'".format(plot_dir))

    if not session_dir.exists():
        return result.FSError(errmsg="Cannot access session path '{}'".format(session_dir))

    plot_template = prefs.get('story.templates.plot')
    plot_regex = regex_from_template(plot_template)
    latest_plot = latest_file(plot_dir, plot_regex)

    session_template = prefs.get('story.templates.session')
    session_regex = regex_from_template(session_template)
    latest_session = latest_file(session_dir, session_regex)

    if thingtype == 'session':
        openable = [str(latest_session.path)]
    elif thingtype == 'plot':
        openable = [str(latest_plot.path)]
    else:
        openable = [str(latest_session.path), str(latest_plot.path)]

    return result.Success(openable=openable)

def regex_from_template(template_path):
    """
    Turn a template name into a regex

    Template names are transformed by replacing instances of the string "NNN"
    with a regex pattern matching one or more digits. The first instance becomes
    a named capture group while the rest are simply matched. The first number is
    the only one used by NPC.

    Args:
        template_path (str): Template path string to parse

    Returns:
        Regex object
    """
    chopped_name = Path(template_path).name
    regex_string = chopped_name.replace(SEQUENCE_KEYWORD, r'(?P<number>\d+)', 1).replace(SEQUENCE_KEYWORD, r'\d+')
    return re.compile("^{regex_string}$".format(regex_string=regex_string), flags=re.I)

class LatestFileInfo:
    """Simple object to hold a file's path and extracted number"""

    def __init__(self, path, number):
        self.path = path
        self.number = number

def latest_file(target_path, target_regex):
    """
    Get the "latest" file in target_path that matches target_regex

    Args:
        target_path (str): Path to search for the latest file
        target_regex (regex): Regex to match against files. Must contain a
            capture group named 'number'.

    Result:
        OLD Dict contianing information about the file found that matches the regex
        and has the largest captured number.
    """

    def file_matches(f):
        """Whether a file exists and matches the target_regex"""

        # `and true` is needed here to force the result to be boolean
        return f.is_file() and target_regex.match(f.name) and True

    buncha_files = [f.name for f in scandir(target_path) if file_matches(f)]
    try:
        latest_file = max(buncha_files, key=lambda f: target_regex.match(f).group('number'))
        file_number = int(target_regex.match(latest_file).group('number'))
    except ValueError:
        latest_file = ''
        file_number = 0

    return LatestFileInfo(target_path.joinpath(latest_file), file_number)
