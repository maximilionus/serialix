from typing import Any
from ast import literal_eval
from os import path, makedirs, remove


class BaseLang:
    """
    Base Data Interchange Format (DIF) realisation.

    This class is not intended to be used directly. Instead, it should be inherited by a class, that provides the support
    for DIF language. Inherited class must overwrite the ``_core__read_file_to_dict()`` and ``_core__write_dict_to_file()``
    static methods with real implementation of their functionality that described in the docstring of each method.

    :param file_path: Path to preferred local file destination
        If the file does not exist at the specified path, it will be created
    :type file_path: str
    :param default_dictionary: Default local file path ``str`` or ``dict``
        that will be used for local file start values and , defaults to {}
    :type default_dictionary: Union[str, dict], optional
    :param force_overwrite_file: Whether the file needs to be overwritten if it already exists, defaults to False
    :type force_overwrite_file: bool, optional
    :raises ValueError: If provided data type in argument ``default_dictionary`` is not
        the path ``str`` or ``dict``, this exception will be raised

    .. note::
        Methods ``.clear()``, ``.copy()``, ``.fromkeys()``, ``.get()``, ``.items()``, ``.keys()``, ``values()``,
        ``pop()``, ``popitem()``, ``setdefault()``, ``update()`` are bound to the attribute ``dictionary``,
        so executing:

        >>> this_object.update({"check": True})

        Is equal to:

        >>> this_object.dictionary.update({"check": True})
    """
    def __init__(self, file_path: str, default_dictionary={}, force_overwrite_file=False):
        self.__parsed_dict = {}
        self.local_file_path = file_path

        if isinstance(default_dictionary, dict):
            self.__default_dict = default_dictionary
        elif path.isfile(default_dictionary):
            self.__default_dict = self._core__read_file_to_dict(default_dictionary)
        else:
            raise ValueError("'default_dictionary' argument should be a dictionary or a path to file string. Provided value is {0}"
                             .format(default_dictionary))

        if not self.is_file_exist() or force_overwrite_file:
            create_directories(self.local_file_path)
            self.create_file()

        self.reload()

    def __getitem__(self, key):
        return self.__parsed_dict[key]

    def __setitem__(self, key, value):
        self.__parsed_dict[key] = value

    def __delitem__(self, key):
        self.__parsed_dict.__delitem__(key)

    def __len__(self):
        return len(self.__parsed_dict)

    def __iter__(self):
        return self.__parsed_dict.__iter__()

    def clear(self):
        """ Clear the ``dictionary`` """
        self.__parsed_dict.clear()

    def copy(self) -> dict:
        """Get the copy of ``dictionary``

        :return: ``dictionary`` copy
        :rtype: dict
        """
        return self.__parsed_dict.copy()

    def get(self, key, default=None) -> Any:
        """Get key from ``dictionary``

        :param key: Key name
        :type key: str
        :param default: Default value, if key was not found, defaults to None
        :type default: Any
        :return: Value of requested ``key``, or ``default`` value
            if key wasn't found.
        :rtype: Any
        """
        return self.__parsed_dict.get(key, default)

    def items(self) -> list:
        """Get items of the ``dictionary``

        :return: Items of the ``dictionary`` ((key, value) pairs)
        :rtype: list
        """
        return self.__parsed_dict.items()

    def keys(self) -> list:
        """Get keys of the ``dictionary``

        :return: Keys of the ``dictionary`` (, key)
        :rtype: list
        """
        return self.__parsed_dict.keys()

    def values(self) -> list:
        """Get values of the ``dictionary``

        :return: Values of the ``dictionary`` (, value)
        :rtype: list
        """
        return self.__default_dict.values()

    def pop(self, key: Any, default=None) -> Any:
        """Pop key from ``dictionary``

        :param key: Key name
        :type key: Any
        :param default: Default value, if key was not found, defaults to None
        :type default: Any, optional
        :return: Value of requested ``key``, or ``default`` value
            if key wasn't found, defaults to None.
        :rtype: Any
        """
        return self.__parsed_dict.pop(key, default)

    def popitem(self) -> Any:
        """Pop item from ``dictionary`` in LIFO order.

        :param key: Key name
        :type key: Any
        :param default: Default value, if key was not found, defaults to None
        :type default: Any, optional
        :return: Value of requested ``key``, or ``default`` value
            if key wasn't found, defaults to None.
        :rtype: Any
        """
        return self.__parsed_dict.popitem()

    def setdefault(self, key: Any, default=None) -> Any:
        """
        If key is in the ``dictionary``, return its value.
        If not, insert key with a value of ``default`` and return ``default``

        :param key: Name of the key
        :type key: Any
        :param default: Default value, defaults to None
        :type default: Any, optional
        :return: If key is in the dictionary, return its value, else:
            returns ``defalut``
        :rtype: Any
        """
        return self.__parsed_dict.setdefault(key, default)

    def update(self, dictionary: dict):
        """Update ``dictionary`` with another dictionary

        :param dictionary: Dictionary, that will be merged to
            ``dictionary``
        :type dictionary: dict
        """
        self.__parsed_dict.update(dictionary)

    @property
    def dictionary(self) -> dict:
        """Full access to the dictionary attribute.
        Contains local file data parsed to dictionary

        :return: ``dictionary`` attribute
        :rtype: dict
        """
        return self.__parsed_dict

    @dictionary.setter
    def dictionary(self, dictionary: dict):
        self.__parsed_dict = dictionary

    @property
    def dictionary_default(self) -> dict:
        """Full access to the default dictionary.
        Contains dictionary with default keys that was
        specified in ``default_dictionary`` argument.

        :return: default dictionary
        :rtype: dict
        """
        return self.__default_dict

    @dictionary_default.setter
    def dictionary_default(self, dictionary: dict):
        self.__default_dict = dictionary

    def commit(self):
        """Commit all changes from ``dictionary`` to local file"""
        self.write_dict_to_file(self.__parsed_dict)

    def refresh(self, safe_mode=True):
        """
        Refresh ``dictionary`` values from local file.
        Note that this method does not remove user-added keys,
        it will only add non existent keys and modify the already existing keys.

        :param safe_mode: Provides the recursive merge of dictionary from local
            file to object's ``dictionary``. This option prevents object's nested
            dictionaries to be overwritten by local files, but is much slower than
            simple ``dict.update()`` method call. So if you don't care about nested
            dictionaries be overwritten, you can disable this feature to boost the
            execution speed
        :type safe_mode: bool, optional
        """
        if safe_mode:
            self.__parsed_dict = recursive_dicts_merge(self.read_file_as_dict(), self.__parsed_dict)
        else:
            self.__parsed_dict.update(self.read_file_as_dict())

    def reload(self):
        """Reset the ``dictionary`` attribute to values from local file"""
        self.__parsed_dict = self.read_file_as_dict()

    def reset_to_defaults(self):
        """
        Reset the ``dictionary`` attribute to values from ``dictionary_default`` attribute.
        Note that local file will stay untouched.
        """
        self.__parsed_dict = self.__default_dict.copy()

    def create_file(self) -> bool:
        """Create new local file from default dictionary

        :return: Was the file created successfully
        :rtype: bool
        """
        self.write_dict_to_file(self.__default_dict)

        return True

    def delete_file(self) -> bool:
        """Delete local file

        :return: Was the file removed.
            False will be returned only if the local file does not exist at the time of deletion.
        :rtype: bool
        """
        if self.is_file_exist():
            remove(self.local_file_path)
            return True
        else:
            return False

    def is_file_exist(self) -> bool:
        """Check local file existence

        :return: Does the file exist
        :rtype: bool
        """
        return path.isfile(self.local_file_path)

    def write_dict_to_file(self, dictionary: dict):
        """Write dict from ``dictionary`` argument to local file bound to this object

        :param dictionary: Dictionary that should be written to file
        :type dictionary: dict
        """
        self._core__write_dict_to_file(self.local_file_path, dictionary)

    def read_file_as_dict(self) -> dict:
        """Read local file bound to this object as dictionary

        :return: Parsed to dictionary local file
        :rtype: dict
        """
        return self._core__read_file_to_dict(self.local_file_path)

    @staticmethod
    def _core__read_file_to_dict(file_path: str) -> dict:
        """Template for reading custom local files from path ``str`` as dictionary

        :param file_path: Path to local file
        :type file_path: str
        :return: Parsed local file dictionary
        :rtype: dict
        """
        pass

    @staticmethod
    def _core__write_dict_to_file(file_path: str, dictionary: dict):
        """Template for writing dictionaries into custom local path ``str``

        :param file_path: Path to local file
        :type file_path: str
        :param dictionary: Dictionary which will be written in ``file_path``
        :type dictionary: dict
        """
        pass


