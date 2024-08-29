from pathlib import Path

from py_utils.types import PathLike


def strip_all_extensions(path: PathLike) -> PathLike:
    """Returns a path without its extensions. Works for multiple extensions (example: `.tar.gz`).

    Args:
        path (Pathlike): `Path` or `str` object

    Returns:
        Pathlike: path without file extensions. Of the same type as the input.
    """
    is_path = isinstance(path, Path)

    filename = Path(path)
    for _ in filename.suffixes:
        filename = filename.with_suffix("")

    return filename if is_path else str(filename)


def get_all_extensions(path: PathLike) -> list[str]:
    """Returns all extensions as list (from left to right).

    Args:
        path (Pathlike): `Path` or `str` object

    Example:
        >>> get_all_extensions('dir/filename.tar.gz')
        [".tar", ".gz"]
        >>> get_all_extensions(Path('dir/filename.tar.gz'))
        [".tar", ".gz"]

    Returns:
        list[str]: All extensions of path.
    """
    filename = Path(path)

    suffixes = filename.suffixes
    return suffixes
