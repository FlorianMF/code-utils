import itertools
from collections import defaultdict
from collections.abc import Mapping, MutableMapping
from typing import Any

__all__ = [
    "flatten_mapping",
    "flatten_mapping_to_top_level",
    "stringify_nested_mapping",
    "merge_lists_of_dicts_on_key",
]


def flatten_mapping(
    nested_mapping: Mapping,
    sep: str = ".",
) -> Mapping[str, Any]:
    """Flatten nested mapping to format: toplevel + sep + intermediate + sep + lowestkey: value.

    Example:
        >>> dictionary = {'top':
        ...                     {'intermediate1': {'low': 1},
        ...                      'intermediate2': {'low': 2,
        ...                                       'low3': 3}
        ...                     }
        ...             }
        >>> print(flatten_mapping(dictionary, sep='.'))
        {'top.intermediate1.low':  1,
        ...  'top.intermediate2.low':  2,
        ...  'top.intermediate2.low3': 3}

    Args:
        nested_mapping (Mapping): Mapping with nested mappings
        sep (str, optional): Character used to separate nesting levels. Defaults to ".".

    Returns:
        Mapping[str, Any]: Flatten mapping
    """
    _mapping = {}
    for key, item in nested_mapping.items():
        if isinstance(item, MutableMapping):
            for _key, _item in flatten_mapping(item, sep=sep).items():
                _mapping[str(key) + sep + str(_key)] = _item
        else:
            _mapping[str(key)] = item
    return _mapping


def flatten_mapping_to_top_level(
    nested_mapping: Mapping,
) -> Mapping[str, Any]:
    """Flatten nested mapping to top level without retaining intermediate keys.

        ! Attention !: If different nested items have the same key value, only one will be retained.

    Example:
        >>> dictionary = {'top':
        ...                     {'intermediate1': {'low': 1},
        ...                      'intermediate2': {'low': 2,
        ...                                       'low3': 3}
        ...                     }
        ...             }
        >>> print(flatten_mapping(dictionary, sep='.'))
        {'low': 2, 'low3': 3}

    Args:
        nested_mapping (Mapping): Mapping with nested mappings

    Returns:
        Mapping[str, Any]: Flatten mapping
    """
    _mapping = {}
    for key, item in nested_mapping.items():
        if isinstance(item, MutableMapping):
            for _key, _item in flatten_mapping_to_top_level(item).items():
                _mapping[str(_key)] = _item
        else:
            _mapping[str(key)] = item
    return _mapping


def stringify_nested_mapping(
    nested_mapping: Mapping[Any, Any],
) -> Mapping[str, str]:
    if isinstance(nested_mapping, Mapping):
        return {
            str(key): stringify_nested_mapping(item)
            for key, item in nested_mapping.items()
        }
    elif isinstance(nested_mapping, (list, tuple)):
        return [stringify_nested_mapping(item) for item in nested_mapping]
    else:
        return str(nested_mapping)


def merge_lists_of_dicts_on_key(
    dicts_lists: list[list[dict]],
    key: str,
) -> list[dict]:
    """Merges lists of lists of dicts on a common key. This key has to be present in all dictionaries.

    It constructs a dict of dicts. This dict has as keys the values of the dicts in the list[list[dict]] for the passed common `key`.
    It then returns the values of this dict to recreate a list[dict].

    Dictionaries with the same value for `key` update each other in the order they are processed.

    Args:
        dicts_lists (list[list[dict]]): List of dictionary lists
        key (str): Common dictionary key on which to merge

    Example:
        >>> list_a = [{'common_key': 1, 'key2': 2}]
        >>> list_b = [{'common_key': 3}]
        >>> list_c = [{'common_key': 4, 'key3': 5}]
        >>> list_d = [{'common_key': 1, 'key2': 6, 'key4': 7}]
        >>> merge_lists_of_dicts_on_key([list_a, list_b, list_c], key='common_key')
        [{'common_key': 1, 'key2': 6, 'key4': 7}, {'common_key': 3}, {'common_key': 4, 'key3': 5}]

    Returns:
        list[dict]: Merged list of dictionaries
    """
    # flatten list[list[dict]] to list[dict]
    list_of_dicts = list(itertools.chain(*dicts_lists))

    # use defaultdict(dict) to avoid having to create a key:dict pair
    merged = defaultdict(dict)

    for item in list_of_dicts:
        merged[item[key]].update(item)
    return list(merged.values())
