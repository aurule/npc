"""
Commands related to story files instead of characters
"""

import re
from os import path, scandir
from shutil import copy as shcopy

from npc import settings
from npc.util import result, flatten

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
    plot_dir = prefs.get('paths.required.plot')
    session_dir = prefs.get('paths.required.session')

    if not path.exists(plot_dir):
        return result.FSError(errmsg="Cannot access plot path '{}'".format(plot_dir))

    if not path.exists(session_dir):
        return result.FSError(errmsg="Cannot access session path '{}'".format(session_dir))

    plot_template = prefs.get('story.templates.plot')
    plot_regex = regex_from_template(plot_template)
    latest_plot = latest_file(plot_dir, plot_regex)

    session_template = prefs.get('story.templates.session')
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
            new_file_name = path.basename(template_path).replace(SEQUENCE_KEYWORD, str(new_number))
            destination = path.join(dest_dir, new_file_name)
            if path.exists(destination):
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
        latest_file(session_dir, session_regex).path,
        latest_file(plot_dir, plot_regex).path
    ]
    old_session_name = path.basename(session_template).replace(SEQUENCE_KEYWORD, str(new_number - 1))
    old_session = path.join(session_dir, old_session_name)
    if path.exists(old_session):
        openable.append(old_session)
    old_plot_name = path.basename(plot_template).replace(SEQUENCE_KEYWORD, str(new_number - 1))
    old_plot = path.join(plot_dir, old_plot_name)
    if path.exists(old_plot):
        openable.append(old_plot)

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
    plot_dir = prefs.get('paths.required.plot')
    session_dir = prefs.get('paths.required.session')

    if not path.exists(plot_dir):
        return result.FSError(errmsg="Cannot access plot path '{}'".format(plot_dir))

    if not path.exists(session_dir):
        return result.FSError(errmsg="Cannot access session path '{}'".format(session_dir))

    plot_template = prefs.get('story.templates.plot')
    plot_regex = regex_from_template(plot_template)
    latest_plot = latest_file(plot_dir, plot_regex)

    session_template = prefs.get('story.templates.session')
    session_regex = regex_from_template(session_template)
    latest_session = latest_file(session_dir, session_regex)

    if thingtype == 'session':
        openable = [latest_session.path]
    elif thingtype == 'plot':
        openable = [latest_plot.path]
    else:
        openable = [latest_session.path, latest_plot.path]

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
    chopped_name = path.basename(template_path)
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

    return LatestFileInfo(path.join(target_path, latest_file), file_number)
