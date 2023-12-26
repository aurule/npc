def trim_tags(value: str) -> str:
    """Filter function to remove leading and trailing tags

    This filter is very simple and does not check that the tags match.

    Args:
        value (str): The value to trim

    Returns:
        str: The trimmed value, or the initial value if it is not wrapped in tags.
    """
    try:
        start: int = value.index(">") + 1
        end: int = value.rindex("<", start)

        return value[start:end]
    except ValueError as e:
        return value
