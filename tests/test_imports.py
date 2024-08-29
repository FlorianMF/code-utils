import operator

import pytest

from py_utils.imports import _compare_version, _module_available


@pytest.mark.parametrize(
    ("module", "is_available"),
    (
        ("pytest", True),
        # ('a.b',True), # TODO: add test for nested imports which works with the already required packages
        ("bla", False),
        ("bla.xyz", False),
    ),
)
def test__module_available(module, is_available):
    assert _module_available(module) == is_available


def test__compare_version_mmp(monkeypatch):
    """Test Major-minor-patch version scheme."""
    monkeypatch.setattr(pytest, "__version__", "7.1.2")

    assert _compare_version("pytest", operator.ge, "7.1.2")
    assert not _compare_version("pytest", operator.lt, "7.1.1")


def test__compare_version_dev(monkeypatch):
    """Test with additional .dev version scheme."""
    monkeypatch.setattr(pytest, "__version__", "7.1.2.dev123")

    assert _compare_version("pytest", operator.ge, "7.1.2.dev123")
    assert not _compare_version("pytest", operator.ge, "7.1.2.dev124")

    assert _compare_version(
        "pytest",
        operator.ge,
        "7.1.2.dev123",
        use_base_version=True,
    )
    assert _compare_version(
        "pytest",
        operator.ge,
        "7.1.2.dev124",
        use_base_version=True,
    )


def test__compare_version_rc(monkeypatch):
    """Test with additional commit hash in version scheme."""
    # dev version before rc
    monkeypatch.setattr(pytest, "__version__", "7.1.2a0+0aef44c")

    assert not _compare_version("pytest", operator.ge, "7.1.2.rc0")
    assert not _compare_version("pytest", operator.ge, "7.1.2")

    assert _compare_version(
        "pytest",
        operator.ge,
        "7.1.2.rc0",
        use_base_version=True,
    )
    assert _compare_version(
        "pytest",
        operator.ge,
        "7.1.2",
        use_base_version=True,
    )
