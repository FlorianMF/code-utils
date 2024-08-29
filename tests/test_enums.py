import pytest

from py_utils.enums import MyEnum


class Enum1(MyEnum):
    FIZZ = "fizz"
    BUZZ = "buzz"

    @property
    def is_fizz(self) -> bool:
        return self == Enum1.FIZZ

    @property
    def is_buzz(self) -> bool:
        return self == Enum1.BUZZ


class Enum2(MyEnum):
    FIZZ = "fizz"


@pytest.mark.parametrize(
    ("str_", "enum", "is_contained"),
    (
        ("fizz", list(Enum1), True),
        ("buzz", list(Enum1), True),
        ("fizz", list(Enum2), True),
        ("buzz", list(Enum2), False),
    ),
)
def test_contains_str(str_, enum, is_contained):
    """Test that enum's keys' string representation are contained in the Enum."""
    # test with string values
    assert (str_ in enum) == is_contained


def test_contains_enum_key():
    """Test that enum's keys are contained in the Enum."""
    # test with enum values
    assert Enum1.FIZZ in list(Enum1)


def test_contains_enum_value():
    """Test that enum's values are contained in the Enum."""
    # test with enum values
    assert Enum1.FIZZ.value in list(Enum1)


def test_cross_access():
    """Test that you can check if a key in one Enum is contained in another Enum."""
    assert Enum1.FIZZ in list(Enum2)  # True
    assert Enum2.FIZZ in list(Enum1)  # True


@pytest.mark.parametrize(("key"), ("fizz", Enum1.FIZZ, Enum1.FIZZ.value))
def test_contains_without_tolist(key):
    """Test that you don't need to do `list(Enum)` to test if Enum.FIZZ in Enum."""
    assert key in Enum1


def test_properties():
    _enum = Enum1("fizz")
    print(_enum.is_fizz)  # True
    print(_enum.is_buzz)  # False


def test_from_str():
    assert Enum1.from_str("fizz") == Enum1.FIZZ
    assert Enum1.from_str("buzz") == Enum1.BUZZ


def test_usage_as_dict_key():
    """Test that the enum can be used as a key in a dictionary."""
    # setup a dict with an enum as a key
    a = {Enum1.FIZZ: "bla"}
    # access the dict with the enum and its value
    assert a["fizz"] == "bla"
    assert a[Enum1.FIZZ] == "bla"


@pytest.mark.parametrize(("key"), ("fizz", "Fizz", "FIZZ", "FiZz", "fiZZ"))
def test_case_insensitivity(key):
    assert key in Enum1
    assert Enum1.from_str(key) in Enum1


def test_values():
    assert Enum1.values == ["fizz", "buzz"]
    assert Enum2.values == ["fizz"]
    with pytest.raises(AttributeError):
        # method should not be available on instance
        Enum1("fizz").values
