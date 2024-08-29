#!/usr/bin/env python

# Always prefer setuptools over distutils
from setuptools import setup

import py_utils.__about__ as about
from py_utils import setup_tools


# https://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-extras
# Define package extras. These are only installed if you specify them.
# From remote, use like `pip install python_utils[dev, docs]`
# From local copy of repo, use like `pip install ".[dev, docs]"`
def _prepare_extras():
    extras = {
        "docs": setup_tools.load_requirements(file_name="docs.txt"),
        # 'examples': setup_tools.load_requirements(file_name='examples.txt'),
        "extra": setup_tools.load_requirements(file_name="extra.txt"),
        "test": setup_tools.load_requirements(file_name="test.txt"),
    }
    extras["dev"] = extras["extra"] + extras["docs"] + extras["test"]
    extras["all"] = extras["dev"]  # + extras['examples']
    return extras


# Configure the package build and distribution
#   @see https://github.com/pypa/setuptools_scm
#
# To record the files created use:
#   python setup.py install --record files.txt
setup(
    name=about.__package_name__,  # Required
    version=about.__version__,  # Required
    author=about.__author_name__,  # Optional
    author_email=about.__author_email__,  # Optional
    url=about.__homepage__,  # Optional
    download_url=about.__download_url__,  # Optional
    license=about.__license__,
    # Optional
    install_requires=setup_tools.load_requirements(file_name="install.txt"),
    extras_require=_prepare_extras(),
)