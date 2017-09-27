"""
Commands related to story files instead of characters
"""

import re
from os import path, scandir
from shutil import copy as shcopy

from npc import settings
from npc.util import result

PLOT_REGEX = re.compile(r'(?i)^plot (?P<number>\d+)$')
SESSION_REGEX = re.compile(r'(?i)^session (?P<number>\d+)$')

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
    plot_path = prefs.get('paths.plot')
    session_path = prefs.get('paths.session')

    if not (path.exists(plot_path) and path.exists(session_path)):
        return result.FSError(errmsg="Cannot access paths '{}' and/or '{}'".format(plot_path, session_path))

    latest_plot = latest_file_info(plot_path, PLOT_REGEX)
    latest_session = latest_file_info(session_path, SESSION_REGEX)

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

def latest(thingtype, **kwargs):
    """
    Open the latest plot and/or session file

    Args:
        prefs (Settings): Settings object to use. Uses internal settings by
            default.

    Returns:
        Result object. Openable will contain the path(s) to the requested file(s).
    """
    prefs = kwargs.get('prefs', settings.InternalSettings())
    plot_path = prefs.get('paths.plot')
    session_path = prefs.get('paths.session')

    if not (path.exists(plot_path) and path.exists(session_path)):
        return result.FSError(errmsg="Cannot access paths '{}' and/or '{}'".format(plot_path, session_path))

    latest_plot = latest_file_info(plot_path, PLOT_REGEX)
    latest_session = latest_file_info(session_path, SESSION_REGEX)
    if thingtype == 'both':
        openable = [latest_plot['path'], latest_session['path']]
    elif thingtype == 'session':
        openable = [latest_session['path']]
    elif thingtype == 'plot':
        openable = [latest_plot['path']]
    else:
        return result.OptionError(errmsg="Unrecognized type '{}'".format(thingtype))

    return result.Success(openable=openable)


def latest_file_info(target_path, target_regex):
    pass
