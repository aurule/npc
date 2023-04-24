from .functions import merge_data_dicts, prepend_namespace

import logging
logger = logging.getLogger(__name__)

class DataStore:
    """Base class for storing and retrieving structured data

    Has the base logic for storing a dict of data, with methods for fetching and modifying it.
    """
    def __init__(self):
        self.data: dict = {}

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
                logger.debug("Key not found: {}".format(key))
                return default
        return current_data


    def merge_data(self, new_data: dict, namespace: str = None) -> None:
        """Merge a dict of data with this object

        Updates this object's data with the values from new_data. If namespace is provided, everything from
        new_data is placed within a dict using namespace as the key.

        Args:
            new_data (dict): Dict of data values to merge with this object
            namespace (str): Optional namespace to use for new_data
        """
        dict_to_merge = prepend_namespace(new_data, namespace)
        self.data = merge_data_dicts(dict_to_merge, self.data)
