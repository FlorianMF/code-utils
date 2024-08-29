from datetime import datetime

import pytest

from py_utils.dates import is_leap


@pytest.mark.parametrize(
    ("year", "expected"),
    (
        (2020, True),
        (2021, False),
        (2022, False),
        (2023, False),
        (2024, True),
        (2025, False),
        (2391, False),
        (2392, True),
        (2393, False),
    ),
)
def test_is_leap(self, year, expected):
    assert is_leap(year) == expected

@pytest.mark.parametrize(
    ("year"),
    (1900, 2100, 2200, 2300, 2500, 2600, 2700, 2900, 3000),
)
def test_is_leap_special_cases(self, year):
    assert not is_leap(year)
