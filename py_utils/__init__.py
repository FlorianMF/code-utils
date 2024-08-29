"""Root package info."""
import os

from py_utils.__about__ import *  # noqa: F403

_PACKAGE_ROOT = os.path.dirname(__file__)
_PROJECT_ROOT = os.path.dirname(_PACKAGE_ROOT)