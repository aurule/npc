import re

unsafe_win_re = re.compile(r'[\\/:*?"<>|]')

def win_sanitize(raw: str) -> str:
    """Make a string safe for Windows filesystems

    Replaces the unsafe characters in unsafe_win_re with a single underscore

    Args:
        raw (str): String to sanitize

    Returns:
        str: Sanitized string containing no characters which are unsafe for Windows filesystems
    """
    return unsafe_win_re.sub("_", raw)
