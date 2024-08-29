import json
import os
import pickle
from pathlib import Path
from typing import Any

from python_utils.types import Pathlike

__all__ = [
    "read_txt",
    "save_txt",
    "load_json",
    "save_json",
    "load_pickle",
    "save_pickle",
]


def read_txt(file_path):
    with open(file_path) as f:
        content = f.read().splitlines()
    return content


def save_txt(data: str, path: Path, append: bool = True):
    """Save txt file.

    Args:
        data: data to save to txt
        path: path to txt file
        append (bool): whether to append to existing file. Defaults to True.
    """
    if isinstance(path, str):
        path = Path(path)
    if not (".txt" == path.suffix):
        path = str(path) + ".txt"

    # In case directory given is the current one, should pop an error
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    except Exception:
        pass

    mode = "a" if append else "w"
    with open(path, mode) as f:
        f.write(str(data))


def load_json(path: Pathlike, **kwargs: Any) -> Any:
    """Load json file.

    Args:
        path: path to json file
        **kwargs: keyword arguments passed to :func:`json.load`

    Returns:
        Any: json data
    """
    if isinstance(path, str):
        path = Path(path)
    if not (".json" == path.suffix):
        path = str(path) + ".json"

    with open(path, "rb") as f:
        data = json.load(f, **kwargs)
    return data


def save_json(
    data: Any,
    path: Pathlike,
    indent: int = 4,
    msg: str = None,
    log: bool = True,
    **kwargs: Any,
) -> None:
    """Load json file.

    Args:
        data: data to save to json
        path: path to json file
        indent: passed to json.dump
        **kwargs: keyword arguments passed to :func:`json.dump`
    """
    if isinstance(path, str):
        path = Path(path)
    if not (".json" == path.suffix):
        path = Path(str(path) + ".json")

    # In case directory given is the current one, should pop an error
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    except Exception:
        pass

    with open(path, "w") as f:
        json.dump(data, f, indent=indent, **kwargs)

    if log:
        if not msg:
            msg = f"Saved new json file at {path}"
        print(msg)


def load_pickle(path: Path, **kwargs) -> Any:
    """Load pickle file.

    Args:
        path: path to pickle file
        **kwargs: keyword arguments passed to :func:`pickle.load`

    Returns:
        Any: json data
    """
    if isinstance(path, str):
        path = Path(path)
    if not (path.suffix in [".pickle", ".pkl"]):
        path = Path(str(path) + ".pkl")

    with open(path, "rb") as f:
        data = pickle.load(f, **kwargs)
    return data


def save_pickle(data: Any, path: Pathlike, **kwargs):
    """Load pickle file.

    Args:
        data: data to save to pickle
        path: path to pickle file
        **kwargs: keyword arguments passed to :func:`pickle.dump`
    """
    if isinstance(path, str):
        path = Path(path)
    if not (path.suffix in [".pickle", ".pkl"]):
        path = str(path) + ".pkl"

    # In case directory given is the current one, should pop an error
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    except Exception:
        pass

    with open(str(path), "wb") as f:
        data = pickle.dump(data, f, **kwargs)
    return data
