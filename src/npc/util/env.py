from os import environ

def testing() -> bool:
    """Get whether we're in testing mode

    returns the value of the TESTING env var, defaulting to False

    Returns:
        bool: True if in testing, false if not
    """
    return environ.get("TESTING", False)
