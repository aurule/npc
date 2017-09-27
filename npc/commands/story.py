"""
Commands related to story files instead of characters
"""

import re
from os import path, scandir
from shutil import copy as shcopy

from npc import settings
from npc.util import result

def session(**kwargs):
    """
    Create the files for a new game session.

    Finds the plot and session log files for the last session, copies the plot,
    and creates a new empty session log.

    Args:
        prefs (Settings): Settings object to use. Uses internal settings by
            default.

    Returns:
        Result object. Openable will contain the current and previous session
        log and plot planning files.
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    plot_path = prefs.get('paths.plot')
    session_path = prefs.get('paths.session')

    if not (path.exists(plot_path) and path.exists(session_path)):
        return result.FSError(errmsg="Cannot access paths '{}' and/or '{}'".format(plot_path, session_path))

    plot_re = re.compile(r'(?i)^plot (?P<number>\d+)$')
    session_re = re.compile(r'(?i)^session (?P<number>\d+)$')

    def get_latest(target_path, target_regex):
        """Get the "latest" file in target_path that matches target_regex"""
        buncha_files = [f.name for f in scandir(target_path) if f.is_file() and target_regex.match(path.splitext(f.name)[0])]
        try:
            latest_file = max(buncha_files, key=lambda f: re.split(r'\s', f)[1])
            (bare_name, bare_ext) = path.splitext(latest_file)
            file_match = target_regex.match(bare_name)
            file_number = int(file_match.group('number'))
        except ValueError:
            latest_file = ''
            bare_ext = '.md'
            file_number = 0

        return {
            'name': latest_file,
            'ext': bare_ext,
            'number': file_number,
            'path': path.join(target_path, latest_file),
            'exists': file_number > 0
        }

    # find latest plot and session file
    latest_plot = get_latest(plot_path, plot_re)
    latest_session = get_latest(session_path, session_re)

    new_number = min(latest_plot['number'], latest_session['number']) + 1

    openable = []
    if latest_session['exists']:
        if latest_session['number'] < new_number:
            # create new session log
            old_session_path = latest_session['path']
            new_session_path = path.join(session_path, "session {num}{ext}".format(num=new_number, ext=latest_session['ext']))
            shcopy(prefs.get('templates.session'), new_session_path)
        else:
            # present existing session files, since we don't have to create one
            old_session_path = path.join(session_path, "session {num}{ext}".format(num=latest_session['number'] - 1, ext=latest_session['ext']))
            new_session_path = latest_session['path']
        openable.extend((new_session_path, old_session_path))
    else:
        # no existing session, so just copy the template
        template_path = prefs.get('templates.session')
        new_session_path = path.join(session_path, "session {num}{ext}".format(num=new_number, ext=path.splitext(template_path)[1]))
        shcopy(template_path, new_session_path)
        openable.append(new_session_path)

    if latest_plot['exists']:
        if latest_plot['number'] < new_number:
            # copy old plot
            old_plot_path = latest_plot['path']
            new_plot_path = path.join(plot_path, "plot {num}{ext}".format(num=new_number, ext=latest_plot['ext']))
            shcopy(old_plot_path, new_plot_path)
        else:
            # present existing plot files, since we don't have to create one
            old_plot_path = path.join(plot_path, "plot {num}{ext}".format(num=latest_plot['number'] - 1, ext=latest_plot['ext']))
            new_plot_path = latest_plot['path']
        openable.extend((new_plot_path, old_plot_path))
    else:
        # no old plot to copy, so create a blank
        new_plot_path = path.join(plot_path, "plot {num}{ext}".format(num=new_number, ext=prefs.get('plot_ext')))
        with open(new_plot_path, 'w') as new_plot:
            new_plot.write(' ')
        openable.append(new_plot_path)

    return result.Success(openable=openable)
