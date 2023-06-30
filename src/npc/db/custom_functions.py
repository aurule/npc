def last_word(string_in: str) -> str:
    """Get the last word in a string

    Words are treated as space-separated character collections. If there is only
    a single word in the string, that word will be returned.

    This helper is designed specifically to be used as a custom sql function and
    not for general use.

    Args:
        string_in (str): The string to extract from

    Returns:
        str: The last word in the string
    """
    return string_in.split()[-1]

def first_word(string_in: str) -> str:
    """Get the first word in a string

    Words are treated as space-separated character collections. If there is only
    a single word in the string, that word will be returned.

    This helper is designed specifically to be used as a custom sql function and
    not for general use.

    Args:
        string_in (str): The string to extract from

    Returns:
        str: The first word in the string
    """
    return string_in.split()[0]
