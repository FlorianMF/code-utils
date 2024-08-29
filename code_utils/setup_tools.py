import os

import py_utils.__about__ as about
from py_utils import _PROJECT_ROOT


def load_requirements(
    path_dir: str = os.path.join(_PROJECT_ROOT, "requirements"),
    file_name: str = "install.txt",
    comment_char: str = "#",
) -> list[str]:
    """Load requirements from a file."""
    with open(os.path.join(path_dir, file_name)) as file:
        lines = [ln.strip() for ln in file.readlines()]
    requirements: list[str] = []
    for ln in lines:
        # import linked requirements file
        if ln.startswith("-r"):
            requirements += load_requirements(path_dir, ln.split(" ")[1])
        # filer all comments
        if ln.startswith(comment_char):
            continue
        if comment_char in ln:
            split = ln.split(comment_char)
            ln = split.pop(0)
            for elem in split:
                if elem.startswith("egg"):
                    ln += comment_char + elem
                else:
                    break
            ln = ln.strip()
        if ln:  # if requirement is not empty
            requirements.append(ln)
    return requirements


def load_long_description():
    url = os.path.join(about.__homepage__, "raw", about.__version__, "docs")
    text = open("README.md", encoding="utf-8").read()
    # replace relative repository path to absolute link to the release
    text = text.replace("](docs", f"]({url}")
    # SVG images are not readable on PyPI, so replace them  with PNG
    text = text.replace(".svg", ".png")
    return text


def read_file(file):
    with open(file) as f:
        content = f.read()
    return content