def create_directories(path_to_use: str, path_is_dir=False):
    """Create all directories from path

    :param path_to_use: The path to be created
    :type path_to_use: str
    :param path_is_dir: Is ``path_to_use`` ends with directory, defaults to False
    :type path_is_dir: bool, optional
    """
    path_to_use = path_to_use if path_is_dir else path.dirname(path_to_use)

    if not path.exists(path_to_use) and len(path_to_use) > 0:
        makedirs(path_to_use)


def recursive_dicts_merge(merge_from: dict, merge_to: dict) -> dict:
    """
    This function will recursively merge ``merge_from`` dictionary to ``merge_to``.
    Merging with this function, instead of the ``dict.update()`` method prevents from
    keys removal of nested dictionaries.

    :param merge_from: Dictionary to merge keys from
    :type merge_from: dict
    :param merge_to: Dictionary to merge keys to
    :type merge_to: dict
    :return: Dictionary with all ``merge_from`` keys merged into ``merge_to``
    :rtype: dict

    .. note::
        ``merge_from`` and ``merge_to`` dictionaries will not be modified in process of execution.
        Function will get their copies and work with them.
    """
    def __merge(merge_from: dict, merge_to: dict):
        for k, v in merge_from.items():
            if isinstance(v, dict):
                __merge(v, merge_to.setdefault(k, {}))
            else:
                merge_to[k] = v

    merge_from = merge_from.copy()
    result_dict = merge_to.copy()

    __merge(merge_from, merge_to)

    return result_dict


def parse_dict_values(input_dict: dict) -> dict:
    """
    This function is written for DIF parsers and languages, that doesn't support
    storing values in their original types, converting them all to ``str`` type.
    Function will recursively scan the input dictionary and will try to convert all
    keys with values which type is ``str``

    :param input_dict: [description]
    :type input_dict: dict
    :return: [description]
    :rtype: dict
    """
    def __recursive_safe_eval(inputd: dict, outputd: dict):
        # TODO
        for k, v in inputd.items():
            if not isinstance(v, str): continue

            try:
                evaled_v = literal_eval(v)
            except ValueError:
                continue
            else:
                if isinstance(evaled_v, dict):
                    __recursive_safe_eval(v, outputd.setdefault(k, {}))
                else:
                    outputd[k] = evaled_v

    result = {}
    __recursive_safe_eval(input_dict, result)

    return result