import pytest

from py_utils.enums import MyIntEnum, MyStrEnum


###########
# StrEnum #
###########
class StrEnum1(MyStrEnum):
    FIZZ = "fizz"
    BUZZ = "buzz"

    @property
    def is_fizz(self) -> bool:
        return self == StrEnum1.FIZZ

    @property
    def is_buzz(self) -> bool:
        return self == StrEnum1.BUZZ


class StrEnum2(MyStrEnum):
    FIZZ = "fizz"


@pytest.mark.parametrize(
    ("str_", "enum", "is_contained"),
    (
        ("fizz", list(StrEnum1), True),
        ("buzz", list(StrEnum1), True),
        ("fizz", list(StrEnum2), True),
        ("buzz", list(StrEnum2), False),
    ),
)
def test_contains_str(str_, enum, is_contained):
    """Test that enum's keys' string representation are contained in the Enum."""
    # test with string values
    assert (str_ in enum) == is_contained


def test_contains_enum_key_str():
    """Test that enum's keys are contained in the Enum."""
    # test with enum values
    assert StrEnum1.FIZZ in list(StrEnum1)


def test_contains_enum_value_str():
    """Test that enum's values are contained in the Enum."""
    # test with enum values
    assert StrEnum1.FIZZ.value in list(StrEnum1)


def test_cross_access_str():
    """Test that you can check if a key in one Enum is contained in another Enum."""
    assert StrEnum1.FIZZ in list(StrEnum2)  # True
    assert StrEnum2.FIZZ in list(StrEnum1)  # True


@pytest.mark.parametrize(("key"), ("fizz", StrEnum1.FIZZ, StrEnum1.FIZZ.value))
def test_contains_without_tolist_str(key):
    """Test that you don't need to do `list(Enum)` to test if Enum.FIZZ in Enum."""
    assert key in StrEnum1


def test_properties():
    _enum = StrEnum1("fizz")
    print(_enum.is_fizz)  # True
    print(_enum.is_buzz)  # False


def test_from_str():
    assert StrEnum1.from_str("fizz") == StrEnum1.FIZZ
    assert StrEnum1.from_str("buzz") == StrEnum1.BUZZ


def test_usage_as_dict_key_str():
    """Test that the enum can be used as a key in a dictionary."""
    # setup a dict with an enum as a key
    a = {StrEnum1.FIZZ: "bla"}
    # access the dict with the enum and its value
    assert a["fizz"] == "bla"
    assert a[StrEnum1.FIZZ] == "bla"


@pytest.mark.parametrize(("key"), ("fizz", "Fizz", "FIZZ", "FiZz", "fiZZ"))
def test_case_insensitivity_str(key):
    assert key in StrEnum1
    assert StrEnum1.from_str(key) in StrEnum1


def test_values_str():
    assert StrEnum1.values == ["fizz", "buzz"]
    assert StrEnum2.values == ["fizz"]
    with pytest.raises(AttributeError):
        # method should not be available on instance
        StrEnum1("fizz").values


###########
# IntEnum #
###########
class IntEnum1(MyIntEnum):
    FIZZ = 0
    BUZZ = 1

    @property
    def is_fizz(self) -> bool:
        return self == IntEnum1.FIZZ

    @property
    def is_buzz(self) -> bool:
        return self == IntEnum1.BUZZ


class IntEnum2(MyIntEnum):
    FIZZ = 0


@pytest.mark.parametrize(
    ("int_", "enum", "is_contained"),
    (
        (0, list(IntEnum1), True),
        (1, list(IntEnum1), True),
        (0, list(IntEnum2), True),
        (1, list(IntEnum2), False),
    ),
)
def test_contains_int(int_, enum, is_contained):
    """Test that enum's keys' string representation are contained in the Enum."""
    # test with string values
    assert (int_ in enum) == is_contained


def test_contains_enum_key_int():
    """Test that enum's keys are contained in the Enum."""
    # test with enum values
    assert IntEnum1.FIZZ in list(IntEnum1)


def test_contains_enum_value_int():
    """Test that enum's values are contained in the Enum."""
    # test with enum values
    assert IntEnum1.FIZZ.value in list(IntEnum1)


def test_cross_access_int():
    """Test that you can check if a key in one Enum is contained in another Enum."""
    assert IntEnum1.FIZZ in list(IntEnum2)  # True
    assert IntEnum2.FIZZ in list(IntEnum1)  # True


@pytest.mark.parametrize(("key"), (0, IntEnum1.FIZZ, IntEnum1.FIZZ.value))
def test_contains_without_tolist_int(key):
    """Test that you don't need to do `list(Enum)` to test if Enum.FIZZ in Enum."""
    assert key in IntEnum1


def test_usage_as_dict_key_int():
    """Test that the enum can be used as a key in a dictionary."""
    # setup a dict with an enum as a key
    a = {IntEnum1.FIZZ: "bla"}
    # access the dict with the enum and its value
    assert a[0] == "bla"
    assert a[IntEnum1.FIZZ] == "bla"


def test_values_int():
    assert IntEnum1.values == [0, 1]
    assert IntEnum2.values == [0]
    with pytest.raises(AttributeError):
        # method should not be available on instance
        IntEnum1(0).values