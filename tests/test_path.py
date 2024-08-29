from pathlib import Path

import pytest

from py_utils.path import get_all_extensions, strip_all_extensions


### round_to_nearest
@pytest.mark.parametrize(
    ("path", "expected"),
    (
        ("dir/file_name.ext", "dir/file_name"),
        (Path("dir/file_name.ext"), Path("dir/file_name")),
        ("dir/file_name.ext1.ext2", "dir/file_name"),
        (Path("dir/file_name.ext1.ext2"), Path("dir/file_name")),
        ("dir/file_name.ext1.ext2.ext3", "dir/file_name"),
        (Path("dir/file_name.ext1.ext2.ext3"), Path("dir/file_name")),
    ),
)
def test_strip_all_extensions(path, expected):
    res = strip_all_extensions(path)
    assert res == expected


@pytest.mark.parametrize(
    ("path", "expected"),
    (
        ("dir/file_name.ext", [".ext"]),
        (Path("dir/file_name.ext"), [".ext"]),
        ("dir/file_name.ext1.ext2", [".ext1", ".ext2"]),
        (Path("dir/file_name.ext1.ext2"), [".ext1", ".ext2"]),
        ("dir/file_name.ext1.ext2.ext3", [".ext1", ".ext2", ".ext3"]),
        (Path("dir/file_name.ext1.ext2.ext3"), [".ext1", ".ext2", ".ext3"]),
    ),
)
def test_get_all_extensions(path, expected):
    res = get_all_extensions(path)
    assert res == expected
