# Helpers common to the gui

from contextlib import contextmanager

@contextmanager
def safe_command(command):
    """
    Helper to suppress AttributeErrors from commands

    Args:
        command (callable): The command to run. Any AttributeError raised by
            the command will be suppressed.
    """
    try:
        yield command
    except AttributeError as err:
        pass
