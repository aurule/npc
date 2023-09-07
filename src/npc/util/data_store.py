from .functions import merge_data_dicts, prepend_namespace

import logging
logger = logging.getLogger(__name__)

class DataStore:
    """Base class for storing and retrieving structured data

    Has the base logic for storing a dict of data, with methods for fetching and modifying it.
    """
    def __init__(self, data_in = None):
        self.data: dict = {}
        if data_in:
            self.merge_data(data_in)

    def __bool__(self) -> bool:
        """Get whether this object is considered "filled"

        A DataStore delegates its bool test to the underlying dict, so it is true when some data is in the
        dict, and false if not.

        Returns:
            bool: True if the store has data, False if not
        """
        return bool(self.data)

    def get(self, key, default=None) -> any:
        """
        Get the value of a key

        Use the period character to indicate a nested key. So, the key
        "alpha.beta.charlie" is looked up like
        `data['alpha']['beta']['charlie']`.

        Args:
            key (str): Key to get
            default (any): Value to return when key isn't found.

        Returns:
            The value in that key, or None if the key could not be resolved.
        """
        key_parts: list = key.split('.')
        current_data = self.data
        for k in key_parts:
            try:
                current_data = current_data[k]
            except (KeyError, TypeError):
                logger.debug(f"Key not found: {key}")
                return default
        return current_data

    def set(self, key: str, value: any):
        """Write a value to a key

        As with get, use the period character to indicate a nested key. The final member of the key will have
        its value overwritten completely.

        Args:
            key (str): Period-delimited key to set
            value (any): New value for the final member of the key

        Raises:
            TypeError: Raised when accessing a list
        """
        key_parts: list = key.split('.')
        terminus: str = key_parts.pop()
        current_data = self.data
        for k in key_parts:
            try:
                current_data = current_data[k]
            except KeyError:
                logger.debug(f"Key not found: {key}")
                current_data[k] = {}
                current_data = current_data[k]
            except TypeError:
                logger.error(f"Cannot access list at {key} as a dict")
                raise TypeError(f"Cannot access list at {key} as a dict")

        try:
            current_data[terminus] = value
        except TypeError:
            logger.error(f"Cannot write string key '{terminus}' to list at '{'.'.join(key_parts)}'")
            raise TypeError(f"Cannot write string key '{terminus}' to list at '{'.'.join(key_parts)}'")

    def merge_data(self, new_data: dict, namespace: str = None) -> None:
        """Merge a dict of data with this object

        Updates this object's data with the values from new_data. If namespace is provided, everything from
        new_data is placed within a dict using namespace as the key.

        Args:
            new_data (dict|DataStore): Dict of data values to merge with this object
            namespace (str): Optional namespace to use for new_data
        """
        if isinstance(new_data, self.__class__):
            new_data = new_data.data

        dict_to_merge = prepend_namespace(new_data, namespace)
        self.data = merge_data_dicts(dict_to_merge, self.data)
